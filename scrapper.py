import datetime 
import requests
from bs4 import BeautifulSoup
import time
import tweepy
import os
import pytz
from os import environ


time_to_execute = ['08:00', '20:00']

while True:
    print("retrieving news...")
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.datetime.now(IST)
    current_time = datetime_ist.strftime("%H:%M")
    print(current_time)
    if current_time in time_to_execute:
        print(f"\nAt {current_time}")

        consumer_key = environ['consumer_key']
        consumer_secret_key = environ['consumer_secret_key']
        access_token = environ['access_token']
        access_token_secret = environ['access_token_secret']

        #authenticating to access the twitter API
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        url = 'https://techcrunch.com/'
        response = requests.get(url)
        results = BeautifulSoup(response.text, 'html.parser')


        def tweet_image(url, message, link, time, i):
            filename = 'temp.jpg'   
            request = requests.get(url, stream=True)
            if request.status_code == 200:
                with open(filename, 'wb') as image:
                    for chunk in request:
                        image.write(chunk)

                api.update_with_media(filename, status = str(i) + "." + message + ".\n\n" + time + "\n\n--" + link)
                os.remove(filename)
            else:
                print("Unable to download image")

        articles = results.find_all('div', class_ = 'post-block post-block--image post-block--unread')
        # print(articles)
        all_articles = []

        for article in articles:

            dict_article = {}
            headline = article.find('h2')   
            if headline:    
                dict_article['headline'] = headline.text.strip()
                # print(headline.text)
            link = article.find('h2').find('a')
            if link:
                dict_article['link'] = link['href']
                # print(link)
            summary = article.find('div', class_ = 'post-block__content')
            if summary:
                dict_article['summary'] = summary.text
                # print(type(dict_article['summary']))
                # print(summary.text)
            image = article.find('img')
            if image:
                dict_article['image'] = image['src']
                # print(image['src'])

            

            dict_article['updated_time'] = (datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%m')
            # print(dict_article['updated_time'])

            all_articles.append(dict_article)

        i = 1
        for article in all_articles:
            content = article['headline']
            content_image = article['image']
            content_url = article['link']
            content_summary = dict_article['summary']
            content_time = dict_article['updated_time']
            print("tweeting...")
            tweet_image(content_image, content, content_url, content_time, i)
            time.sleep(15)
            i += 1
            if i == 7:
                break