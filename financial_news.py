import feedparser
import pandas as pd
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from urllib.parse import quote
import time

# --- 1. Nifty 50 Members by Timeline --- #
def get_nifty50_members(dt):
    if dt < datetime(2017, 9, 29):
        return {
            'HDFCBANK': 'HDFC Bank', 'RELIANCE': 'Reliance Industries', 'HDFC': 'HDFC', 'ITC': 'ITC',
            'HINDUNILVR': 'Hindustan Unilever', 'LT': 'Larsen & Toubro', 'SBI': 'State Bank of India',
            'TATAMOTORS': 'Tata Motors', 'DRREDDY': 'Dr Reddy’s', 'TATASTEEL': 'Tata Steel', 'GRASIM': 'Grasim Industries',
            'HEROMOTOCO': 'Hero MotoCorp', 'HINDALCO': 'Hindalco'
        }
    elif dt < datetime(2018,4,2):
        d = get_nifty50_members(datetime(2017,1,1))
        d['BAJFINANCE'] = 'Bajaj Finance'
        return d
    elif dt < datetime(2018,9,28):
        d = get_nifty50_members(datetime(2017,9,29))
        d['BAJAJFINSV'] = 'Bajaj Finserv'
        return d
    elif dt < datetime(2019,3,29):
        d = get_nifty50_members(datetime(2018,4,2))
        d['JSWSTEEL'] = 'JSW Steel'
        return d
    elif dt < datetime(2019,9,27):
        d = get_nifty50_members(datetime(2018,9,28))
        d['BRITANNIA'] = 'Britannia Industries'
        return d
    elif dt < datetime(2020,7,31):
        d = get_nifty50_members(datetime(2019,3,29))
        d['NESTLEIND'] = 'Nestle India'
        return d
    elif dt < datetime(2020,9,25):
        d = get_nifty50_members(datetime(2019,9,27))
        d['HDFCLIFE'] = 'HDFC Life'
        return d
    elif dt < datetime(2021,3,31):
        d = get_nifty50_members(datetime(2020,7,31))
        d['SBILIFE'] = 'SBI Life Insurance'
        return d
    elif dt < datetime(2022,3,31):
        d = get_nifty50_members(datetime(2020,9,25))
        d['TATACONSUM'] = 'Tata Consumer Products'
        return d
    elif dt < datetime(2022,9,30):
        d = get_nifty50_members(datetime(2021,3,31))
        d['APOLLOHOSP'] = 'Apollo Hospitals'
        return d
    elif dt < datetime(2024,3,28):
        d = get_nifty50_members(datetime(2022,3,31))
        d['ADANIENT'] = 'Adani Enterprises'
        return d
    elif dt < datetime(2024,9,30):
        d = get_nifty50_members(datetime(2024,3,28))
        d['SHRIRAMFIN'] = 'Shriram Finance'
        d.pop('UPL', None)
        return d
    elif dt < datetime(2025,3,28):
        d = get_nifty50_members(datetime(2024,9,30))
        d['BEL'] = 'Bharat Electronics'
        d['TRENT'] = 'Trent'
        d.pop('DIVISLAB', None)
        d.pop('LTIM', None)
        return d
    else:
        d = get_nifty50_members(datetime(2024,9,30))
        d['ETERNAL'] = 'Eternal Ltd'
        d['JIOFIN'] = 'Jio Financial Services'
        d.pop('BPCL', None)
        return d

# --- 2. Sentiment Analyzer --- #
analyzer = SentimentIntensityAnalyzer()

# --- 3. News Scraping by Dynamic Window --- #
start_date = datetime(2017, 1, 1)
end_date = datetime(2025, 1, 1)
delta = timedelta(days=7)  # Weekly bins

all_news = []
curr_date = start_date

while curr_date < end_date:
    next_date = curr_date + delta
    companies_in_window = get_nifty50_members(curr_date)
    for symbol, keyword in companies_in_window.items():
        print(f"▶ Scraping {symbol} ({keyword}) • {curr_date.date()} to {next_date.date()}", flush=True)
        query = f"{keyword} after:{curr_date.strftime('%Y-%m-%d')} before:{next_date.strftime('%Y-%m-%d')}"
        encoded_query = quote(query)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            if hasattr(entry, 'published_parsed'):
                pub_date = datetime(*entry.published_parsed[:6]).date()
                title = ' '.join(entry.title.strip().split())
                vad = analyzer.polarity_scores(title)
                all_news.append({
                    'date': pub_date,
                    'stock': symbol,
                    'title': title,
                    'link': entry.link.strip(),
                    'compound': vad['compound'],
                    'pos': vad['pos'],
                    'neu': vad['neu'],
                    'neg': vad['neg']
                })
    curr_date = next_date
    time.sleep(1)  # Rate-limiting protection

# --- 4. Save Results --- #
df_news = pd.DataFrame(all_news)
df_news.sort_values(by='date', inplace=True)
df_news.to_csv('nifty50_google_rss_sentiment_2017_2025.csv', index=False)
print(f"\n✅ News sentiment scraping completed. Headlines collected: {len(df_news)}")
