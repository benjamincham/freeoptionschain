<!-- markdownlint-disable MD033 MD041 -->
<h1 align="center">
    Free Options Chain (FOC) data for python
</h1>
<p align="center">
    <strong>This library module retrieves stock options data from NASDAQ</strong>
</p>

---

## Why <span style="color:lightblue;">Free Options Chain (FOC) </span> ?

The Free Options Chain (FOC) Module offers accurate options data at no cost, intended for Research and Personal use only.

FOC is created to address the limitations and issues associated with free APIs and other sources of Options data. For instance: YahooFinance is known for providing data with erroneous Volume and Open-Interest information.

## Core Features

- Fetch options chain price only
- Fetch options chain with greeks
- Fetch single options contract with details
- Get all options expiration dates for a stock
- Stream quotes of options contract, options chain and stock price
- (coming soon) Fetch historical options data

## ⏰ Status

| Status      | Feature(s)              | Goal                                                                                                                                                                                                |
| ----------- | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ✅          | First Release           | Fetch options chain(w/o) greeks, single options contract, expiration dates                                                                                                                          |
| ✅          | Quote Streaming        | Continuously provide options chain(w/o) greeks, single options data                                                                                                                                 |
| ❏           | Historical options data | Options data are fetched and stored in a central online database. I'm considering either using a cloud instance or relying on widespread library adoption to capture all options data collectively. |

---

## Installation

You can install the library by using:

```{.sourceCode .bash}
pip install freeoptionschain
```

## Import

```{.sourceCode .python}
from FOC import FOC
```

## Fetch all options expiration dates for a stock

To fetch the options expiration date for a specific stock for a given expiration date, you can simply use:

```{.sourceCode .python}
#create instance
ref_FOC = FOC()

# Fetch options expiration dates for 'AAPL'
options_chain = ref_FOC.get_expiration_dates("AAPL")
```

## Fetch options chain with price

To fetch the options chain for a specific stock for a given expiration date, you can simply use:

```{.sourceCode .python}
#create instance
ref_FOC = FOC()

# Options Chain of AAPL CALL options for 6 October 2023
options_chain = ref_FOC.get_options_chain("AAPL","2023-10-06",OptionType.CALL)
```

## Fetch options chain with greeks

To fetch the options chain with greeks for a specific stock for a given expiration date, you can simply use:

```{.sourceCode .python}
#create instance
ref_FOC = FOC()

# Options Chain of AAPL CALL options for 6 October 2023, with greeks
options_chain = ref_FOC.get_options_chain_greeks("AAPL","2023-10-06",OptionType.CALL)
```

## Fetch single options contract

To fetch single options contract for a specific symbol, you can simply use:

```{.sourceCode .python}
#create instance
ref_FOC = FOC()

# get options contract symbol for AAPL CALL options with strike $200 for 6 October 2023
contract_symbol = ref_FOC.get_contract_symbol("AAPL",'2023-10-06','CALL',200.0)
#fetch options contract with greeks
options_contract = ref_FOC.get_options_price_data(contract_symbol)
```

## Fetch current price of a stock

To fetch the current price of a ticker symbol, you can simply use:

```{.sourceCode .python}
#create instance
ref_FOC = FOC()

#fetch current stock price for AAPL
stock_price = ref_FOC.get_stock_price("AAPL")
```

## Create quote streams

To create quote streams of options contract/chain or stock price, you can use:

```{.sourceCode .python}
#create instance
ref_FOC = FOC()

#example of callback function
def example_result_callback(result):
    print("Result from target function:", result)

ref_FOC.create_quote_stream_stock_price(20,'AAPL',1,result_callback=example_result_callback)

ref_FOC.create_quote_stream_options_price_data(20,'AMC---230811C00004000',result_callback=example_result_callback)

ref_FOC.create_quote_stream_options_chain(5,"AMC","2023-10-20","CALL",result_callback=example_result_callback)

ref_FOC.create_quote_stream_options_chain_greeks(5,"AMC","2023-10-20","CALL",result_callback=example_result_callback)
    
```

## What else?

Let me know what other features would be useful to implement, create an issue on the repo or [email me](mailto:benjaminchamwb@gmail.com).

If you like my work, do consider supporting me so that i can dedicate more time and attention.
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E0NVBCJ)
[![patreon](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Fshieldsio-patreon.vercel.app%2Fapi%3Fusername%3Dbenjamincham%26type%3Dpatrons&style=flat)](https://patreon.com/benjamincham)

---

Free Options Chain (FOC) is released under the
[MIT license](https://github.com/benjamincham/free_options_chain/blob/main/LICENSE).

<span style="font-size: 9px;">**Disclaimer:** _Free Options Chain (FOC) is an unofficial API wrapper to retrieve options data. It is in no way endorsed by or affiliated with NASDAQ or any associated organization.This authors accept no responsibility for any damage that might stem from use of this package. See the LICENSE file for more details._<span>
