# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import sys
import subprocess
import os, time
import re
import imghdr
from mastodon import Mastodon
from mastodon import MastodonUnauthorizedError, MastodonNotFoundError, MastodonAPIError
import sb_authinfo_mastodon as sbauth
import sb_iofiles as sbio


class MastodonInterface:

    post_max_len = 500
    
    #class constructor
    def __init__(self, debuginfo = False):
        self.debuginfo = debuginfo
        self.api = Mastodon( client_id = sbauth.MASTODON_CLIENT_ID, client_secret = sbauth.MASTODON_CLIENT_SECRET, access_token = sbauth.MASTODON_ACCESS_TOKEN , api_base_url = sbauth.MASTODON_API_BASE_URL )
        try:
            self.app_credentials = self.api.app_verify_credentials()
            self.app_name = self.app_credentials['name']
            self.credentials = self.api.account_verify_credentials()
            self.username = self.credentials['username']
            self.user_id = self.credentials['id']
        except MastodonUnauthorizedError:
            self.app_credentials = False
            self.app_name = ''
            self.credentials = False
            self.username = ''
            self.user_id = ''
            
            if self.debuginfo: print("Authentication failed! check the authentication parameters and try again.")

    #get own timeline (in order to checkl the tweets of users the bot follows)    
    def getTimeline(self):
        # grab the last ID that the bot replied to, so it doesn't reply to earlier posts. (spam prevention measure)
        latestpost_id_log = os.path.join(sbio.timeline_mngt_path, f"{self.user_id}{sbio.tl_latest_post_id_fn}")        
        if os.path.exists(latestpost_id_log):
            fp = open(latestpost_id_log)
            lastid = fp.read().strip()
            fp.close()
            if lastid == '':
                lastid = 0
        else:
            lastid = 0
                
        # Get timeline based on the lastest tweet ID collected
        if lastid == 0:
            timeline = self.api.timeline_home( limit = 100 )
            if self.debuginfo: print("got fresh timeline")
        else:
            timeline = self.api.timeline_home( since_id = lastid, limit = 100 )
            if self.debuginfo: print("got updated timeline")

        # update the timeline reference file
        if self.debuginfo: print(f"Collected {len(timeline)} new tweets from the bot's timeline")
        if len(timeline) > 0:
            fp = open(latestpost_id_log, 'w')
            fp.write(str(max([x['id'] for x in timeline])))
            fp.close()

        return timeline

    #get a user timeline, with no reblogs by default  (will change this later)
    #screenname needs to be full if the user is not on the same instance as the bot
    def getUserTimeline(self, user_screen_name = ''):
        user_timeline = False
        if user_screen_name:
            try:
                useracc = self.api.account_lookup( user_screen_name )
                userid = useracc['id']
                if self.debuginfo: print(f"user found! -> screen_name='{user_screen_name}', ID='{userid}'")
            except MastodonNotFoundError:
                if self.debuginfo: print(f"user not found! -> {user_screen_name}")
                return user_timeline
            
            # grab the last ID that the bot collected from the specific user (spam prevention measure)
            latestpost_id_log = os.path.join(sbio.timeline_mngt_path, f"{userid}_tl_latest_fetched_post_id.txt")
            if self.debuginfo: print(f"File for user: {latestpost_id_log}")
            if os.path.exists(latestpost_id_log):
                fp = open(latestpost_id_log)
                lastid = fp.read().strip()
                fp.close()
                if lastid == '':
                    lastid = 0
            else:
                lastid = 0
                
            # Get timeline based on the lastest tweet ID collected
            if lastid == 0:
                user_timeline = self.api.account_statuses( id = userid, exclude_reblogs = True, limit = 100 )
                if self.debuginfo: print(f"got fresh timeline of {user_screen_name}")
            else:
                user_timeline = self.api.account_statuses( id = userid, exclude_reblogs = True, since_id = lastid, limit = 100 )
                if self.debuginfo: print(f"got updated timeline of {user_screen_name}")

            # update the timeline reference file
            if self.debuginfo: print(f"Collected {len(user_timeline)} new tweets from {user_screen_name}'s timeline")
            if len(user_timeline) > 0:
                fp = open(latestpost_id_log, 'w')
                fp.write(str(max([x['id'] for x in user_timeline])))
                fp.close()

        return user_timeline

    #post only text...
    def postText( self, post_text = '' ):
        post_res = False
        if post_text and len(post_text) < self.post_max_len:
            # TODO: need to catch some exceptions here???
            self.api.status_post( status = post_text )
            post_res = True
            if self.debuginfo: print(f"Post: {post_text}\n")
        else:
            if self.debuginfo: print(f"Not valid post!\n Lenght:{len(post_text)} \n Tweet:{post_text}\n")
        
        return post_res

    
    # up to 4 images,  5 MB each
    def postTextAndImage(self, post_text = '', image_path = '' ):
        post_res = False
        valid_img_types = {'jpeg','png','bmp'}
        valid_img_size = 5
        if image_path and post_text and len(post_text) < self.post_max_len:
            try:
                if not isinstance(image_path, list): image_path = [image_path]
                media_id_list = []
                for img_to_upload in image_path:
                    #check that the file is actually an image (also serves as file existance check using the exception)
                    img_type = imghdr.what(img_to_upload)
                    #get the file size in MB (also serves as file existance check using the exception)
                    img_size = os.stat(img_to_upload).st_size / 1024**2
                    #check if everything is in order before uploading to mastodon server
                    if img_type in valid_img_types and img_size < valid_img_size:
                        if self.debuginfo: print(f"Will upload a {img_type} image of size {img_size}MB \n path:{img_to_upload}\n")
                        #img_upload = open(img_to_upload, 'rb')
                        media_id = self.api.media_post(media_file = img_to_upload)
                        if self.debuginfo: print(f"Uploaded image. media_dict:{media_id}\n")
                        media_id_list.append(media_id)
                        time.sleep(5)
                    else:
                        if self.debuginfo: print(f"Image type or size error... type: {img_type}, size: {img_size}MB")
                    if len(media_id_list) >= 4: break
                if media_id_list:
                    self.api.status_post( status = post_text, media_ids = media_id_list )
                    if self.debuginfo: print(f"Post with {len(media_id_list)} imgs: {post_text}\n")
                    post_res = True
            except FileNotFoundError:
                if self.debuginfo: print(f"File not found: {img_to_upload}")
            except MastodonAPIError as apierror:
                if self.debuginfo: print(f"API Error: {str(apierror)}")
                #try again 1 time, if fails, then move on...
                post_res = retryPostTextAndImage( ptext = post_text, mediaids = media_id_list )
        else:
            if self.debuginfo: print(f"Not valid post!\n Lenght:{len(post_text)} \n Post:{post_text}\n")
    
        return post_res
    
    #Function to be used ONLY if a post with images fails (triggers expection)
    def retryPostTextAndImage(self, ptext = '', mediaids = '' ):
        res_flg = False
        if ptext and mediaids:
            try:
                time.sleep(20)
                self.api.status_post( status = ptext, media_ids = mediaids )
                if self.debuginfo: print(f"[retry] Post with {len(mediaids)} imgs: {ptext}\n")
                res_flg = True
            except MastodonAPIError as apierror:
                if self.debuginfo: print(f"API Error on retry: {str(apierror)}")
        return res_flg
        
    
    #def tweetSysInfo( debuginfo = False ):
    #    #Get uptime info
    #    output = (subprocess.check_output(["uptime"])).decode()
    #    uptime = output.split(',')[0].split('up')[1]
    #    loadavg = output.split('load average')[1].split()
    #    uptime_loadavg = 'Uptime: %s; Load average: %s, %s, %s' % (uptime, loadavg[-3].strip(","),loadavg[-2].strip(","),loadavg[-1].strip(",") )
    #    #Get available memory info
    #    output = (subprocess.check_output(["free", "-h"])).decode().split()
    #    availablemem = 'Available memory: %s' % (output[12])
    #    #Concatenate the output
    #    systweet = 'Some non-sense info: \n[%s] \n[%s]\n' % (uptime_loadavg, availablemem)
    #    #send tweet
    #    tweetText( systweet, debuginfo )
 
# === END === 
