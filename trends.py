from pytrends.request import TrendReq

pytrend = TrendReq(hl='en-GB', tz=360)

kw_list = ["vpn", "hack", "cyber", "stream", "torrent"]
pytrend.build_payload(kw_list, cat=0, timeframe='now 7-d', geo='', gprop='')
data = pytrend.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)


data['country'] = data.index
data.reset_index()
melted = data.melt(id_vars=["country"], 
        var_name="term", 
        value_name="score")

melted['rank'] = melted.groupby("country")["score"].rank("dense", ascending=False)
final = melted.sort_values(by=['country', 'rank', 'term'])
print(final.to_string() )
