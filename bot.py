def send_tweet():

  import pandas as pd
  pd.set_option('max.rows', 500)
  from requests import Request, Session
  from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
  import json
  import os
  import tweepy
  from dotenv import load_dotenv
  load_dotenv()

  API_COINMKT_KEY=os.getenv('API_COINMKT_KEY')
  API_TWT_KEY=os.getenv('API_TWT_KEY')
  API_SECRET_KEY=os.getenv('API_SECRET_KEY')
  ACCESS_TOKEN=os.getenv('ACCESS_TOKEN')
  ACCESS_TOKEN_SECRET=os.getenv('ACCESS_TOKEN_SECRET')

  auth = tweepy.OAuthHandler(API_TWT_KEY, API_SECRET_KEY)
  auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
  api = tweepy.API(auth)

  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
  parameters = {
    'start':'1',
    'limit':'5000',
    'convert':'USD'
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY':API_COINMKT_KEY,
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

  eth = get_data(coin="Ethereum")
  btc = get_data(coin="Bitcoin")

  ratio=float(eth.market_cap/btc.market_cap)

  status= "The ETH/BTC market cap ratio is currently {:.1f}% \n\n#ethereum $ETH".format(100*ratio)

  return api.update_status(status=status)

