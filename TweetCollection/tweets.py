# -*- coding: utf-8 -*-
import GetOldTweets3 as got
import time, json, pickle
from datetime import datetime, date, timedelta
import pandas as pd

searches = [
    "भेनचोद",
    "भोसडीके",
    "चुदाई",
    "कुत्ते",
    "मुल्ले",
    "दलाल",
    "नीच",
    "गाँड",
    "हरामी",
    "रंडी",
    "सूअर",
    "भड़वा",
    "गांड",
    "लुंड",
    "माधरचोद",
    "मादरचोद",
    "बहनचोद",
    "भेनचोद",
    "#भोसडीके",
    "#चुदाई",
    "#कुत्ते",
    "#मुल्ले",
    "#दलाल",
    "#नीच",
    "#गाँड",
    "#हरामी",
    "#रंडी",
    "#सूअर",
    "#भड़वा",
    "#गांड",
    "#लुंड",
    "#माधरचोद",
    "#मादरचोद",
    "#बहनचोद",
]
query = " OR ".join(searches)


def save(filename, tweets):
    with open("save.pkl", "wb+") as f:
        pickle.dump(tweets, f)


def load_to_csv(pickle_dir):
    with open(pickle_dir, "rb") as f:
        dump = pickle.load(f)
        tweets = [vars(tweet) for tweet in dump]
    return pd.DataFrame(tweets)


def DownloadTweets(
    SinceDate, UntilDate, Query=query, update_days=30, max_tweets=1000, sleep=300
):
    """
    Downloads all tweets from a certain month in three sessions in order to avoid sending too many requests. 
    Date format = 'yyyy-mm-dd'. 
    Query=string.
    """
    since = datetime.strptime(SinceDate, "%Y-%m-%d")
    until = datetime.strptime(UntilDate, "%Y-%m-%d")
    current = since
    results = []
    while current < until:
        try:
            batch_criteria = (
                got.manager.TweetCriteria()
                .setQuerySearch(Query)
                .setSince(current.strftime("%Y-%m-%d"))
                .setUntil((current + timedelta(days=update_days)).strftime("%Y-%m-%d"))
                .setLang("hi")
                .setMaxTweets(max_tweets)
            )
            current = current + timedelta(days=update_days)
            batch_tweets = got.manager.TweetManager.getTweets(batch_criteria)
            results.extend(batch_tweets)
            print(
                "Retrieving tweets from :" + current.strftime("%Y-%m-%d"),
                " to ",
                (current + timedelta(days=update_days)).strftime("%Y-%m-%d"),
            )
            time.sleep(sleep)
        except:
            pass
    return results
