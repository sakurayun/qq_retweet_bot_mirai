#coding:utf-8
import requests
import tweepy
import json as js
import os
import sys
from urllib.parse import quote
import json as js
import requests
import urllib
import time
import datetime
from datetime import datetime
from datetime import timedelta

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

retweet_group = 'RAS'

def get_session(qq='',addr='http://127.0.0.1:11451'):
    global qq,addr
    #Setup tunnel
    response = requests.get(addr+'/about')
    print('Version Info:\n'+str(response.text)+'\n\n')
    body = '{"authKey":"input_ur_authKey_here"}'
    response2 = requests.post(url=addr+'/auth',data=body)
    print('Status Code: '+str(response2.status_code)+'\n\n')

    #Gather session
    r2t=response2.text
    if r2t[8] == '0':
        session = r2t[21:-2]
        global session
        print('Session Code: '+str(session))
    else:
        print(r2t[8])

    #Verify session
    body_session = '{"sessionKey":"'+session+'","qq":"'+qq+'"}'
    global body_session
    response3 = requests.post(url=addr+'/verify',data=body_session)
    print('\n\n')
    r3t=response3.text
    if r3t[8] == '0':
        print('Successfully Initialized Retweet API!')
    else:
        print('Failed!')
    return session

def release_session():
    response = requests.post(url=addr+'/release',data=body_session)
    rt=response.text
    if rt[8] == '0':
        print('Successfully Released Session ID!')
    else:
        print('Failed!')
    return


def send_group_mirai(qq_group_id,datatobesent):
    body_tobesent = '{"sessionKey":"'+ session + '","target": ' + qq_group_id + ''',"messageChain":[{"type": "Plain", "text":"''' + datatobesent + '"}]}'
    response4 = requests.post(url=addr+'/sendGroupMessage',data=body_tobesent)
    r4t=response4.text
    print(r4t)


def analysis_time(retweet_time):
	offset_hours = 8                            
	local_timestamp = retweet_time + timedelta(hours=offset_hours)
	final_timestamp = datetime.strftime(local_timestamp,'%m.%d %H:%M:%S')
	return final_timestamp

def send_qqgroup_message(retweet_time,tweet_data,actual_name,qq_group_id,reply_user_name,reply_text,rt_tweet_text,rt_user,repeat):
	message_format = '#'+actual_name+'# '+retweet_time+'\n\n'
	original_tweet_data=tweet_data
	if repeat == '0':
		original_tweet_data=tweet_data + '\n----\n' + tweet_data
	elif repeat =='1':
		original_tweet_data = tweet_data
	if reply_user_name != 'NULL':
		tweet_data=message_format + original_tweet_data +'\n\n回复 #'+reply_user_name+'#\n\n'+reply_text
	elif rt_user !='':
		tweet_data=message_format + original_tweet_data +'\n\n转发 #'+rt_user+'#\n\n'+rt_tweet_text
	else:
		tweet_data=message_format + original_tweet_data
	tweet_data=quote(tweet_data)
#	urllib.request.urlopen('http://127.0.0.1:5700/send_group_msg?group_id='+ str(qq_group_id) + '&message='+ tweet_data)
    send_group_mirai(tweet_data)

def send_picture(qq_group_id,url):
#	url=quote("[CQ:image,file="+url+"]")
#	urllib.request.urlopen('http://127.0.0.1:5700/send_group_msg?group_id='+ str(qq_group_id) + '&message='+ url)
    image_tobesent = '{"sessionKey":"'+ session + '","group": ' + qq_group_id + ''',"urls":["''' + url + '"]}'
    response5 = requests.post(url=addr+'/sendImageMessage',data=image_tobesent)
    r5t=response5.text
    print(r5t)
    return
    
def recog_tag(tags_data,match_tag):
	for single_tag in tags_data:
		for single_match_tag in match_tag:
			if single_match_tag == single_tag['text']:
				tags = 0
			else:
				tags = 1
	return tags

def analysis_screen_name(screen_name):
	user=api.get_user(screen_name)
	name=user.name
	return name

def readfile(txtname):
    last_id = 0
    if not os.path.exists(txtname):
        fileread=open(txtname,"a+")
        fileread.close()
    else:
        fileread=open(txtname,"r")
        for i in fileread.readlines():
            print(i)
            if i is not '':
                last_id = int(i)
            fileread.close()
    return last_id

def writefile(txtname,last_id):
	filewrite=open(txtname,"w+")
	filewrite.writelines(str(last_id))
	filewrite.close()

def get_in_reply_tweet(in_reply_id):
    status=api.get_status(in_reply_id,tweet_mode='extended')
    return status.full_text

def send_tweet(new_tweets,actual_name,qq_group_id,tags,reply_user_name,last_id,match_tag,repeat,with_picture):
    tags=0
    for status in reversed(new_tweets):
        try:
            media = status.extended_entities.get('media',[])
        except:
            media = ''
        try:
            tags_data = status.entities.get('hashtags',[])
            tags = recog_tag(tags_data,match_tag)
        except:
            tags = 1
        try:
            reply_user_screen_name = status.in_reply_to_screen_name
            reply_user_name = analysis_screen_name(reply_user_screen_name)
        except:
            reply_user_name = 'NULL'
        try:
            tags_data = status.entities.get('hashtags',[])
            tags = recog_tag(tags_data,match_tag)
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
            send_qqgroup_message(retweet_time,retweet_text,actual_name,qq_group_id,reply_user_name,reply_text,rt_tweet_text,rt_user,repeat)
            print('推文发送成功')
            mu=[m['media_url'] for m in media]
            for n in mu:
                if media != '' and with_picture == 1:
                    send_picture(qq_group_id,n)
                    print('图片发送成功，Image URL: '+n)
    return last_id

def retweet(screen_name,actual_name,qq_group_id,match_tag,repeat,with_picture):
	txtname = retweet_group + '_' + screen_name + '_tweet_ids.txt'
	tags=0
	reply_user_name='NULL'
	last_id=readfile(txtname)
	if last_id==0:
		new_tweets=api.user_timeline(screen_name=screen_name,count = 1,tweet_mode='extended',include_rts='false',include_entities=True)
		last_id=send_tweet(new_tweets,actual_name,qq_group_id,tags,reply_user_name,last_id,match_tag,repeat,with_picture)
		writefile(txtname,last_id)
	else:
		new_tweets=api.user_timeline(screen_name=screen_name,since_id = last_id,include_rts='false',tweet_mode='extended',include_entities=True)
		last_id=send_tweet(new_tweets,actual_name,qq_group_id,tags,reply_user_name,last_id,match_tag,repeat,with_picture)
		writefile(txtname,last_id)




#get_session()

#retweet('screen_name','测试',00000000,['test'],0,1)
#retweet('screen_name','twitter_user's_real_name',qq_group_id,['tag'] or 0(no tag recognization),0(repeat) or 1(not_repeat),0(with_picture) or 1(without_picture))

#release_session()
exit(0)

