from pytrends.request import TrendReq

pytrend = TrendReq(hl='en-GB', tz=360)
# Ability to load data by given dates or timeframe
# target_timeframe = '2021-07-01 2021-07-07'
target_timeframe = 'now 7-d' 

term_list = ["vpn", "hack", "cyber", "stream", "torrent"]
pytrend.build_payload(term_list, cat=0, timeframe=target_timeframe, geo='', gprop='')
gtrends_data = pytrend.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)

# Country name is stored as index in df
# Index data stored as column in df for transformations
gtrends_data['country'] = gtrends_data.index
gtrends_data.reset_index()

# Massaging dataframe from wide to long format.
staged_data = gtrends_data.melt(id_vars=["country"], 
        var_name="term", 
        value_name="score")

staged_data['rank'] = staged_data.groupby("country")["score"].rank("dense", ascending=False)
final_data = staged_data.sort_values(by=['country', 'rank', 'term'])
# Storing as CSV or DWH. For DWH need to have connector
final_data.to_csv('output.csv', index=False)
