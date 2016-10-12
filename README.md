# Data Mining for the Project of Twitter Sociolinguistics #

This repository contains a sample file `complete_timeline.py` used to harvest the timeline tweets of a given list of Twitter users. Specifically, it mines the tweets that are posted earlier than a particular time point `being`. In addition, it handles other issues such as unstable network connection and Twitter users' privacy setting.

Part of the code is built from fragments introduced by [Russell 2013](http://shop.oreilly.com/product/0636920030195.do).

The folder `rate_control` contains the files that record the time stamps of the most recent queries, in order to avoid hitting the rate limits of Twitter API.
