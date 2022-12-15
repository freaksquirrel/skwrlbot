# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import time
import rb_funcs as rbfunc
from sb_twitter import TwitterInterface
from sb_mastodon import MastodonInterface
from optparse import OptionParser


def main():
    parser = OptionParser()
    parser.add_option("-t", "--tweet2post", action="store_true", dest="tweet2post", default=False, help="Check own twitter TL and post own updates to Mastodon")
    parser.add_option("-p", "--post2tweet", action="store_true", dest="post2tweet", default=False, help="Check own mastodon TL and post own updates to Twitter")
    parser.add_option("-v", "--verbose",    action="store_true", dest="debuginfo",  default=False, help="Print out debug messages")
    (options, args) = parser.parse_args()

    # some boring debug info for the log
    localtime = time.asctime( time.localtime(time.time()) )
    if options.debuginfo: print(f"--Repost Bot start------------------------------- \n Time: {localtime} \n")
    # end debug purposes

    if options.tweet2post or options.post2tweet:
        #create the twitter instance if required
        twitterApi = TwitterInterface(debuginfo = options.debuginfo)
        #create the mastodon instance if required
        mastodonApi = MastodonInterface(debuginfo = options.debuginfo)
        
        #Call the functions here
        if options.tweet2post:
            #rbfunc.tweetToPost( tAPI = twitterApi, mAPI = mastodonApi, alltweets = True, debug_info=options.debuginfo)
            rbfunc.tweetToPost( tAPI = twitterApi, mAPI = mastodonApi, debug_info=options.debuginfo)
        else:
            #rbfunc.postToTweet( tAPI = twitterApi, mAPI = mastodonApi, allposts = True, debug_info=options.debuginfo)
            rbfunc.postToTweet( tAPI = twitterApi, mAPI = mastodonApi, debug_info=options.debuginfo)
    else:
        if options.debuginfo: print("The report bot was called but no action was performed \n")
        
    # finalizing the boring debug info...
    localtime = time.asctime( time.localtime(time.time()) )
    if options.debuginfo: print(f"--Repost Bot end------------------------------- \n Time: {localtime} \n")

# === END: main() ===

if __name__ == "__main__":
    main()
