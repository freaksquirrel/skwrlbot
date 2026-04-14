# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import sys
import subprocess
import os, time
import re
import imghdr
from atproto import Client, client_utils

import sb_authinfo_bluesky as sbauth
import sb_iofiles as sbio
        
class BlueskyInterface:

    post_max_len = 300
    
    # Class constructor
    def __init__( self, async_clnt = False, debuginfo = False ):
        self.debuginfo = debuginfo
        if async_clnt:
            self.client = AsyncClient()
        else:
            self.client = Client()

        # TODO: check the error handling
        try:
            self.profile = self.client.login( sbauth.BLUESKY_BOT_HANDLE, sbauth.BLUESKY_BOT_SECRET )
            self.app_name = self.profile.display_name
            self.username = self.profile.handle
        except atproto.exceptions.AtProtocolError :
            self.profile = None
            self.app_name = ""
            self.username = ""
            
            if self.debuginfo: print("Authentication failed! check the authentication parameters and try again.")
    # -- end: init


    # Get own timeline (in order to checkl the tweets of users the bot follows)
    # TODO: 
    def getTimeline(self):

        timeline = self.client.get_timeline(algorithm='reverse-chronological')
        return timeline

    # TODO: get a user timeline 
    def getUserTimeline(self, user_screen_name = ''):
        user_timeline = False

        return user_timeline

    # post only text...
    def postText( self, post_text = '', fortune_c = False ):
        
        post_res = False 
        if post_text and len(post_text) < self.post_max_len:
            if fortune_c: post_text = post_text.replace("#fortune", "")
            text_builder = client_utils.TextBuilder()
            text_builder.text( post_text )
            if fortune_c:
                text_builder.tag('#fortune', 'fortune')
                text_builder.text(" \n ")
            text_builder.tag('#skwrlbot', 'skwrlbot')
            self.client.send_post(text_builder)
            post_res = True
            #if self.debuginfo: print(f"Post: {post_text}\n")
            if self.debuginfo: print(f"Post: {text_builder.build_text()}\n")
        else:
            if self.debuginfo: print(f"Not valid post!\n Lenght:{len(post_text)} \n Post:{post_text}\n")
        return post_res

    
    # up to 4 images,  5 MB each
    def postTextAndImage(self, post_text = '', image_path = '', image_alt = '' ):
        post_res = False
        valid_img_types = {'jpeg','png','bmp'}
        valid_img_size = 5
        #if image_path and post_text and image_alt and len(post_text) < self.post_max_len:
        if image_path and post_text and len(post_text) < self.post_max_len:
            try:
                if not isinstance(image_path, list): image_path = [image_path]
                #if not isinstance(image_alt , list): image_alt  = [image_alt]
                image_alt = [post_text] * len(image_path)

                post_text = post_text.replace("#weatherSQuirreL", "")
                text_builder = client_utils.TextBuilder()
                text_builder.text( post_text )
                text_builder.tag('#weatherSQuirreL', 'weatherSQuirreL')
                text_builder.text(" \n ")
                text_builder.tag('#skwrlbot', 'skwrlbot')

                media_list = []
                for img_to_upload in image_path:
                    #check that the file is actually an image (also serves as file existance check using the exception)
                    img_type = imghdr.what(img_to_upload)
                    #get the file size in MB (also serves as file existance check using the exception)
                    img_size = os.stat(img_to_upload).st_size / 1024**2
                    #check if everything is in order before opening..
                    if img_type in valid_img_types and img_size < valid_img_size:
                        if self.debuginfo: print(f"Will upload a {img_type} image of size {img_size}MB \n path:{img_to_upload}\n")
                        with open(img_to_upload, 'rb') as imgf:
                            media_list.append(imgf.read())
                    else:
                        if self.debuginfo: print(f"Image type or size error... type: {img_type}, size: {img_size}MB")
                    if len(media_list) >= 4: break
                if media_list:
                    self.client.send_images(
                        text = text_builder,
                        images = media_list,
                        image_alts = image_alt
                    )
                    if self.debuginfo: print(f"Post with {len(media_list)} imgs: {post_text}\n")
                    post_res = True
            except FileNotFoundError:
                if self.debuginfo: print(f"File not found: {img_to_upload}")
        else:
            if self.debuginfo: print(f"Not valid post!\n Lenght:{len(post_text)} \n Post:{post_text}\n Images:{len(image_path)}\n")
    
        return post_res

# === END === 
