import pandas as pd
from datetime import datetime
from tqdm import tqdm
from forex_python.converter import CurrencyRates

c = CurrencyRates()

df_train = pd.read_csv('train.csv')
df_test = pd.read_csv('test.csv')

df = pd.concat([df_train, df_test], ignore_index=True)

def fetch_rates(date , to_curr):
  print('Fetching rates for {} on {}'.format(to_curr, date))
  return 1.00 if to_curr == 'USD' else c.get_rate(to_curr, 'USD', date)

currencies = df['currency'].unique()
date = []
rate = []
to_currency = []

with tqdm(total=len(df['search_date'].unique())) as pbar:
  for d in df['search_date'].unique():
    d_ = datetime.strptime(str(d), '%Y%m%d')
    for curr in currencies:
      rate.append(fetch_rates(d_, curr))
      date.append(d)
      to_currency.append(curr)
    pbar.update()

result = pd.DataFrame()
result['date'] = date
result['currency'] = to_currency
result['rate'] = rate

result.to_csv('historical_rates.csv', index=False, mode='w')
