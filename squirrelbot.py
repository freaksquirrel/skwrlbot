# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import argparse
import sys
import time
import sb_funcs as sbfunc
from sb_twitter import TwitterInterface
from sb_mastodon import MastodonInterface


def main():
    parser = argparse.ArgumentParser( description="Post stuff to the fediverse (twitter stuff is now deprecated)")
    parser.add_argument("-t", "--tweet", action="store", type="string", dest="tweet_text", help="send a tweet directly")
    parser.add_argument("-p", "--post", action="store", type="string", dest="post_text", help="post on mastodon directly")
    parser.add_argument("-f", "--fortune", action="store_true", dest="cookie")
    parser.add_argument("--dual", action="store_true", dest="dual_post", default=False, help="post on mastodon and twitter at the same time")
    parser.add_argument("--tweetonly", action="store_true", dest="only_tweet", default=False, help="post only to twitter...")
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
    
    # create the twitter instance if required
    #if args.tweet_text or (args.cookie and (args.dual_post or args.only_tweet)) or args.sysinfo or args.hashtag_find:
    if args.tweet_text or (args.cookie and (args.dual_post or args.only_tweet)) or args.sysinfo:
        twitterApi = TwitterInterface(debuginfo = args.debuginfo)
        post_max_len = twitterApi.tweet_max_len

    # create the mastodon instance if required
    if args.post_text or (args.cookie and not args.only_tweet):
        mastodonApi = MastodonInterface(debuginfo = args.debuginfo)
        post_max_len = mastodonApi.post_max_len
    
    # post (and maybe tweet) the system info
    if args.sysinfo:
        sysinfotxt = sbfunc.getSysInfo( debugflg = args.debuginfo, max_len = post_max_len )
        mastodonApi.postText( sysinfotxt )
        if args.dual_post:
            twitterApi.tweetText( sysinfotxt )
    
    # Post a fortune cookie... depending on flags, it may also tweet it ;)
    if args.cookie:
        fortunetxt = sbfunc.getFortuneCookie( debugflg = args.debuginfo, max_len = post_max_len )
        if args.dual_post:
            mastodonApi.postText( fortunetxt )
            twitterApi.tweetText( fortunetxt )
        elif args.only_tweet:
            twitterApi.tweetText( fortunetxt )
        else:
            mastodonApi.postText( fortunetxt )
    
    # tweet something...
    if args.tweet_text:
        twitterApi.tweetText( args.tweet_text )
        if args.dual_post:
            mastodonApi.postText( args.tweet_text )

    # post something...
    if args.post_text:
        mastodonApi.postText( args.post_text )
        if args.dual_post:
            twitterApi.tweetText( args.post_text )

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
