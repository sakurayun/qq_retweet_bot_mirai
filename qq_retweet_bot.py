#coding:utf-8
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

consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

retweet_group = '组名'

def analysis_time(retweet_time):
	offset_hours = 8                         
	local_timestamp = retweet_time + timedelta(hours=offset_hours)
	final_timestamp = datetime.strftime(local_timestamp,'%m.%d %H:%M:%S')
	return final_timestamp

def send_qqgroup_message(retweet_time,tweet_data,actual_name,qq_group_id):
	message_format = '＃' + actual_name +'＃' + retweet_time +'\n\n'
	tweet_data = message_format + tweet_data + '\n\n———\n\n' + tweet_data
	tweet_data=quote(tweet_data)
	urllib.request.urlopen('http://127.0.0.1:5700/send_group_msg?group_id='+ str(qq_group_id) + '&message='+ tweet_data)

def send_picture(qq_group_id,url):
	url=quote("[CQ:image,file="+url+"]")
	urllib.request.urlopen('http://127.0.0.1:5700/send_group_msg?group_id='+ str(qq_group_id) + '&message='+ url)

def recog_tag(tags_data,match_tag):
	for single_tag in tags_data:
		for single_match_tag in match_tag:
			if single_match_tag == single_tag['text']:
				tags = 0
			else:
				tags = 1
	return tags

def retweet(screen_name,actual_name,qq_group_id,match_tag):
	txtname = retweet_group + '_' + screen_name + '_tweet_ids.txt'
	tweets=[]
	last_id = 0
	tags=0
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
	if last_id==0:
		new_tweets=api.user_timeline(screen_name=screen_name,count = 1,tweet_mode='extended',include_rts='false',include_entities=True)
		for tweet in new_tweets:
			try:
				media = tweet.extended_entities.get('media',[])
			except:
				media =''
			retweet_text = tweet.full_text
			last_id = tweet.id
			retweet_time = analysis_time(tweet.created_at)
			try:
				tags_data = tweet.entities.get('hashtags',[])
				tags = recog_tag(tags_data,match_tag)
			except:
				tags = 1
			if tags == 0 or match_tag ==0:
				send_qqgroup_message(retweet_time,retweet_text,actual_name,qq_group_id)
				print('推文发送成功')
				mu=[m['media_url'] for m in media]
				for n in mu:
					if media != '':
						send_picture(qq_group_id,n)
						print('Tweet id: '+n)

		filewrite=open(txtname,"w+")
		filewrite.writelines(str(last_id))
		filewrite.close()
	else:
		new_tweets=tweepy.Cursor(api.user_timeline,screen_name=screen_name,since_id = last_id,include_rts='false',tweet_mode='extended',include_entities=True).items()
		for status in new_tweets:
			try:
				media = status.extended_entities.get('media',[])
			except:
				media = ''
			try:
				tags_data = status.entities.get('hashtags',[])
				tags = recog_tag(tags_data,match_tag)
			except:
				tags = 1
			tweets.append({
			    'text': status.full_text,
				'tweet_id':status.id,
				'tweet_time':status.created_at,
				'tweet_media':[m['media_url'] for m in media]
				})
		for tweet in reversed(tweets):
			retweet_text=tweet['text']
			retweet_time = analysis_time(tweet['tweet_time'])
			if tags == 0 or match_tag == 0:
				send_qqgroup_message(retweet_time,retweet_text,actual_name,qq_group_id)
				print('推文发送成功')
				for n in tweet['tweet_media']:
					if media != '':
						send_picture(qq_group_id,n)
						print('图片发送成功')
			if tweet['tweet_id'] > last_id:
				last_id = tweet['tweet_id']
		fileread=open(txtname,"w+")
		fileread.writelines(str(last_id))
		fileread.close()

retweet('screen_name','测试',00000000,['test'])
retweet('screen_name','测试',00000000,0)
exit(0)

