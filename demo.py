from FOC import FOC

if __name__ == "__main__":

    ref_FOC = FOC()
    
    results = ref_FOC.get_options_price_data(ref_FOC.get_contract_symbol("AMC",'2023-08-11','CALL',4.0))
    print(results)