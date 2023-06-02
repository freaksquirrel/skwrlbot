# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import sys
import subprocess
import os, time
import re
import imghdr
from twython import Twython
from twython import exceptions as TwythonExceptions
import sb_authinfo_twitter as sbauth
import sb_iofiles as sbio

## Exceptions
# TwythonError  -> Generic error class, catch-all for most Twython issues.
# TwythonAuthError   -> Raised when you try to access a protected resource and it fails due to some issue with your authentication.
# TwythonRateLimitError   -> Raised when you've hit a rate limit.
    
class TwitterInterface:

    tweet_max_len = 270

    #class constructor
    def __init__(self, debuginfo = False):
        self.debuginfo = debuginfo
        self.api = Twython( sbauth.TWITTER_APP_KEY,sbauth.TWITTER_APP_SECRET, sbauth.TWITTER_OAUTH_TOKEN, sbauth.TWITTER_OAUTH_TOKEN_SECRET )
        try:
            self.credentials = self.api.verify_credentials()
            self.screen_name = self.credentials['screen_name']
            self.user_id = self.credentials['id']
        except TwythonExceptions.TwythonAuthError:
            self.credentials = False
            self.screen_name = ''
            self.user_id = ''
            if self.debuginfo: print("Authentication failed! check the authentication parameters and try again.")

    #get own timeline (in order to checkl the tweets of users the bot follows)
    def getTimeline(self):
        # grab the last ID that the bot replied to, so it doesn't reply to earlier posts. (spam prevention measure)
        latesttweet_id_log = os.path.join(sbio.timeline_mngt_path, f"{self.user_id}{sbio.tl_latest_tweet_id_fn}")
        if os.path.exists(latesttweet_id_log):
            fp = open(latesttweet_id_log)
            lastid = fp.read().strip()
            fp.close()
            if lastid == '':
                lastid = 0
        else:
            lastid = 0
                
        # Get timeline based on the lastest tweet ID collected
        if lastid == 0:
            timeline = self.api.get_home_timeline( count = 100, tweet_mode = 'extended')
            if self.debuginfo: print("got fresh timeline")
        else:
            timeline = self.api.get_home_timeline( since_id = lastid, count = 100, tweet_mode = 'extended')
            if self.debuginfo: print("got updated timeline")

        # update the timeline reference file
        if self.debuginfo: print(f"Collected {len(timeline)} new tweets from the bot's timeline")
        if len(timeline) > 0:
            fp = open(latesttweet_id_log, 'w')
            fp.write(str(max([x['id'] for x in timeline])))
            fp.close()

        return timeline

    #get a user timeline, with no replies or retweets by default  (will change this later)
    def getUserTimeline(self, user_screen_name = ''):
        user_timeline = False
        if user_screen_name:
            try:
                useracc = self.api.show_user(screen_name = user_screen_name)
                userid = useracc['id']
                if self.debuginfo: print(f"user found! -> screen_name='{user_screen_name}', ID='{userid}'")
            except TwythonExceptions.TwythonError:
                if self.debuginfo: print(f"user not found! -> {user_screen_name}")
                return user_timeline
            
            # grab the last ID that the bot collected from the specific user (spam prevention measure)           
            latesttweet_id_log = os.path.join(sbio.timeline_mngt_path, f"{userid}{sbio.tl_latest_tweet_id_fn}")
            if self.debuginfo: print(f"File for user: {latesttweet_id_log}")
            if os.path.exists(latesttweet_id_log):
                fp = open(latesttweet_id_log)
                lastid = fp.read().strip()
                fp.close()
                if lastid == '':
                    lastid = 0
            else:
                lastid = 0
                
            # Get timeline based on the lastest tweet ID collected
            if lastid == 0:
                #TODO: use userid instead?
                user_timeline = self.api.get_user_timeline(screen_name = user_screen_name, count = 100, exclude_replies = True, include_rts = False, tweet_mode = 'extended')
                if self.debuginfo: print(f"got fresh timeline of {user_screen_name}")
            else:
                #TODO: use userid instead?
                user_timeline = self.api.get_user_timeline(screen_name = user_screen_name, since_id = lastid, count = 100, exclude_replies = True, include_rts = False, tweet_mode = 'extended')
                if self.debuginfo: print(f"got updated timeline of {user_screen_name}")

            # update the timeline reference file
            if self.debuginfo: print(f"Collected {len(user_timeline)} new tweets from {user_screen_name}'s timeline")
            if len(user_timeline) > 0:
                fp = open(latesttweet_id_log, 'w')
                fp.write(str(max([x['id'] for x in user_timeline])))
                fp.close()

        return user_timeline

    #tweet only text...
    def tweetText(self, tweet_text = ''):
        tweet_res = False
        if tweet_text and len(tweet_text) < self.tweet_max_len:
            try:
                self.api.update_status(status = tweet_text)
                if self.debuginfo: print(f"Tweet: {tweet_text}\n")
                tweet_res = True
            except TwythonExceptions.TwythonRateLimitError:
                if self.debuginfo: print("WTF???? rate limit")
            except TwythonExceptions.TwythonError:
                if self.debuginfo: print("WTF???? error")
        else:
            if self.debuginfo: print(f"Not valid tweet!\n Lenght:{len(tweet_text)} \n Tweet:{tweet_text}\n")
    
        return tweet_res

    # up to 4 Image 5 MB, GIF 15 MB
    def tweetTextAndImage(self, tweet_text = '', image_path = '' ):
        tweet_res = False
        valid_img_types = {'jpeg','png','bmp'}
        valid_img_size = 5
        if image_path and tweet_text and len(tweet_text) < self.tweet_max_len:
            try:
                if not isinstance(image_path, list): image_path = [image_path]
                media_id_list = []
                for img_to_upload in image_path:
                    #check that the file is actually an image (also serves as file existance check using the exception)
                    img_type = imghdr.what(img_to_upload)
                    #get the file size in MB (also serves as file existance check using the exception)
                    img_size = os.stat(img_to_upload).st_size / 1024**2
                    #check if everything is in order before uploading to twitter server
                    if img_type in valid_img_types and img_size < valid_img_size:
                        if self.debuginfo: print(f"Will upload a {img_type} image of size {img_size}MB \n path:{img_to_upload}\n")
                        img_data = open(img_to_upload, 'rb')
                        response = self.api.upload_media(media = img_data)
                        time.sleep(2)
                        #check for media_id
                        if 'media_id' in response.keys() and response['media_id']:
                            if self.debuginfo: print(f"Uploaded image. ID:{response['media_id']}\n")
                            media_id_list.append(response['media_id'])
                        else:
                            if self.debuginfo: print(f"Media ID error... was not able to upload? file:{img_to_upload}")
                    else:
                        if self.debuginfo: print(f"Image type or size error... type: {img_type}, size: {img_size}MB")
                    if len(media_id_list) >= 4: break
                if media_id_list:
                    #Now try to add the text and attach the image(s)            
                    self.api.update_status( status = tweet_text, media_ids = media_id_list )
                    if self.debuginfo: print(f"Tweet with {len(media_id_list)} imgs : {tweet_text}\n")
                    tweet_res = True        
            except FileNotFoundError:
                if self.debuginfo: print(f"File not found: {img_to_upload}")
            except TwythonExceptions.TwythonRateLimitError:
                if self.debuginfo: print("WTF???? rate limit")
            except TwythonExceptions.TwythonError:
                if self.debuginfo: print("WTF???? error")
        else:
            if self.debuginfo: print(f"Not valid tweet!\n Lenght:{len(tweet_text)} \n Tweet:{tweet_text}\n")
    
        return tweet_res

    #time for patadas has come my friend... unleash the beast!
    def tweetPatadas(statusObj):
        repliedTo = []
        try:
            if os.path.exists(sbio.patadas_frases):
                frasespatadasfile = open(sbio.patadas_frases)
                patadas = frasespatadasfile.read().split('\n')
                frasespatadasfile.close()
                patadas = list(filter(len, patadas))
                patada = patadas[randint(0,len(patadas)-1)]
                
                if self.debuginfo: print(f"Posting in reply to @{statusObj['user']['screen_name'].encode('ascii', 'replace')}: {statusObj['full_text'].encode('ascii', 'replace')}" )
                self.api.update_status(status = f"@{statusObj['user']['screen_name']} {patada}", in_reply_to_status_id = statusObj['id'])
                repliedTo.append( (statusObj['id'], statusObj['user']['screen_name'], statusObj['full_text'].encode('ascii', 'replace')) )
                time.sleep(5)
                return repliedTo
            else:
                if self.debuginfo: print(f"Error: Frases file does not exists \n file: {sbio.patadas_frases}")
                return []
            
        except Exception:
            if self.debuginfo: print(f"Unexpected error: {sys.exc_info()[0:2]}")
            return []

    
    # implement "find and reply" actions for several hashtags... really just playing around with this
    #------------------------------------------------------------------------------------------------------------------------
    def _findhashtag(self, hashtag_s):
        #default = "Invalid/Not implemented"
        return getattr(self, 'findAndreply2' + str(hashtag_s), lambda: hashtagnotvalid)()

    def hashtagnotvalid(self):
        if self.debuginfo: print("Invalid/Not implemented")
        return "Invalid/Not implemented"
    
    def findAndreply2patadas(self):
        timeline = self.getTimeline()
        
        for status in timeline:
            #if re.findall('[#?]patadas\\b', status['full_text'].lower()) and status['user']['screen_name'].lower() not in sbauth.TWITTER_BOT_HANDLE:
            if re.findall('[#?]patadas\\b', status['full_text'].lower()) and status['user']['screen_name'].lower() not in self.screen_name:
                #apply patadas!!!!
                repliedTo = self.tweetPatadas(status)
                    
        if len(repliedTo) > 0:
            fp = open(sbio.hashtag_search_log, 'a')
            fp.write('\n'.join(['%s|%s|%s' % (x[0], x[1], x[2]) for x in repliedTo]) + '\n')
            fp.write('\n')
            fp.close()

    #def findAndreply2dramaqueen(self, arg):
    #    if self.debuginfo: print(f"you called findAndreply2dramaqueen({arg})")
    #    return "drama"

    #def findAndreply2galletas(self, arg):
    #    if self.debuginfo: print(f"you called findAndreply2galletas({arg})")
    #    return "galletas de animalitos"
 
# === END: twitter interface class === 
