import requests

def get_data():
    response = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd")
    data = response.json()
    
    return data