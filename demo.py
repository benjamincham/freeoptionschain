from FOC import FOC

if __name__ == "__main__":

    ref_FOC = FOC()
    
    options_price_data = ref_FOC.get_options_price_data(ref_FOC.get_contract_symbol("AMC",'2023-08-11','CALL',4.0))
    print(options_price_data)
    
    stocks_price_data = ref_FOC.get_stock_price("AAPL")
    print(stocks_price_data)