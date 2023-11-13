from FOC import FOC

def example_result_callback(result):
    print("Result from target function:", result)

if __name__ == "__main__":

    ref_FOC = FOC()
    
    stocks_price_data = ref_FOC.get_stock_price("AMC")
    print(stocks_price_data)

    options_price_data = ref_FOC.get_options_chain_greeks("AAPL","2023-11-10","CALL")
    print(options_price_data)
    
    options_price_data = ref_FOC.get_options_chain("AAPL","2023-11-10","CALL")
    print(options_price_data)
        
    options_price_data = ref_FOC.get_options_price_data(ref_FOC.get_contract_symbol("AAPL",'2023-11-10','CALL',175.0))
    print(options_price_data)
    

    ref_FOC.create_quote_stream_stock_price(2,'AMC',1,result_callback=example_result_callback)
    
    ref_FOC.create_quote_stream_options_chain(5,"AMC","2023-10-20","CALL",result_callback=example_result_callback)
    
    ref_FOC.create_quote_stream_options_chain_greeks(5,"AMC","2023-10-20","CALL",result_callback=example_result_callback)
    
    