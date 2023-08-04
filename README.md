
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
- (coming soon) Stream options chain and options contract
- (coming soon) Fetch historical options data

## ⏰ Status

| Status | Feature(s) | Goal |
| ------ | ------ | ---- |
| ✅ | First Release | Fetch options chain(w/o) greeks, single options contract, expiration dates |
| In-progress | Streaming data | Continuously provide options chain(w/o) greeks, single options data   |
| ❏ | Historical options data | Every time when Options data are fetch, the data are stored in a central online database. I am considering either running a cloud instance or hoping for significant adoption of the library to collectively capture all options data. |
---


Installation
------------

You can install the library by using:
``` {.sourceCode .bash}
pip install freeoptionschain
```
Import
------

``` {.sourceCode .python}
from FOC import *
```
Fetch all options expiration dates for a stock
---------------------------------
To fetch the options expiration date for a specific stock for a given  expiration date, you can
simply use:

``` {.sourceCode .python}
#create instance
ref_FOC = FOC()

# Options Chain of AAPL CALL options for 6 October 2023
options_chain = ref_FOC.get_expiration_dates("AAPL")
```
Fetch options chain with price
---------------------------------
To fetch the options chain for a specific stock for a given  expiration date, you can
simply use:

``` {.sourceCode .python}
#create instance
ref_FOC = FOC()

# Options Chain of AAPL CALL options for 6 October 2023
options_chain = ref_FOC.get_options_chain("AAPL","2023-10-06",OptionType.CALL)
```
Fetch options chain with greeks
---------------------------------
To fetch the options chain with greeks for a specific stock for a given  expiration date, you can
simply use:

``` {.sourceCode .python}
#create instance
ref_FOC = FOC()

# Options Chain of AAPL CALL options for 6 October 2023, with greeks
options_chain = ref_FOC.get_options_chain_greeks("AAPL","2023-10-06",OptionType.CALL)
```
Fetch options chain with greeks
---------------------------------
To fetch single options contract for a specific symbol, you can
simply use:

``` {.sourceCode .python}
#create instance
ref_FOC = FOC()

# AAPL CALL options with strike $200 for 6 October 2023, with greeks
options_contract = ref_FOC.get_options_price_data(ref_FOC.get_contract_symbol("AAPL",'2023-10-06','CALL',200.0))
```
What else?
----------

Let me know what other features would be useful to implement, create an issue on the repo or  [email me](mailto:benjaminchamwb@gmail.com).

If you like my work, do consider supporting me so that i can dedicate more time and attention.
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E0NVBCJ)
[![patreon](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Fshieldsio-patreon.vercel.app%2Fapi%3Fusername%3Dbenjamincham%26type%3Dpatrons&style=flat)](https://patreon.com/benjamincham)

---
Free Options Chain (FOC) is released under the
[MIT license](https://github.com/benjamincham/free_options_chain/blob/main/LICENSE).

<span style="font-size: 9px;">**Disclaimer:** *Free Options Chain (FOC) is an unofficial API wrapper to retrieve options data. It is in no way endorsed by or affiliated with NASDAQ or any associated organization.This authors accept no responsibility for any damage that might stem from use of this package. See the LICENSE file for more details.*<span>