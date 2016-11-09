from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib2
import pandas as pd
import datetime


base_url = "http://www.chittorgarh.com/report/nse_nifty_index_50_stocks_live_list/7/"
user_agent = UserAgent()
headers = { 'User-Agent': str(user_agent.random) }
req = urllib2.Request(base_url, None, headers)
read_url = urllib2.urlopen(req)
response = read_url.read()
soup = BeautifulSoup(response, "lxml")
table = soup.find_all("table", attrs={'class': 'table'})
table_data = [j for i in table for j in i.find_all("tr")]
table_header = [str(j.text.strip()) for d in table_data[0:1]
                for j in d.find_all("th")]
table_value = table_data[1:]
column_header = ["Company_Name", "Open", "High", "Low", "LTP", "Change", "LTP1", "Percentage_Change", "Shares_Traded", "Trades", "Date_Updated"]
dataset = []
for d in table_value:
    cols = d.find_all("td")
    cols = [str(element.text.strip()) for element in cols]
    dataset.append(tuple(cols))

data_frame = pd.DataFrame(data=dataset, columns=column_header)
data_frame['Date_Updated'] = pd.to_datetime(data_frame['Date_Updated'], format="%m/%d/%Y")
now = datetime.datetime.now()
csv_frame = data_frame.to_csv("today_{0}.csv".format(now), index=False)
