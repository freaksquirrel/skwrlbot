# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import sys
import subprocess
import os.path
import time
import re
import requests
import sb_iofiles as sbio
from sb_twitter import TwitterInterface
from sb_mastodon import MastodonInterface


def tweetToPost( tAPI = False, mAPI = False, alltweets = False, debug_info = False):
    post_res = False
    posted_tweets = 0
    latest_posted_tweet_id = 0
    if not tAPI or not mAPI or not isinstance(tAPI, TwitterInterface) or not isinstance(mAPI, MastodonInterface):
        return post_res
    else:
        #Check that the APIs are working fine
        if tAPI.credentials == False or tAPI.screen_name == '' or mAPI.credentials == False or mAPI.app_name == '':
            return post_res
        else:
            #start the process from here
            #get own Tweets (not own timeline)
            twTimeLine = tAPI.getUserTimeline( user_screen_name = tAPI.screen_name )
            for tweet in reversed(twTimeLine):
                if debug_info: print(f"Tweet: {tweet['full_text']}")
                if ( re.findall('[#?]t2p\\b', tweet['full_text'].lower()) or alltweets ):
                    if 'media' in tweet['entities'].keys():
                        if debug_info: print(f"Need to download media from tweet. [{len(tweet['extended_entities']['media'])} file(s)]")
                        #Tweets with images
                        tempdir = f"t_{tweet['id']}"
                        temppath = os.path.join(sbio.tempdata_directory, tempdir)
                        try:
                            os.makedirs(temppath, exist_ok = True)
                            if debug_info: print(f"Temp dir created successfully: {temppath}")
                            media_list = []
                            for media_info in tweet['extended_entities']['media']:
                                media_list.append(media_info['media_url'])
                                if len(media_list) >= 4: break

                            #download the images (up to 4), put them in temp, and upload them to mastodon
                            downloaded_imgs = downloadImageToDir( img_url = media_list, save_path = temppath)
                            #post the images and the text
                            mAPI.postTextAndImage(post_text = f"{tweet['full_text']}", image_path = downloaded_imgs )
                            
                            #uploaded_media_ids = []
                            #for img_to_upload in downloaded_imgs:
                            #    media_id = mAPI.api.media_post(media_file = img_to_upload)
                            #    uploaded_media_ids.append(media_id)
                            #    if debug_info: print(f"Uploaded image. media_dict:{media_id}\n")
                            #    time.sleep(2)
                            ##Now post the tweet with the media attached to it...
                            #time.sleep(5)
                            #mAPI.api.status_post( status = f"{tweet['full_text']} #tweet2post", media_ids=uploaded_media_ids )

                            #and then... get rid of the downlaoded files
                            deleteTempFileAndDir( file_list = downloaded_imgs, dir_path = temppath)
                            
                        except OSError as error:
                            if debug_info: print(f"Temp dir cannot be created: {temppath}")
                        #except FileNotFoundError:
                        #    if debug_info: print(f"File not found: {img_to_upload}")
                        except MastodonAPIError as apierror:
                            if debug_info: print(f"API Error: {str(apierror)}")
                    else:
                        if debug_info: print(f"Will post simple tweet to mastodon -> [ {tweet['full_text']} ]")
                        post_res = mAPI.postText( post_text = f"{tweet['full_text']}" )
                        if post_res:
                            latest_posted_tweet_id = tweet['id']
                            posted_tweets += 1
                #TODO: update the TL file in case that the process gets truncated (maybe will store the max id checked and then updat the file only once somewhere...)
                #tweet['id'],  tweet['user']['id']
                latesttweet_id_log = os.path.join(sbio.timeline_mngt_path, f"{tweet['user']['id']}{sbio.tl_latest_tweet_id_fn}")
                if debug_info: print(f"File for user: {latesttweet_id_log}")
                fp = open(latesttweet_id_log, 'w')
                fp.write(f"{tweet['id']}")
                fp.close()
            if debug_info: print(f"Posted {posted_tweets} tweets out of {len(twTimeLine)} to mastodon. Latest ID: {latest_posted_tweet_id} \n")
            return post_res


#This function is pending! need to check the twitter stuff more carefully
def post2Tweet( mAPI = False, tAPI = False, allposts = False, debug_info = False):
    tweet_res = False
    tweeted_posts = 0
    if not tAPI or not mAPI or not isinstance(tAPI, TwitterInterface) or not isinstance(mAPI, MastodonInterface):
        return tweet_res
    else:
        #Check that the APIs are working fine
        if tAPI.credentials == False or tAPI.screen_name == '' or mAPI.credentials == False or mAPI.app_name == '':
            return tweet_res
        else:
            #start the process from here
            return tweet_res



############### this functions will be moved somewhere else later... im lazy today.
def downloadImageToDir( img_url = '', save_path = ''):
    downloaded_files = []
    if img_url and save_path:
        if not isinstance(img_url, list): img_url = [img_url]
        for i_url in img_url:
            response = requests.get(i_url)
            imgfullpath = os.path.join( save_path, os.path.basename(i_url) )
            if response.status_code == 200 :
                fp = open(imgfullpath, 'wb')
                fp.write(response.content)
                fp.close()
                downloaded_files.append(imgfullpath)
    return downloaded_files


def deleteTempFileAndDir( file_list = '', dir_path = ''):
    if file_list and dir_path:
        if not isinstance(file_list, list): file_list = [file_list]
        try:
            for f_name in file_list:
                os.remove(f_name)
                print(f"File deleted: {f_name}")
            os.rmdir(dir_path)
            print(f"Directory deleted: {dir_path}")
            return True
        except OSError as error:
            print(f"Dir cannot be deleted: {dir_path}")
        except FileNotFoundError:
            print(f"File not found: {f_name}")
    else:
        return False
        
# === END === 
