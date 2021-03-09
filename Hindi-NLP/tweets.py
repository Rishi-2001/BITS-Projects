# -*- coding: utf-8 -*-
import GetOldTweets3 as got
import time, json, pickle
from datetime import datetime, date, timedelta
import pandas as pd

searches = [
    "boobe",
    "औकात",
    "सलमान",
    "गांड",
    "दलाली",
    "media",
    "teri",
    "haramzade",
    "कुत्तों",
    "बाप",
    "gashti",
    "अबे",
    "ghatiya",
    "bhandve",
    "तेरी",
    "bna",
    "maar",
    "छाप",
    "gasti",
    "gaandmasti",
    "hijra",
    "dimag",
    "मरे",
    "chut",
    "accept",
    "बहनचोद",
    "हरामी",
    "jhant",
    "संघी",
    "lodu",
    "gaandfat",
    "query",
    "chootiya",
    "karti",
    "भेनचोद",
    "समझा",
    "कुत्ते",
    "rape",
    "ArvindKejriwal",
    "tera",
    "karke",
    "तेरा",
    "bc",
    "लुंड",
    "Feminists",
    "इस्लाम",
    "chuchi",
    "भेनचोद",
    "लुंड",
    "walo",
    "kuttiya",
    "choochi",
    "chinaal",
    "loda",
    "ghasti",
    "हलाला",
    "रोना",
    "kaminey",
    "Liberals",
    "भड़वा",
    "मुह",
    "saala",
    "बहन",
    "kutta",
    "results",
    "मिडिया",
    "chutiyapa",
    "gandu",
    "randi",
    "pataka",
    "दल्ले",
    "gaand",
    "tharak",
    "हराम",
    "Indian",
    "maa",
    "raand",
    "पैदा",
    "choot",
    "kanjar",
    "chutan",
    "कौम",
    "माधरचोद",
    "तुझे",
    "hawas",
    "bhadve",
    "lund",
    "chutiye",
    "सूअर",
    "ma",
    "chootia",
    "chinki",
    "चुदाई",
    "feminist",
    "मादरचोद",
    "तुमको",
    "सूअर",
    "भडवा",
    "हरामी",
    "भोसडीके",
    "सुअर",
    "paki",
    "najayaz",
    "lundtopi",
    "मा",
    "chutadd",
    "रंडी",
    "तुम्हे",
    "दोगले",
    "tum",
    "गाँड",
    "चुप",
    "जायरा",
    "साले",
    "women",
    "pagal",
    "kamine",
    "chuche",
    "Maa",
    "chooche",
    "culture",
    "बेशर्म",
    "jhantu",
    "दलाल",
    "gaandufad",
    "tujhe",
    "tharkiभड़वा",
    "hijda",
    "जात",
    "mard",
    "chutia",
    "chutiya",
    "chod",
    "मां",
    "jese",
    "maal",
    "भेज",
    "suar",
    "chutiya",
    "balatkar",
    "patakha",
    "bhosad",
    "chutad",
    "harami",
    "नीच",
    "aurat",
    "फट",
    "ghassa",
    "मुल्ले",
    "तू",
    "mutth",
    "tatte",
    "नमक",
    "chakke",
    "bhadva",
    "Feminist",
    "रंडी",
    "chod",
    "aand",
    "तेरे",
    "tatti",
    "lundure",
    "chodu",
    "aandu",
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
