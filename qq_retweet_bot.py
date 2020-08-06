# coding=utf-8
'''
Credits:
xiofan2[xiofan2/qq_retweet_bot]
anrio[Modifications/Suggestions]
'''

import requests
import tweepy
import json as js
import os
import sys
from urllib.parse import quote
import urllib.request
import json as js
import requests
import urllib
import time
import datetime
from datetime import datetime
from datetime import timedelta


#Enter your keys
consumer_key = ''
consumer_secret = ''
access_token = '-'
access_token_secret = ''
retweet_group = 'Inari'
addr = 'http://localhost:11451'
#Process keys
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_session(qq='550463623'):
    global body_session, session
    # Setup tunnel
    response = requests.get(addr + '/about')
    rt1=str(response.text)
    ver = rt1[-9:-3]
    print('Mirai-Api-HTTP Version: ' + ver + '\n')
    body = '{"authKey":"1145141919810"}'
    response2 = requests.post(url=addr + '/auth', data=body)
    print('HTTP Status Code: ' + str(response2.status_code) + '\n')
    # Gather session
    r2t = response2.text
    if r2t[8] == '0':
        session = r2t[21:-2]
        print('Session Code: ' + str(session) + '\n')
    else:
        print(r2t[8])
    # Verify session
    body_session = '{"sessionKey":"' + session + '","qq":"' + qq + '"}'
    response3 = requests.post(url=addr + '/verify', data=body_session)
    r3t = response3.text
    if r3t[8] == '0':
        print('Successfully connected to Mirai-Api-HTTP server!\n')
    else:
        print('Failed!')
        print(r3t)
    return session


def release_session():
#Session keys need to be released immediately everytime you finish the process
    response = requests.post(url=addr + '/release', data=body_session)
    rt = response.text
    if rt[8] == '0':
        print('\nSuccessfully Released Session ID!')
    else:
        print('Failed!')
    return 0


def send_group_mirai(datatobesent, qq_group_id):
    body_tobesent = '{"sessionKey":"' + session + '","target": ' + str(
        qq_group_id) + ''',"messageChain":[{"type": "Plain", "text":"''' + datatobesent + '"}]}'
    response4 = requests.post(url=addr + '/sendGroupMessage', data=body_tobesent.encode('utf-8'))
    r4t = response4.text
    print(r4t)
    return 0


def analysis_time(retweet_time):
    offset_hours = 8
    local_timestamp = retweet_time + timedelta(hours=offset_hours)
    final_timestamp = datetime.strftime(local_timestamp, '%m.%d %H:%M:%S')
    return final_timestamp


def send_qqgroup_message(retweet_time, tweet_data, actual_name, qq_group_id, reply_user_name, reply_text, rt_tweet_text,
                         rt_user, repeat):
    # str(retweet_time,actual_name)
    message_format = '🌹' + actual_name + '🌹 于' + retweet_time + '更新了推文\n\n'
    original_tweet_data = tweet_data
    if repeat == '0':
        original_tweet_data = tweet_data + '\n----\n' + tweet_data
    elif repeat == '1':
        original_tweet_data = tweet_data
    if reply_user_name != 'NULL':
        tweet_data = message_format + original_tweet_data + '\n\n回复 #' + reply_user_name + '#\n\n' + reply_text
    elif rt_user != '':
        tweet_data = message_format + original_tweet_data + '\n\n转发 #' + rt_user + '#\n\n' + rt_tweet_text
    else:
        tweet_data = message_format + original_tweet_data
    #	tweet_data=tweet_data.encode('utf-8')
    print(tweet_data)
    #	urllib.request.urlopen('http://127.0.0.1:5700/send_group_msg?group_id='+ str(qq_group_id) + '&message='+ tweet_data)
    send_group_mirai(tweet_data, qq_group_id)
    return


def send_picture(qq_group_id, url):
    #	url=quote("[CQ:image,file="+url+"]")
    #	urllib.request.urlopen('http://127.0.0.1:5700/send_group_msg?group_id='+ str(qq_group_id) + '&message='+ url)
    image_tobesent = '{"sessionKey":"' + session + '","group": ' + str(qq_group_id) + ''',"urls":["''' + url + '"]}'
    response5 = requests.post(url=addr + '/sendImageMessage', data=image_tobesent)
    r5t = response5.text
    print(r5t)
    return


def recog_tag(tags_data, match_tag):
    for single_tag in tags_data:
        for single_match_tag in match_tag:
            if single_match_tag == single_tag['text']:
                tags = 0
            else:
                tags = 1
    return tags


def analysis_screen_name(screen_name):
    user = api.get_user(screen_name)
    name = user.name
    return name


def readfile(txtname):
    last_id = 0
    if not os.path.exists(txtname):
        fileread = open(txtname, "a+")
        fileread.close()
    else:
        fileread = open(txtname, "r")
        for i in fileread.readlines():
            print('Processed: '+i)
            if i is not '':
                last_id = int(i)
            fileread.close()
    return last_id


def writefile(txtname, last_id):
    filewrite = open(txtname, "w+")
    filewrite.writelines(str(last_id))
    filewrite.close()


def get_in_reply_tweet(in_reply_id):
    status = api.get_status(in_reply_id, tweet_mode='extended')
    return status.full_text


def send_tweet(new_tweets, actual_name, qq_group_id, tags, reply_user_name, last_id, match_tag, repeat, with_picture):
    tags = 0
    for status in reversed(new_tweets):
        try:
            media = status.extended_entities.get('media', [])
        except:
            media = ''
        try:
            tags_data = status.entities.get('hashtags', [])
            tags = recog_tag(tags_data, match_tag)
        except:
            tags = 1
        try:
            reply_user_screen_name = status.in_reply_to_screen_name
            reply_user_name = analysis_screen_name(reply_user_screen_name)
        except:
            reply_user_name = 'NULL'
        try:
            tags_data = status.entities.get('hashtags', [])
            tags = recog_tag(tags_data, match_tag)
        except:
            tags = 1
        try:
            in_reply_id = status.in_reply_to_status_id
            reply_text = get_in_reply_tweet(in_reply_id)
        except:
            reply_text = ''

        try:
            rt_tweet_text = status.quoted_status.full_text
            rt_user = status.quoted_status.user.name

        except:
            rt_tweet_text = ''
            rt_user = ''

        retweet_text = status.full_text
        retweet_time = analysis_time(status.created_at)
        if last_id == 0:
            last_id = status.id
        elif status.id > last_id:
            last_id = status.id
        if tags == 0 or match_tag == 0:
            send_qqgroup_message(retweet_time, retweet_text, actual_name, qq_group_id, reply_user_name, reply_text,
                                 rt_tweet_text, rt_user, repeat)
            print('Retweet successed!')
            mu = [m['media_url'] for m in media]
            for n in mu:
                if media != '' and with_picture == 1:
                    send_picture(qq_group_id, n)
                    print('Send image successed! Image URL: ' + n)
    return last_id


def retweet(screen_name, actual_name, qq_group_id, match_tag, repeat, with_picture):
    # actual_name=actual_name.encode("utf-8").decode("latin1")
    txtname = retweet_group + '_' + screen_name + '_tweet_ids.txt'
    tags = 0
    reply_user_name = 'NULL'
    last_id = readfile(txtname)
    if last_id == 0:
        new_tweets = api.user_timeline(screen_name=screen_name, count=1, tweet_mode='extended', include_rts='false',
                                       include_entities=True)
        last_id = send_tweet(new_tweets, actual_name, qq_group_id, tags, reply_user_name, last_id, match_tag, repeat,
                             with_picture)
        writefile(txtname, last_id)
    else:
        new_tweets = api.user_timeline(screen_name=screen_name, since_id=last_id, include_rts='false',
                                       tweet_mode='extended', include_entities=True)
        last_id = send_tweet(new_tweets, actual_name, qq_group_id, tags, reply_user_name, last_id, match_tag, repeat,
                             with_picture)
        writefile(txtname, last_id)

#main
get_session()

#Enter your configs here
# retweet('screen_name','twitter_user's_real_name',qq_group_id,['tag'] or 0(no tag recognization),0(repeat) or 1(not_repeat),0(with_picture) or 1(without_picture))

# xapenny
retweet('xapenny2015', 'xapenny', 884169045, 0, 0, 1)
# iOS讨论
retweet('CStar_OW', 'CoolStar', 567435967, 0, 0, 1)
retweet('nsimayu', '新岛夕', 567435967, 0, 0, 1)
retweet('unc0verTeam', 'unc0ver Team', 567435967, 0, 0, 1)
retweet('checkra1n', 'checkra1n', 567435967, 0, 0, 1)
retweet('axi0mX','axi0mX',567435967,0,0,1)
retweet('CharizTeam','Chariz Repository',567435967,0,0,1)
retweet('keen_lab','KEENLAB',567435967,0,0,1)
retweet('GetSileo','Sileo',567435967,0,0,1)
retweet('packixrepo','Packix Repository',567435967,0,0,1)
retweet('Pwn20wnd','@Pwn20wnd',567435967,0,0,1)
retweet('CorelliumHQ','Corellium',567435967,0,0,1)
retweet('electra_team','Electra Team',567435967,0,0,1)
retweet('i41nbeer','Ian Beer',567435967,0,0,1)
retweet('coolbooter','CoolBooter',567435967,0,0,1)
retweet('tihmstar','tihmstar',567435967,0,0,1)
retweet('Apple','Apple',567435967,0,0,1)
retweet('qwertyoruiopz','qwertyoruiop',567435967,0,0,1)
retweet('tim_cook','Tim Cook',567435967,0,0,1)
retweet('PanguTeam','PanguTeam',567435967,0,0,1)

release_session()

exit(0)
