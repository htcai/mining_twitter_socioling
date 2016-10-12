import twitter
import json
from datetime import datetime
import time
from dateutil.parser import parse
from urllib2 import URLError
import pytz
import io

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

print twitter_api


utc=pytz.UTC
null = 'null'
true = True
false = False
privacy = '000000000000000'

def de_emp(lst):
    lng = len(lst)
    if lst[lng-1] == '':
        del lst[lng-1]


# avoid the double-retrieval of a single tweet
def de_overlap(diction):
    maxid = int(diction["max_id"]) - 1
    diction["max_id"] = str(maxid)
    return diction


def read_txt(path):
    f = open(path, 'r')
    strs = f.read().split('\n')
    de_emp(strs)
    etts = [eval(ett) for ett in strs]
    return etts


path_ts = '/rate_control/timeline_ts.txt'
f_tl = open(path_ts, 'r')
f_list = f_tl.read().split('\n')
de_emp(f_list)
tl_control = [parse(item) for item in f_list]
f_tl.close()


def tl_rate_control():
    delta = datetime.now() - tl_control[0]
    wait_seconds = 60 * 15 + 2 - delta.total_seconds()
    if wait_seconds > 0:
        print 'will wait', wait_seconds
        time.sleep(wait_seconds)
    del tl_control[0]
    tl_control.append(datetime.now())
    f_tl = open(path_ts, 'w')
    for ts in tl_control:
        f_tl.write(str(ts) + '\n')
    f_tl.close()


def store_tweets(tweets, following, usr_id):
    path_file = ''
    with io.open(format(path_file), 'a', encoding='utf-8') as f_tweets:
        for tweet in tweets:
            f_tweets.write(unicode(json.dumps(tweet, ensure_ascii=False))+'\n')


begin = utc.localize(datetime(, , ))


def tts_old(tts):
    num = len(tts)
    tt = tts[num-1]
    found = parse(tt['created_at']) < begin
    return found


def harvest_timeline(user):
    usr_id = user['id_str']
    sts_count = int(user['statuses_count'])
    kw = {
        'count': 200,
        'trim_user': 'false',
        'include_rts': 'true',
        'since_id': 1,
        'user_id': usr_id
        }    
    tl_rate_control()    
    no_tts = False
    try:
        page_num = 1
        tweets = twitter_api.statuses.user_timeline(**kw)
    except twitter.api.TwitterHTTPError, e:
        print 'HTTP Error' + str(e.e.code) + str(datetime.now())
        
        if e.e.code == 401 or e.e.code == 404:
            tweets = None
            page_num = 17

        if e.e.code == 429:
            time.sleep(60*15+2)
        
        if e.e.code in (500, 502, 503, 504):
            time.sleep(300)
    except URLError, e:
        print 'URL Error' + str(e.e.code) + str(datetime.now())
        time.sleep(300)
    
    if tweets is None:
        tweets = []
        page_num = 17
        no_tts = True
    else:      
        store_tweets(tweets, usr_id)
    max_pages = min(16, sts_count/200 + 1)

    while not tts_old(tweets) and page_num < max_pages and len(tweets) > 0:
        kw['max_id'] = min([tweet['id'] for tweet in tweets]) - 1
        tl_rate_control()        
        try:
            tweets = twitter_api.statuses.user_timeline(**kw)
            page_num += 1
            store_tweets(tweets, usr_id)
        except twitter.api.TwitterHTTPError, e:
            print 'HTTP Error' + str(e.e.code) + str(datetime.now())
            if e.e.code in (429, 500, 502, 503, 504):
                time.sleep(302)
    
    f = open('', 'a')
    if no_tts == True:
        usr_id = str(usr_id) + privacy
    else:
        print len(harvested_ids), 'Harvested ' + usr_id + str(datetime.now())
    f.write(str(usr_id) + '\n')
    f.close()
    harvested_ids.append(usr_id)


try:
    path_h = ''
    ids = read_txt(path_h)
    harvested_ids = [str(user_id) for user_id in ids]
except IOError, e:
    harvested_ids = []

#proper_ids = [user_id for user_id in harvested_ids if privacy not in user_id]


def process(subjs):
    global proper_ids
    for user in subjs:
        usr = user['id_str']
        if usr not in harvested_ids and usr+privacy not in harvested_ids:
            harvest_timeline(user)


path_authors = ''
authors = read_txt(path_authors)
process(authors)





    
