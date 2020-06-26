import requests
from bs4 import BeautifulSoup
import html5lib

curr_source = requests.get("https://www.easymarkets.com/int/learn-centre/discover-trading/currency-acronyms-and-abbreviations/")
curr_soup = BeautifulSoup(curr_source.content,'html5lib')

currency_ref = [i.text.split("\n")[2] for i in curr_soup.findAll('tr')][1:]

for i in range(len(currency_ref)):
    if "EURO" in currency_ref[i]:
        currency_ref[i] = currency_ref[i].split(" ")[0]

ref = {"from":"","to":""}
for i in ["from","to"]:
    while True:
        inp = input(f"Enter the currency to change {i}: ").upper()
        if inp in currency_ref:
            ref[i] = inp
            break
        else:
            print("Invalid input, try again.")

with open("apikey.txt",'r') as api:
    api_key = api.read()

base = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
main = f"{base}&from_currency={ref['from']}&to_currency={ref['to']}&apikey={api_key}" 

rate = requests.get(main).json()
exchange_rate = float(rate["Realtime Currency Exchange Rate"]["5. Exchange Rate"])

inp_curr = float(input("\nEnter amount of money to be converted: "))

print(f"\nToday's rate of conversion from {rate['Realtime Currency Exchange Rate']['2. From_Currency Name']} to {rate['Realtime Currency Exchange Rate']['3. To_Currency Code']} is : {exchange_rate:.2f}")

converted = inp_curr * exchange_rate

print(f"\nConverted Currency is {ref['to']} {converted:.2f}")