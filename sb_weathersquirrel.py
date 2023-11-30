# -*- coding: utf-8 -*-
#!/usr/bin/env python3

# Note: Twitter related calls are commented out since twitter's API does not work as intended now... blame Melon Tusk for it. 
import argparse
import sys
import time
import sb_weather_funcs as sbwfunc
import sb_weather_config as sbwcfg
from sb_mastodon import MastodonInterface
#from sb_twitter import TwitterInterface


def main():
    cat_full_list = ['all'] + list(sbwcfg.graph_amedas_dic.keys())
    area_sn_list = [area['short_name'] for area in sbwcfg.area_info.values() if area['short_name'] != 'comm']
    parser = argparse.ArgumentParser( description="Post weather info from AMEADAS api to the fediverse or twitter.")
    parser.add_argument("-v", "--verbose"        , action="store_true", dest="debuginfo",      default=False, help="Print out debug messages")
    parser.add_argument("-p", "--postweather"    , action="store_true", dest="postweather",     default=False, help="Post latest weather info for default area")
    parser.add_argument("-c", "--compweatherdate", action="store_true", dest="compweatherdate", default=False, help="Post weather comparison by dates for default area")
    parser.add_argument("-a", "--cmpweatherarea" , action="store_true", dest="cmpweatherarea",  default=False, help="Post weather comparison of the 2 default areas")
    parser.add_argument("--cmpwareas"            , nargs=2, metavar=('area_sn_A','area_sn_B'), choices=area_sn_list, help="Post graphs that compare the weather of 2 different areas (ref. by short name)")
    parser.add_argument("--cmpallareas"          , nargs=1, dest="cmpallareas", metavar=('category_name'), choices=cat_full_list, help="Post graphs that compare a weather info category for all areas registered. Use 'all' to post all categories related info")
    #parser.add_argument("-t", "--tweetweather",   action="store_true", dest="tweetweather",   default=False, help="Tweet weather info (deprecated)")
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
    elif args.cmpallareas:
        cat_name = args.cmpallareas[0]
        # create the mastodon instance
        mastodonApi = MastodonInterface(debuginfo = args.debuginfo )
        # Call the functions here
        debug_info = sbwfunc.postAllAreasWeatherInfo( mAPI = mastodonApi, val_name = cat_name, debug_info = args.debuginfo )
    ####======================================= Twitter stuff ====================================================================
    # elif args.tweetweather:
    #     #create the twitter instance if required
    #     twitterApi = TwitterInterface(debuginfo = args.debuginfo )
    #     #Call the functions here
    #     debug_info = sbwfunc.tweetCompWeatherInfo( tAPI = twitterApi, debug_info = args.debuginfo )
    else:
        if args.debuginfo: print("The report bot was called but no action was performed \n")
        
    # finalizing the boring debug info...
    localtime = time.asctime( time.localtime(time.time()) )
    if args.debuginfo: print(f"--Weather squirrel Bot end------------------------------- \n Time: {localtime} \n")
# === END: main() ===

if __name__ == "__main__":
    sys.exit(main())
    
#----EOF--------------------------------------------------------
