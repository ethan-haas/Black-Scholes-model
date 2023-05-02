import numpy as np
import pandas as pd
from scipy.stats import norm
from datetime import datetime
from wallstreet import Stock, Call, Put
import concurrent.futures

ticker = "AAPL"
risk_free_rate = 0.034

def black_scholes(stock_price, strike_price, time_to_expiry, risk_free_rate, volatility, option_type):
    d1 = (np.log(stock_price / strike_price) + (risk_free_rate + 0.5 * volatility ** 2) * time_to_expiry) / (volatility * np.sqrt(time_to_expiry))
    d2 = d1 - volatility * np.sqrt(time_to_expiry)
    
    if option_type == "call":
        option_value = stock_price * norm.cdf(d1) - strike_price * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2)
    elif option_type == "put":
        option_value = strike_price * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(-d2) - stock_price * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type: must be 'call' or 'put'")

    return option_value

def filter_positive_value_diff(options_df):
    return options_df[options_df["value_diff"] > 0]

def process_expiration_date(date):
    call_option = Call(ticker, d=date.day, m=date.month, y=date.year)
    put_option = Put(ticker, d=date.day, m=date.month, y=date.year)
    
    calls = []
    puts = []
    
    for strike in call_option.strikes:
        call_option.set_strike(strike)
        implied_volatility = call_option.implied_volatility()
        expiration_date = datetime.strptime(call_option.expiration, "%d-%m-%Y")
        time_to_expiry = (expiration_date - datetime.today()).days / 365
        calls.append({
            "Contract Name": call_option.code,
            "Strike": strike,
            "Last Price": call_option.price,
            "time_to_expiry": time_to_expiry,
            "Implied Volatility": implied_volatility,
            "bs_value": black_scholes(stock_price, strike, time_to_expiry, risk_free_rate, implied_volatility, "call"),
            "value_diff": None
        })

    for strike in put_option.strikes:
        put_option.set_strike(strike)
        implied_volatility = put_option.implied_volatility()
        expiration_date = datetime.strptime(put_option.expiration, "%d-%m-%Y")
        time_to_expiry = (expiration_date - datetime.today()).days / 365
        puts.append({
            "Contract Name": put_option.code,
            "Strike": strike,
            "Last Price": put_option.price,
            "time_to_expiry": time_to_expiry,
            "Implied Volatility": implied_volatility,
            "bs_value": black_scholes(stock_price, strike, time_to_expiry, risk_free_rate, implied_volatility, "put"),
            "value_diff": None
        })

    return calls, puts

# Get the stock price for the most recent trading day
s = Stock(ticker)
stock_price = s.price

# Get list of expiration dates
g = Call(ticker)
expiration_dates = g.expirations
date_objects = [datetime.strptime(date_str, "%d-%m-%Y") for date_str in expiration_dates]

# Initialize empty lists for calls and puts
all_calls = []
all_puts = []

# Loop through each expiration date using concurrent.futures for parallelism
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_expiration_date, date) for date in date_objects]
    
    for future in concurrent.futures.as_completed(futures):
        calls, puts = future.result()
        all_calls.extend(calls)
        all_puts.extend(puts)

all_calls = pd.DataFrame(all_calls)
all_puts = pd.DataFrame(all_puts)



all_calls["value_diff"] = all_calls["bs_value"] - all_calls["Last Price"]
all_puts["value_diff"] = all_puts["bs_value"] - all_puts["Last Price"]

print("Call Options:")
print(all_calls[["Contract Name", "Strike", "Last Price", "bs_value", "value_diff"]])
print("\nPut Options:")
print(all_puts[["Contract Name", "Strike", "Last Price", "bs_value", "value_diff"]])

# Write calls and puts to separate sheets in a single Excel file
with pd.ExcelWriter(ticker + '_options_data.xlsx', engine='openpyxl') as writer:
    all_calls.to_excel(writer, sheet_name='Calls', index=False)
    all_puts.to_excel(writer, sheet_name='Puts', index=False)

# Find most undervalued call and put options
positive_value_diff_calls = filter_positive_value_diff(all_calls)
positive_value_diff_puts = filter_positive_value_diff(all_puts)

try:
    most_undervalued_call_idx = positive_value_diff_calls['value_diff'].idxmax()
    most_undervalued_call = positive_value_diff_calls.loc[most_undervalued_call_idx]
    print("Most undervalued call option:")
    print(most_undervalued_call[['Contract Name', 'Strike', 'Last Price', 'time_to_expiry', 'bs_value', 'value_diff']])
except ValueError:
    print("No undervalued call options found.")

try:
    most_undervalued_put_idx = positive_value_diff_puts['value_diff'].idxmax()
    most_undervalued_put = positive_value_diff_puts.loc[most_undervalued_put_idx]
    print("\nMost undervalued put option:")
    print(most_undervalued_put[['Contract Name', 'Strike', 'Last Price', 'time_to_expiry', 'bs_value', 'value_diff']])
except ValueError:
    print("No undervalued put options found.")

print("\n\nOptions data has been saved to '" + ticker +  "_options_data.xlsx'\n\n")
