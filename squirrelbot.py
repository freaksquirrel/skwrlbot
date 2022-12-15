# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import time
import sb_funcs as sbfunc
from sb_twitter import TwitterInterface
from sb_mastodon import MastodonInterface
from optparse import OptionParser


def main():
    parser = OptionParser()
    parser.add_option("-t", "--tweet", action="store", type="string", dest="tweet_text", help="send a tweet directly")
    parser.add_option("-p", "--post", action="store", type="string", dest="post_text", help="post on mastodon directly")
    parser.add_option("-f", "--fortune", action="store_true", dest="cookie")
    parser.add_option("-i", "--info", action="store_true", dest="sysinfo")
    parser.add_option("--dual", action="store_true", dest="dual_post", help="post on twitter and mastodon at the same time")
    parser.add_option("--hashtag", action="store", type="string", dest="hashtag_find")
    parser.add_option("-v", "--verbose", action="store_true", dest="debuginfo", default=False, help="Print out debug messages")
    (options, args) = parser.parse_args()

    # some boring debug info for the log
    if options.debuginfo:
        localtime = time.asctime( time.localtime(time.time()) )
        print(f"----------------------------------------------------- \n Start time: {localtime} \n")
    # end debug purposes

    #create the twitter instance if required
    if options.tweet_text or options.cookie or options.sysinfo or options.hashtag_find:
        twitterApi = TwitterInterface(debuginfo = options.debuginfo)

    #create the mastodon instance if required
    if options.post_text or options.dual_post:
        mastodonApi = MastodonInterface(debuginfo = options.debuginfo)
    
    # tweet system info
    if options.sysinfo:
        sysinfotxt = sbfunc.getSysInfo( debugflg = options.debuginfo, max_len = twitterApi.tweet_max_len )
        twitterApi.tweetText( sysinfotxt )
        if options.dual_post:
            mastodonApi.postText( sysinfotxt )
    
    # tweet a fortune cookie... also post to mastodon if flag is raised ;)
    if options.cookie:
        fortunetxt = sbfunc.getFortuneCookie( debugflg = options.debuginfo, max_len = twitterApi.tweet_max_len )
        twitterApi.tweetText( fortunetxt )
        if options.dual_post:
            mastodonApi.postText( fortunetxt )
    
    # tweet something...
    if options.tweet_text:
        twitterApi.tweetText( options.tweet_text )
        if options.dual_post:
            mastodonApi.postText( options.tweet_text )

    # post something...
    if options.post_text:
        mastodonApi.postText( options.post_text )
        if options.dual_post:
            twitterApi.tweetText( options.post_text )

    # find a given hashtag in the bot's feed and perform related task...
    if options.hashtag_find:
        twitterApi.FindAndreplyTo()._hashtag( options.hashtag_find )
        
    # finalizing the boring debug info...
    if options.debuginfo:
        localtime = time.asctime( time.localtime(time.time()) )
        print(f"----------------------------------------------------- \n End time: {localtime} \n")
    # end debug purposes
# === END: main() ===

if __name__ == "__main__":
    main()
