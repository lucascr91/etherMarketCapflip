import pandas as pd
pd.set_option('max.rows', 500)
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pickle as pkl

key=pkl.load(open('key.pkl','rb'))
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY':key,
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

def get_data(coin:str):
	complete = [coindata for coindata in  data['data'] if coindata['name'].lower()==coin.lower()][0]
	dict_coin= dict([('name', complete['name']), ('symbol', complete['symbol'])])
	dict_coin.update(complete['quote']['USD'])
	df= pd.DataFrame({k: [v] for k, v in dict_coin.items()})
	return df

print(get_data(coin="Ethereum"))
