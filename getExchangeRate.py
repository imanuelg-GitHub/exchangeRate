import sys

import requests
from requests.exceptions import HTTPError

if len(sys.argv) != 2:
    print("Usage :", sys.argv[0], "<filename>")
    sys.exit(0)


def process_file():
    BalanceDict = {}  # define empty key-value pair dictionary
    file = open(sys.argv[1])
    while True:
        line = file.readline()  # get line from file

        if not line:  # if line is empty, we reached end of file
            break
        entry = line.strip().split()
        BalanceDict[entry[0]] = BalanceDict.get(entry[0], 0) + int(entry[1])
    file.close()
    return BalanceDict


def process_user_input(BalanceDict):
    ToCCY = "usd"
    while True:
        for ccy, amt in BalanceDict.items():
            if amt != 0 and ccy != 'USD':
                # currencies on this url must be lowercase
                try:
                    url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/" + ccy.lower() + "/" + ToCCY.lower() + ".json"
                    response = requests.get(url)
                    response.raise_for_status()
                except HTTPError as e:
                    print(ccy, "ccy not found. Please try again...")
                    del BalanceDict[u_ccy]
                    break
                else:
                    print(ccy, amt, "( USD ", round(float(response.json()[ToCCY]) * amt, 2), ")")  # Calculate FX amount
        try:
            u_ccy, u_amt = input("\nEnter ccy, amt (Quit 0 to end user input) : ").split()
            BalanceDict[u_ccy] = BalanceDict.get(u_ccy, 0) + int(u_amt)
            if u_ccy == "Quit" and u_amt == "0":
                break
        except ValueError:
            print("You must enter ccy and amt. Please try again.")
            continue


BalanceDict = process_file()
process_user_input(BalanceDict)
