# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import datetime as dt
import glob
import sb_weather_config as sbwcfg
from sb_mastodon import MastodonInterface
from sb_twitter import TwitterInterface


# Post a single weather graph/info for a given date to either Mastodon or Twitter
# ============= BEGIN: STILL UNDER CONSTRUCTION =========================
def postWeatherInfoSingle( API = False, value = '', target_date = '', debug_info = False):
    post_res = False
    toWhere = ''
    if not API or (not isinstance(API, MastodonInterface) and not isinstance(API, TwitterInterface)) or value == '':
        return post_res
    else:
        #Check that the API is working fine
        if API.credentials == False: #or API.app_name == '' or API.screen_name == '':
            return post_res
        else:
            try:
                if( not isinstance(target_date, dt.datetime) ): target_date = dt.datetime.now()
                weather_image_path = []
                weather_image_path = findWeatherGraphsByDate( target_datetime = target_date, val_name = value )
                weather_post_text = sbwcfg.weather_ondate_post_single_text.replace( sbwcfg.replace_target_date, target_date.strftime('%Y-%m-%d') )
                if isinstance(API, MastodonInterface):
                    #post_res = API.postTextAndImage(post_text = weather_post_text, image_path = weather_image_path )
                    toWhere = 'Mastodon'
                elif isinstance(API, TwitterInterface):
                    #post_res = API.tweetTextAndImage(tweet_text = weather_post_text, image_path = weather_image_path )
                    toWhere = 'Twitter'
                else:
                    return post_res
            except MastodonAPIError as apierror:
                if debug_info: print(f"Mastodon API Error: {str(apierror)}")
            except TwythonExceptions.TwythonError as apierror:
                if debug_info: print(f"Twitter API Error: {str(apierror)}")

    if debug_info: print(f"Posted {len(weather_image_path)} graph regarding {target_date} {value} to {toWhere}.\n")
    return post_res
# ============= END: STILL UNDER CONSTRUCTION =========================

# Post all weather graphs/info for a given date to Mastodon (up to 4 images)
def postWeatherInfoSimple( mAPI = False, debug_info = False):
    post_res = False
    if not mAPI or not isinstance(mAPI, MastodonInterface):
        return post_res
    else:
        #Check that the API is working fine
        if mAPI.credentials == False or mAPI.app_name == '':
            return post_res
        else:
            try:
                when_weather = dt.datetime.today()# - dt.timedelta(days = 1)
                weather_image_path = []
                weather_image_path = findWeatherGraphsByDate( target_datetime = when_weather )
                weather_post_text = sbwcfg.weather_ondate_post_text.replace( sbwcfg.replace_target_date, when_weather.strftime('%Y-%m-%d') )
                post_res = mAPI.postTextAndImage(post_text = weather_post_text, image_path = weather_image_path )
            except MastodonAPIError as apierror:
                if debug_info: print(f"API Error: {str(apierror)}")

    if debug_info: print(f"Posted {len(weather_image_path)} graph regarding {when_weather} weather to mastodon.\n")
    return post_res


# Post all weather comparison graphs to Mastodon (up to 4 images)
def postCompWeatherInfo( mAPI = False, debug_info = False):
    post_res = False
    if not mAPI or not isinstance(mAPI, MastodonInterface):
        return post_res
    else:
        #Check that the API is working fine
        if mAPI.credentials == False or mAPI.app_name == '':
            return post_res
        else:
            try:
                when_lst = dt.datetime.today() - dt.timedelta(days = sbwcfg.ndays_timedelta_lst)
                when_prv = dt.datetime.today() - dt.timedelta(days = sbwcfg.ndays_timedelta_prv)
                weather_comp_image_path = []
                weather_comp_image_path = findWeatherCompGraphsByDate( lst_target = when_lst, prv_target = when_prv )
                weather_comp_post_text = sbwcfg.weather_comp_post_text.replace( sbwcfg.replace_target_date, when_lst.strftime('%Y-%m-%d') ).replace( sbwcfg.replace_target_date_cmp, when_prv.strftime('%Y-%m-%d') )
                post_res = mAPI.postTextAndImage(post_text = weather_comp_post_text, image_path = weather_comp_image_path )
            except MastodonAPIError as apierror:
                if debug_info: print(f"API Error: {str(apierror)}")

    if debug_info: print(f"Posted {len(weather_comp_image_path)} graph regarding {when_lst} vs {when_prv} weather to mastodon.\n")
    return post_res


# Tweet all weather comparison graphs (up to 4 images)
def tweetCompWeatherInfo( tAPI = False, debug_info = False):
    post_res = False
    if not tAPI or not isinstance(tAPI, TwitterInterface):
        return post_res
    else:
        #Check that the API is working fine
        if tAPI.credentials == False or tAPI.screen_name == '':
            return post_res
        else:
            try:
                when_lst = dt.datetime.today() - dt.timedelta(days = sbwcfg.ndays_timedelta_lst)
                when_prv = dt.datetime.today() - dt.timedelta(days = sbwcfg.ndays_timedelta_prv)
                weather_comp_image_path = []
                weather_comp_image_path = findWeatherCompGraphsByDate( lst_target = when_lst, prv_target = when_prv )
                weather_comp_post_text = sbwcfg.weather_comp_post_text.replace( sbwcfg.replace_target_date, when_lst.strftime('%Y-%m-%d') ).replace( sbwcfg.replace_target_date_cmp, when_prv.strftime('%Y-%m-%d') )
                post_res = tAPI.tweetTextAndImage(tweet_text = weather_comp_post_text, image_path = weather_comp_image_path )
            except TwythonExceptions.TwythonError as apierror:
                if debug_info: print(f"API Error: {str(apierror)}")

    if debug_info: print(f"Posted {len(weather_comp_image_path)} graph regarding {when_lst} vs {when_prv} weather to twitter.\n")
    return post_res


# Post all weather comparison graphs to Mastodon (up to 4 images)
def postCompAreaWeatherInfo( mAPI = False, areaA = '', areaB = '', when_weather = '', debug_info = False):
    post_res = False
    if not mAPI or not isinstance(mAPI, MastodonInterface):
        return post_res
    else:
        #Check that the API is working fine
        if mAPI.credentials == False or mAPI.app_name == '':
            return post_res
        else:
            try:
                area_code_A, area_code_B = ['','']
                for areacd_check in sbwcfg.area_info :
                    if( areacd_check == 'common' ): continue
                    if( areaA in list(sbwcfg.area_info[areacd_check].values()) ): area_code_A = areacd_check
                    if( areaB in list(sbwcfg.area_info[areacd_check].values()) ): area_code_B = areacd_check
                if( not area_code_A ): area_code_A = sbwcfg.area_code_def
                if( not area_code_B ): area_code_B = sbwcfg.area_code_comp_def
                if( not when_weather or not isinstance(when_weather, dt.datetime) ): when_weather = dt.datetime.today() - dt.timedelta(days = 1)
                weather_comp_image_path = []
                weather_comp_image_path = findWeatherCompAreaGraphsByDate( target_datetime = when_weather, areaA = area_code_A, areaB = area_code_B )
                weather_comp_post_text = sbwcfg.weather_comparea_post_text.replace( sbwcfg.replace_target_date, when_weather.strftime('%Y-%m-%d') ).replace( sbwcfg.replace_target_acodeA, sbwcfg.area_info[area_code_A]['name']).replace( sbwcfg.replace_target_acodeB, sbwcfg.area_info[area_code_B]['name'])
                post_res = mAPI.postTextAndImage(post_text = weather_comp_post_text, image_path = weather_comp_image_path )
            except MastodonAPIError as apierror:
                if debug_info: print(f"API Error: {str(apierror)}")

    if debug_info: print(f"Posted {len(weather_comp_image_path)} graph regarding {when_weather} weather comparison between areas to mastodon.\n")
    return post_res


# Search for weather info graphs from a given date at the given path and return the paths
def findWeatherGraphsByDate( target_datetime = '', val_name = '', graph_path = ''):
    if( not isinstance(target_datetime, dt.datetime) ): target_datetime = dt.datetime.now()
    if( not graph_path ):
        graph_path = sbwcfg.graph_path.replace(sbwcfg.replace_target_year, target_datetime.strftime('%Y')).replace(sbwcfg.replace_target_month,target_datetime.strftime('%m')).replace(sbwcfg.replace_target_areacode, sbwcfg.area_code_def)
    datetime_str = target_datetime.strftime('%Y-%m-%d')
    if val_name == '':
        val_replace = '*'
    else:
        val_replace = sbwcfg.graph_amedas_dic[val_name][2]
    
    search_pattern = graph_path + sbwcfg.graph_simple_fname.replace(sbwcfg.replace_target_value , val_replace).replace(sbwcfg.replace_target_date , datetime_str)
    print(f"Search pattern: ({search_pattern})")
    graph_files = glob.glob( search_pattern )
    return graph_files


# Search for weather comparison graphs from a given date at the given path and return the paths
def findWeatherCompGraphsByDate( lst_target = '', prv_target = '', graph_path = ''):
    if( not isinstance(lst_target, dt.datetime) or not isinstance(prv_target, dt.datetime) ):
        lst_target = dt.datetime.now() - dt.timedelta( days = sbwcfg.ndays_timedelta_lst )
        prv_target = dt.datetime.now() - dt.timedelta( days = sbwcfg.ndays_timedelta_prv )
    if( not graph_path ):
        graph_path = sbwcfg.graph_path.replace(sbwcfg.replace_target_year, lst_target.strftime('%Y')).replace(sbwcfg.replace_target_month,lst_target.strftime('%m')).replace(sbwcfg.replace_target_areacode, sbwcfg.area_code_def)
    datetime_str_lst = lst_target.strftime('%Y-%m-%d')
    datetime_str_prv = prv_target.strftime('%Y-%m-%d')
    val_replace = '*'
    search_pattern = graph_path + sbwcfg.graph_datecomp_fname.replace( sbwcfg.replace_target_value, val_replace ).replace( sbwcfg.replace_target_date, datetime_str_lst ).replace( sbwcfg.replace_target_date_cmp, datetime_str_prv )
    print(f"The searh pattenn -> ({search_pattern})")
    graph_files = glob.glob( search_pattern )
    return graph_files


# Search for weather comparison graphs from a given date at the given path and return the paths
def findWeatherCompAreaGraphsByDate( target_datetime = '', val_name = '', areaA = '', areaB = '', graph_path = '' ):
    if( not isinstance(target_datetime, dt.datetime) ): target_datetime = dt.datetime.now()
    if( not graph_path ):
        graph_path = sbwcfg.graph_path.replace(sbwcfg.replace_target_year, target_datetime.strftime('%Y')).replace(sbwcfg.replace_target_month,target_datetime.strftime('%m')).replace(sbwcfg.replace_target_areacode, 'common')
    datetime_str = target_datetime.strftime('%Y-%m-%d')
    if( not areaA ) :
        areaa_replace = sbwcfg.area_info[sbwcfg.area_code_def]['short_name']
    else:
        areaa_replace = sbwcfg.area_info[areaA]['short_name']

    if( not areaB ) :
        areab_replace = sbwcfg.area_info[sbwcfg.area_code_comp_def]['short_name']
    else:
        areab_replace = sbwcfg.area_info[areaB]['short_name']

    if val_name == '':
        val_replace = '*'
    else:
        val_replace = sbwcfg.graph_amedas_dic[val_name][2]

    search_pattern = graph_path + sbwcfg.graph_areacomp_fname.replace(sbwcfg.replace_target_acodeA, areaa_replace).replace(sbwcfg.replace_target_acodeB, areab_replace).replace(sbwcfg.replace_target_date , datetime_str).replace(sbwcfg.replace_target_value , val_replace)
    print(f"The searh pattenn -> ({search_pattern})")
    graph_files = glob.glob( search_pattern )
    return graph_files


# === END ===
