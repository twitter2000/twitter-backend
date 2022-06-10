from sys import maxsize
import requests
import tweepy
import json
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


# analyze sentiment by calculating the polarity scores
def Myanalyzer(s1):
    vs = analyzer.polarity_scores(s1)
#   print("{}… {}".format(s1[:30], str(vs)))
    return vs

    # anlayze each tweets and store in a list(result_list)


def processed_data(tweets):
    result_list = {}
    for s1 in tweets:
        result = Myanalyzer(s1)
        result_list['comment'] = s1
    result_list['compound'] = result['compound']

    return result_list


def tweet_analysis_model(json_response):
    # collecting tweets(in list form) from json module
    result = []
    stats = {}
    tweets = []
    tweet_ids = []
    for i in range(99):
        tweets.append(json_response['data'][i]['text'])
        tweet_ids.append(f"id:{(json_response['data'][i]['id'])}")
        # import sentiment analyze
        result.append(processed_data(tweets))

    tweetdf = pd.DataFrame(result)
    print('tweetdf', tweetdf['compound'].tolist())
    stats['mean'] = tweetdf.mean().to_list()[0]
    stats['max_'] = tweetdf['compound'].max()
    stats['min_'] = tweetdf['compound'].min()
    stats['tweets'] = tweet_ids
    # result.append(stats)
    return result, stats


def search_twitter(query, tweet_fields, bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&max_results=100".format(
        query, tweet_fields
    )
    response = requests.request("GET", url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def twitter_analyzer(query):
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAADP2YQEAAAAA%2BLsU1upRGdchco9gP8KzWzM%2BhzE%3DWKFqfAV7PONFRSBINRkJXTyKqxIV4lHOVdvxHoa6WDp3fBzxNw'
    consumer_key = "ksQQWDulv88zcSNDNzxbSbcQr"
    consumer_secret = "irDXc6Ss7XNgTfKc6Psnmh9x7F6THy6HIyB7ozxgk28nBa17GS"
    access_token_key = "1228318711569735681-FAmltyMwORCokftBHniYckcXYt6ZxO"
    access_token_secret = "6YKekRIZbEu4VcjkbAWdTb5pmStkejPdT7sUECzwwKwYp"
    client = tweepy.Client(bearer_token)

    # twitter fields to be returned by api call
    tweet_fields = "tweet.fields=text,author_id,created_at"

    # twitter api call
    json_response = search_twitter(
        query=query, tweet_fields=tweet_fields, bearer_token=bearer_token)
    # pretty printing
    return tweet_analysis_model(json_response)
