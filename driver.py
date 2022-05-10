from webbrowser import get
#import requests
#import os
import json


from user_info import get_data as get_data_userinfo
from followers import get_data as get_data_followers
from following import get_data as get_data_following
from timeline import get_data as get_data_timeline


def main():
    username = "espn"
    user_info = get_data_userinfo(username)
    #print(user_info)
    user_id = user_info['data'][0]['id']

    followers = get_data_followers(user_id)
    following = get_data_following(user_id)

    timeline_data = get_data_timeline(user_id)
    timeline = timeline_data[0]
    tweets = timeline_data[1]
    retweets = timeline_data[2]

    result = {}
    result['user_id'] = user_id
    result['user_metrics'] = user_info['data'][0]['public_metrics']

   #print(followers)
    result['followers'] = followers['data']
    result['following'] = following['data']
    result['tweets'] = tweets
    result['retweets'] = retweets
    result['timeline'] = timeline['data']

    print(json.dumps(result, indent=4, sort_keys=True))





if __name__ == "__main__":
    main()

