# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import os.path

#you may need to adjust the path below
#example --> iofiles_path = '/home/username/twitterbot/iofiles'
iofiles_path = './iofiles'

# common directories and files
patadas_frases_fn  ='frases_patadas.txt'
timeline_directory = 'timeline_id_logs'
patadas_frases     = os.path.join(iofiles_path, patadas_frases_fn)
timeline_mngt_path = os.path.join(iofiles_path, timeline_directory)
tempdata_directory = os.path.join(iofiles_path, 'tempdata')

# Twitter related files
tl_latest_tweet_id_fn     = '_tl_latest_fetched_tweet_id.txt'
hashtag_search_log_fn = 'hashtag_search_log.txt'
latesttweet_id_log = os.path.join(timeline_mngt_path, own_tl_latest_tweet_id_fn)
hashtag_search_log = os.path.join(iofiles_path, hashtag_search_log_fn)

# Mastodon related files
tl_latest_post_id_fn     = '_tl_latest_fetched_post_id.txt'
hashtag_search_mast_log_fn = 'hashtag_search_mastodon_log.txt'
latestpost_id_log  = os.path.join(timeline_mngt_path, own_tl_latest_post_id_fn)
hashtag_search_log = os.path.join(iofiles_path, hashtag_search_mast_log_fn)
