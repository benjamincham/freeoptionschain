from enum import Enum,auto

contract_symbol_delimiter = '---'
src_home_url = 'https://www.nasdaq.com/market-activity/stocks'

def get_options_price_url(tickersymbol:str, expiration_date:str,option_type):
    option_type = enum_OptionType_to_string(option_type)
    return f"https://api.nasdaq.com/api/quote/{tickersymbol}/option-chain?assetclass=stocks&limit=1000&fromdate={expiration_date}&todate={expiration_date}&excode=oprac&callput={option_type}&money=all&type=all"

def get_options_contract_url(tickersymbol:str, recordID:str):
    return f"https://api.nasdaq.com/api/quote/{tickersymbol}/option-chain?assetclass=stocks&recordID={recordID}"

def get_stock_price_url(tickersymbol:str, last_n_price:int):
    str_last_n_price = str(last_n_price)
    return f"https://api.nasdaq.com/api/quote/{tickersymbol}/realtime-trades?&limit={str_last_n_price}"

class OptionType(Enum):
    CALL = auto()
    PUT = auto()
    CALLPUT = auto()

def get_OptionType(optiontype):
    if isinstance(optiontype, str):
        try:
            return OptionType[optiontype.upper()]  # Convert the string to enum member
        except KeyError:
            raise ValueError(f"Invalid OptionType: {optiontype}")
    elif isinstance(optiontype, OptionType):
        return optiontype  # Return the enum member directly
    else:
        raise TypeError("Input value must be a string or a OptionType enum member")

def enum_OptionType_to_string(option_enum):
    return option_enum.name.lower()