# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import argparse
import sys
import time
import sb_funcs as sbfunc
from sb_mastodon import MastodonInterface
from sb_bluesky import BlueskyInterface


def main():
    parser = argparse.ArgumentParser( description="Post stuff to the fediverse and bluesky")
    parser.add_argument("-p", "--post", action="store", dest="post_text", help="post on mastodon directly")
    parser.add_argument("-b", "--blue", action="store", dest="bpos_text", help="post on bluesky directly")
    parser.add_argument("-f", "--fortune", action="store_true", dest="cookie")
    #parser.add_argument("--dual", action="store_true", dest="dual_post", default=False, help="post on mastodon and XXX at the same time")
    #parser.add_option("--hashtag", action="store", type="string", dest="hashtag_find")
    parser.add_argument("-i", "--info", action="store_true", dest="sysinfo")
    parser.add_argument("-v", "--verbose", action="store_true", dest="debuginfo", default=False, help="Print out debug messages")
    args = parser.parse_args()

    post_max_len = 0
    
    # some boring debug info for the log
    if args.debuginfo:
        localtime = time.asctime( time.localtime(time.time()) )
        print(f"----------------------------------------------------- \n Start time: {localtime} \n")
    # end debug purposes

    # create the mastodon instance if required
    if args.post_text or args.cookie: 
        mastodonApi = MastodonInterface(debuginfo = args.debuginfo)
        post_max_len = mastodonApi.post_max_len

    # create the bluesky instance if required
    if args.bpos_text or args.cookie:
        blueskyApi = BlueskyInterface(debuginfo = args.debuginfo)   #TODO: check if async is better
        #post_max_len = blueskyApi.post_max_len
    
    # post (and maybe tweet) the system info
    if args.sysinfo:
        sysinfotxt = sbfunc.getSysInfo( debugflg = args.debuginfo, max_len = post_max_len )
        mastodonApi.postText( sysinfotxt )
        if args.dual_post:
            # post something else
    
    # Post a fortune cookie...
    if args.cookie:
        fortunetxt = sbfunc.getFortuneCookie( debugflg = args.debuginfo, max_len = mastodonApi.post_max_len )
        mastodonApi.postText( fortunetxt )
        fortunetxt = sbfunc.getFortuneCookie( debugflg = args.debuginfo, max_len = blueskyApi.post_max_len )
        #blueskyApi.postText( fortunetxt , True )
        blueskyApi.postText( post_text = fortunetxt, fortune_c = True )
        
        # if args.dual_post:
        #     mastodonApi.postText( fortunetxt )
        #     twitterApi.tweetText( fortunetxt )
        # elif args.only_tweet:
        #     twitterApi.tweetText( fortunetxt )
        # else:
        #     mastodonApi.postText( fortunetxt )
    
    # post something...
    if args.post_text:
        mastodonApi.postText( args.post_text )

    # post something...
    if args.bpos_text:
        blueskyApi.postText( args.post_text )


    # find a given hashtag in the bot's feed and perform related task...  Will not support this anymore as the API does not allow it without paying...
    #if args.hashtag_find:
    #    twitterApi.FindAndreplyTo()._hashtag( args.hashtag_find )
        
    # finalizing the boring debug info...
    if args.debuginfo:
        localtime = time.asctime( time.localtime(time.time()) )
        print(f"----------------------------------------------------- \n End time: {localtime} \n")
    # end debug purposes
# === END: main() ===

if __name__ == "__main__":
    sys.exit(main())

#----EOF--------------------------------------------------------
