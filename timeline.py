from webbrowser import get
import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
#bearer_token = os.environ.get("BEARER_TOKEN")
bearer_token = "AAAAAAAAAAAAAAAAAAAAAN6ubQEAAAAAsskOd3YAHJYaqf666eJGJmraaM0%3DLGe7PDtgFvFfqdWubiMNnfs9H1Nr1KpJuyZ9khmbQgFLlEbW5l"


def create_url(id):
    # Replace with user ID below
    user_id = id
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at", "max_results": 100}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_data(id):
    timeline = get_timeline(id)
    tweets = tweets_separately(timeline)
    retweets = retweets_separately(timeline)
    return [timeline, tweets, retweets]

def get_timeline(id):
    url = create_url(id)
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    #print(json.dumps(json_response, indent=4, sort_keys=True))
    return json_response

def tweets_separately(timeline):
    #get the timeline json, filter each text for whether there is RT @ in the start, put all the ones that don't have it into separate list
    json_response = timeline
    timeline = json_response['data']

    #print(json_response['data'][0]['text'][0:5])
    tweets_iterator = filter(is_tweet, timeline)
    tweets = list(tweets_iterator)

    return tweets
   # print(json_response['data'][0])

def retweets_separately(timeline):
    #get the timeline json, filter each text for whether there is RT @ in the start, put all the ones that don't have it into separate list
    json_response = timeline
    timeline = json_response['data']

    #print(json_response['data'][0]['text'][0:5])
    retweets_iterator = filter(is_retweet, timeline)
    retweets = list(retweets_iterator)

    return retweets

def is_tweet(tweet):
    first_five = tweet['text'][0:4]
    if first_five == "RT @":
        return False
    else:
        return True

def is_retweet(tweet):
    first_five = tweet['text'][0:4]
    if first_five == "RT @":
        return True
    else:
        return False
       


if __name__ == "__main__":
    get_data()