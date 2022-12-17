# skwrlbot
Source code for the twitter skwrlbot. It requires access to the twitter api and mastodon api using clientids and tokens before actually being able to tweet/post. So I will update this later with all that info...



example usages:

tweet a fortune cookie:

python3 squirrelbot.py -f -v

tweet sys info:

python3 squirrelbot.py -i -v

tweet or post(mastodon) something:

python3 squirrelbot.py -t "this is a tweet!" -v

python3 squirrelbot.py -p "this is a post!" -v


Repost tweets to mastodon:

python3 repostbot.py -t -v


Will update usage examples later.

I use them in a crontab so I will try to add that example too...
