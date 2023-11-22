# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import argparse
import sys
import time
import sb_weather_funcs as sbwfunc
from sb_twitter import TwitterInterface
from sb_mastodon import MastodonInterface


def main():
    parser = argparse.ArgumentParser( description="Post weather imfo from AMEADAS api to the fediverse or twitter.")
    parser.add_argument("-p", "--postweather",     action="store_true", dest="postweather",     default=False, help="Post latest weather info for default area")
    parser.add_argument("-c", "--compweatherdate", action="store_true", dest="compweatherdate", default=False, help="Post weather comparison by dates for default area")
    parser.add_argument("-a", "--cmpweatherarea",  action="store_true", dest="cmpweatherarea",  default=False, help="Post weather comparison of the 2 default areas")
    parser.add_argument("--cmpwareas", nargs=2, metavar=('area_sn_A','area_sn_B'), help="Post graphs that compare the weather of 2 different areas (ref. by short name)")
    parser.add_argument("-t", "--tweetweather",   action="store_true", dest="tweetweather",   default=False, help="Tweet weather info (deprecated)")
    parser.add_argument("-v", "--verbose",        action="store_true", dest="debuginfo",      default=False, help="Print out debug messages")
    args = parser.parse_args()

    # some boring debug info for the log
    localtime = time.asctime( time.localtime(time.time()) )
    if args.debuginfo: print(f"--Weather squirrel Bot start------------------------------- \n Time: {localtime} \n")
    # end debug purposes

    if args.postweather:
        #create the mastodon instance
        mastodonApi = MastodonInterface(debuginfo = args.debuginfo )
        #Call the functions here
        debug_info = sbwfunc.postWeatherInfoSimple( mAPI = mastodonApi, debug_info = args.debuginfo )
    elif args.compweatherdate:
        #create the mastodon instance
        mastodonApi = MastodonInterface(debuginfo = args.debuginfo )
        #Call the functions here
        debug_info = sbwfunc.postCompWeatherInfo( mAPI = mastodonApi, debug_info = args.debuginfo )
    elif args.cmpweatherarea:
        #create the mastodon instance
        mastodonApi = MastodonInterface(debuginfo = args.debuginfo )
        #Call the functions here
        debug_info = sbwfunc.postCompAreaWeatherInfo( mAPI = mastodonApi, debug_info = args.debuginfo )
    elif args.cmpwareas:
        area_sn_A, area_sn_B = args.cmpwareas
        # create the mastodon instance
        mastodonApi = MastodonInterface(debuginfo = args.debuginfo )
        # Call the functions here
        debug_info = sbwfunc.postCompAreaWeatherInfo( mAPI = mastodonApi, areaA = area_sn_A, areaB = area_sn_B, debug_info = args.debuginfo )
    ####======================================= Twitter stuff ====================================================================
    elif args.tweetweather:
        #create the twitter instance if required
        twitterApi = TwitterInterface(debuginfo = args.debuginfo )
        #Call the functions here
        debug_info = sbwfunc.tweetCompWeatherInfo( tAPI = twitterApi, debug_info = args.debuginfo )
    else:
        if args.debuginfo: print("The report bot was called but no action was performed \n")
        
    # finalizing the boring debug info...
    localtime = time.asctime( time.localtime(time.time()) )
    if args.debuginfo: print(f"--Weather squirrel Bot end------------------------------- \n Time: {localtime} \n")

# === END: main() ===

if __name__ == "__main__":
    sys.exit(main())
    
#----EOF--------------------------------------------------------
