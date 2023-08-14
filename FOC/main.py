from .defined import *
from .db import *
from .intervalrunner import IntervalRunner
import requests, pytz,threading, concurrent.futures, pytz,json
import pandas as pd
import yfinance as yf
from yahoo_fin import options as op
from datetime import datetime
from dateutil.relativedelta import relativedelta
from urllib.parse import unquote
from json import JSONDecodeError

class FOC:
    
    def __init__(self):
        self.dbconn = dbhubIO()
        self.session = self.get_session()
        self.User_Agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        self.cookies_dict = self.session.cookies.get_dict()
        
        self.quote_streams = {}
    
    def __del__(self):
        self.dbconn.close_connection()
        
    def get_session(self):
        session = None
        
        try:
            session = requests.Session()
            session.get(src_home_url, headers= {"User-Agent": self.User_Agent})
        except Exception:
            pass

        return session
    
    def get_expiration_dates(self,ticker):
        expiration_dates = op.get_expiration_dates(ticker)
        for idx, expiration_date in enumerate(expiration_dates):
            expiration_dates[idx] = datetime.strptime(expiration_date, "%B %d, %Y").strftime("%Y-%m-%d")
        return expiration_dates
    
    def get_options_chain_greeks(self,tickersymbol:str,expiration_date:str,option_type):
            options_chain = None
            option_type = get_OptionType(option_type)
            options_chain = self.get_options_chain_price(tickersymbol,expiration_date,option_type)
            options_chain['tickersymbol'] = tickersymbol
            options_chain['recordID'] = options_chain['drillDownURL'].str.split('/').str[-1]
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = list(executor.map(self.get_options_greeks, options_chain['recordID']))
                
            # Concatenate the results into a single DataFrame
            df_results = pd.concat(results, ignore_index=True)

            # Merge the results DataFrame with the original DataFrame based on index
            options_chain = options_chain.merge(df_results)
            options_chain = self.drop_uncessary_columns(options_chain,option_type)
            
            if self.dbconn and options_chain is not None:
                df_to_save = options_chain.copy()
                df_to_save['tickersymbol'] = tickersymbol
                df_to_save['expiration_date'] = expiration_date
                df_to_save['timestamp'] = self.get_timestamp()
                self.dbconn.insert_data("options_chain_greeks",df_to_save)
                
            return options_chain
    
    def get_timestamp(self):
        return datetime.now(pytz.timezone("US/Eastern")).strftime('%Y-%m-%d %H:%M:%S')
    
    def get_options_chain(self,tickersymbol:str,expiration_date:str,option_type):
            options_chain = None
            option_type = get_OptionType(option_type)
            options_chain = self.get_options_chain_price(tickersymbol,expiration_date,option_type)
            if options_chain is not None:
                options_chain = self.drop_uncessary_columns(options_chain,option_type)
                options_chain['timestamp'] = self.get_timestamp()
                
                if self.dbconn and options_chain is not None:
                    df_to_save = options_chain.copy()
                    df_to_save['tickersymbol'] = tickersymbol
                    df_to_save['expiration_date'] = expiration_date
                    self.dbconn.insert_data("options_chain",df_to_save)
                    
            return options_chain
        
    def drop_columns_with_prefix(self,df, prefixes):
        if prefixes is not None:
            columns_to_drop = [col for col in df.columns if any(col.startswith(prefix) for prefix in prefixes)]
            df.drop(columns=columns_to_drop, inplace=True)
        return df

    def drop_uncessary_columns(self,options_chain_df, OptionType:OptionType):
        dropcolumns_prefix = None
        if OptionType == OptionType.CALL:
            dropcolumns_prefix = 'p_'
        elif OptionType == OptionType.PUT:
            dropcolumns_prefix = 'c_'
        else:
            dropcolumns_prefix = None
        
        return self.drop_columns_with_prefix(options_chain_df,dropcolumns_prefix)

    def json_extract_node(self,json_data, hierarchy_keys):
        try:
            for key in hierarchy_keys:
                json_data = json_data[key]
            return json_data
        except (TypeError, KeyError):
            raise ValueError("Invalid json keys.")
    
    def get_options_greeks(self,recordID):
        options_chain_greeks = None
        options_data = self.get_options_data(recordID)
        
        if options_data is not None:
            list_greeks=[]
            list_greeks.append(self.extract_greeks(options_data,'optionChainPutData','p_'))
            list_greeks.append(self.extract_greeks(options_data,'optionChainCallData','c_'))
            
            for idx,greek in enumerate(list_greeks):
                list_greeks[idx] = greek.set_index('label').T.rename_axis(recordID)
            
            options_chain_greeks = pd.concat(list_greeks, axis=1)
            options_chain_greeks['recordID'] = recordID
            options_chain_greeks = options_chain_greeks.rename_axis(recordID)
            
        return options_chain_greeks
    
    def extract_greeks(self,json_data,json_fieldname:str,prefix:str = None):
        def add_prefix(label,prefix):
            return prefix + label
        df = None
        data_list = json_data['data'][json_fieldname]['optionChainGreeksList'].values()
        df = pd.DataFrame(data_list)
        if prefix is not None:
            df['label'] = df['label'].apply(add_prefix, args=(prefix,))
            
        df = df.rename(columns={"value": "value"})

        return df
    
    def get_options_chain_price(self,tickersymbol:str,expiration_date:str,option_type:OptionType=OptionType.CALL):
        options_chain_price = None
        
        url = get_options_price_url(tickersymbol,expiration_date,option_type)
        headers = {
                    'authority': 'api.nasdaq.com',
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'origin': 'https://www.nasdaq.com',
                    'referer': 'https://www.nasdaq.com/',
                    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Linux"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': self.User_Agent,
                    }
        
        response = requests.get(
                                url,
                                headers=headers,
                                cookies=self.session.cookies,
                                timeout=100
                            )
        try:
            options_chain_price = response.json()
        except JSONDecodeError:
            pass
        
        if options_chain_price is not None:
            data_list = self.json_extract_node(options_chain_price,['data','table','rows'])
            df = pd.DataFrame(data_list)
            # Set the 'expiryDate' column as the index
            df.set_index('expiryDate', inplace=True)
            options_chain_price = df.groupby('expiryDate')
            options_chain_price = options_chain_price.get_group((list(options_chain_price.groups)[0]))

        return options_chain_price
    
    def get_contract_symbol(self,tickersymbol:str, expiration_date:str, option_type,strike_price):
        contract_tickersymbol = tickersymbol.upper()
        contract_expiration = datetime.strptime(expiration_date, "%Y-%m-%d").strftime("%y%m%d")
        contract_optiontype = 'C' if get_OptionType(option_type) == OptionType.CALL else 'P'
        options_price_formatted = int(float(strike_price) * 1000)
        contract_strike = f'{options_price_formatted:08d}'
        
        return str(contract_tickersymbol+contract_symbol_delimiter+contract_expiration+contract_optiontype+contract_strike)
    
    def get_options_data(self,contract_symbol:str):
        options_data = None
        tickersymbol = contract_symbol.split(contract_symbol_delimiter)[0]
        
        url = get_options_contract_url(tickersymbol,contract_symbol)
        headers = {
                    'authority': 'api.nasdaq.com',
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'origin': 'https://www.nasdaq.com',
                    'referer': 'https://www.nasdaq.com/',
                    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Linux"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': self.User_Agent,
                    }
        
        response = requests.get(
                                url,
                                headers=headers,
                                cookies=self.session.cookies,
                                timeout=100
                            )
        try:
            options_data = response.json()
        except JSONDecodeError:
            pass
        
        return options_data
    
    def get_stocks_data(self,tickersymbol:str,last_n_price:int):
        stocks_data = None

        url = get_stock_price_url(tickersymbol,last_n_price)
        headers = {
                    'authority': 'api.nasdaq.com',
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'origin': 'https://www.nasdaq.com',
                    'referer': 'https://www.nasdaq.com/',
                    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Linux"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': self.User_Agent,
                    }
        
        response = requests.get(
                                url,
                                headers=headers,
                                cookies=self.session.cookies,
                                timeout=100
                            )
        try:
            stocks_data = response.json()
        except JSONDecodeError:
            pass
        
        return stocks_data
    
    def get_options_type(self,contract_symbol:str):
        char_optiontype = contract_symbol.split(contract_symbol_delimiter)[-1][6] #options type symbol is the 7th char, e.g. YYMMddT000000
        char_optiontype = char_optiontype.upper()
        optiontype = OptionType.CALL if char_optiontype == 'C' else OptionType.PUT
        return optiontype

    def get_options_price_data(self,contract_symbol:str):

        options_price_data = None
        options_data = self.get_options_data(contract_symbol)
        options_data_fieldtype = 'optionChainCallData' if self.get_options_type(contract_symbol) == OptionType.CALL else 'optionChainPutData'
        if options_data is not None:
            list_values=[]
            list_values.append(self.json_extract_node(options_data,['data',options_data_fieldtype,'optionChainListData']).values())
            list_values.append(self.json_extract_node(options_data,['data',options_data_fieldtype,'optionChainGreeksList']).values())
            
            for idx,values in enumerate(list_values):
                list_values[idx] = pd.DataFrame(values).set_index('label').T.rename_axis(contract_symbol)
            
            options_price_data = pd.concat(list_values, axis=1)
            timestamp_string = self.json_extract_node(options_data,['data',options_data_fieldtype,'timeStamp'])
            timestamp_string = " ".join(timestamp_string.split(" ")[:-1])
            datetime_object = datetime.strptime(timestamp_string, "%b %d, %Y %I:%M %p")
            options_price_data['timestamp']=  datetime_object.strftime("%Y-%m-%d %H:%M:%S")
            options_price_data['contract_symbol'] = contract_symbol
            
            if self.dbconn:
                df_to_save = options_price_data.copy()
                self.dbconn.insert_data("options_price_data", df_to_save)
            
        return options_price_data
    
    def get_stock_price(self, tickersymbol:str, last_n_price = 1):
        
        stock_price_data = None
        stock_data = self.get_stocks_data(tickersymbol,last_n_price)
        if stock_data is not None:
            stock_price_data = {}
            stock_price_data['price'] = json.dumps(self.json_extract_node(stock_data,['data','rows']))
            
            price_meta = self.json_extract_node(stock_data,['data','topTable','rows'])[0]
            stock_price_data.update(price_meta)
            stock_price_data = pd.DataFrame(stock_price_data, index=[0])

        return stock_price_data
    
    def create_quote_stream_stock_price(self, interval_secs:int, symbol:str, last_n_price = 1,result_callback=None):
        
        instance_IntervalRunner = IntervalRunner(interval_secs=interval_secs, target_func=self.get_stock_price, func_args=(symbol,last_n_price), result_callback=result_callback)
        self.register_start_quote_stream(symbol,instance_IntervalRunner)
        
    def create_quote_stream_options_price_data(self, interval_secs:int, symbol:str, result_callback=None ):
        
        instance_IntervalRunner = IntervalRunner(interval_secs=interval_secs, target_func=self.get_options_price_data, func_args=(symbol,), result_callback=result_callback)
        self.register_start_quote_stream(symbol,instance_IntervalRunner)
        
    def create_quote_stream_options_chain(self, interval_secs:int, symbol:str,expiration_date:str,option_type, result_callback=None ):
        
        instance_IntervalRunner = IntervalRunner(interval_secs=interval_secs, target_func=self.get_options_chain, func_args=(symbol,expiration_date,option_type), result_callback=result_callback)
        self.register_start_quote_stream(symbol,instance_IntervalRunner)
    
    def create_quote_stream_options_chain_greeks(self, interval_secs:int, symbol:str,expiration_date:str,option_type, result_callback=None ):
        
        instance_IntervalRunner = IntervalRunner(interval_secs=interval_secs, target_func=self.get_options_chain_greeks, func_args=(symbol,expiration_date,option_type), result_callback=result_callback)
        self.register_start_quote_stream(symbol,instance_IntervalRunner)
        
    def register_start_quote_stream(self,symbol,intervalRunner:IntervalRunner):
        intervalRunner.start()
        self.quote_streams[symbol] = intervalRunner
        
    def stop_quote_stream(self,symbol):
        instance_IntervalRunner = self.quote_streams[symbol]
        instance_IntervalRunner.stop()
        self.quote_streams.pop(symbol)
                
    def update_quote_stream_interval(self,symbol,new_interval:int):
        instance_IntervalRunner = self.quote_streams[symbol]
        instance_IntervalRunner.interval = new_interval
        
    def stop_quote_stream_all(self):
        for key in list(self.quote_streams.keys()):
            self.stop_quote_stream(key)
            
    def list_quote_steram(self):
        return list(self.quote_streams.keys())