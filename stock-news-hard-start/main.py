import requests
from twilio.rest import Client
import os


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
account_sid = "AC2aa8b84eb0d70d00cbbe48c4e84237b0"
auth_token = os.environ.get('TWILIO_Key')

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
stock_parameters = {
    "function" : "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": os.environ.get('Stock_API_Key')
}


NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_parameters = {
    "qInTitle" : COMPANY_NAME,
    "apiKey" : os.environ.get('News_API_Key'),

}



stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
# print(stock_response.raise_for_status())
stock_data = stock_response.json()
daily_prices = stock_data['Time Series (Daily)']
data_list = [value for (key,value) in daily_prices.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']
print(yesterday_closing_price)
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data['4. close']
print(day_before_yesterday_closing_price)
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down ="🔻"
diff_percentage = round((difference/float(yesterday_closing_price)) *100)
print(diff_percentage)


if abs(diff_percentage) > 0:
    response = requests.get(NEWS_ENDPOINT,params=news_parameters)
    news_data = response.json()
    three_articles =news_data['articles'][:3]
    print(three_articles)



client = Client(account_sid, auth_token)
for num in range(0,3):
    message = client.messages.create(
            body=f"TSLA: {up_down}{abs(diff_percentage)}%\nHeadline: {three_articles[num]['title']}\nBrief: {three_articles[num]['description']}",
            from_="+1xxxxxxxxx",
            to=os.environ.get('My_Phone_Num')
)


#The SMS message format will be like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


