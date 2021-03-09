import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.naive_bayes import MultinomialNB as MNB
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
from indicnlp.tokenize import trivial_tokenize_indic

csv = pd.read_csv("data.csv")[["Text", "Label"]]
corpus = " ".join(csv["Text"])
vocab = {
    k: v
    for k, v in Counter(trivial_tokenize_indic(corpus)).items()
    if v > 5 and not k.isalpha() and v < 1000
}
csv["Clean"] = csv["Text"].apply(
    lambda x: [word for word in trivial_tokenize_indic(x) if word in vocab]
)

power = {0: {k: 0 for k in vocab.keys()}, 1: {k: 0 for k in vocab.keys()}}
for label in [0, 1]:
    for sent in csv[csv["Label"] == label]["Clean"].tolist():
        for word in sent:
            power[label][word] += 1

pos, neg = (
    {k for k, v in power[0].items() if v > 3},
    {k for k, v in power[1].items() if v > 3},
)
inter = pos.intersection(neg)
ratio = {
    k: power[1][k]
    / power[0][k]
    * ((csv["Label"] == 0).sum() / (csv["Label"] == 1).sum())
    for k in inter
}
hindi = sorted(ratio.items(), key=lambda k: -k[1])[:50]

csv = pd.read_csv("data.csv")[["Text", "Label"]]
corpus = " ".join(csv["Text"])
vocab = {
    k: v
    for k, v in Counter(trivial_tokenize_indic(corpus)).items()
    if v > 5 and k.isalpha() and v < 1000
}
csv["Clean"] = csv["Text"].apply(
    lambda x: [word for word in trivial_tokenize_indic(x) if word in vocab]
)

power = {0: {k: 0 for k in vocab.keys()}, 1: {k: 0 for k in vocab.keys()}}
for label in [0, 1]:
    for sent in csv[csv["Label"] == label]["Clean"].tolist():
        for word in sent:
            power[label][word] += 1

pos, neg = (
    {k for k, v in power[0].items() if v > 3},
    {k for k, v in power[1].items() if v > 3},
)
inter = pos.intersection(neg)
ratio = {
    k: power[1][k]
    / power[0][k]
    * ((csv["Label"] == 0).sum() / (csv["Label"] == 1).sum())
    for k in inter
}
eng = sorted(ratio.items(), key=lambda k: -k[1])[:50]
