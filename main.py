# -*- coding: utf-8 -*-
#/usr/local/lib/python3.6
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC, LinearSVC

from sklearn.metrics import accuracy_score, precision_score, f1_score, r2_score, recall_score, classification_report
from sklearn.model_selection import train_test_split
import os
import re
import nltk
import csv
import unicodedata
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from data.tweentsentbr.features import FeatureExtractor
from data.aspects.features import AspectExtractor
from sklearn.naive_bayes import GaussianNB
import pickle

nltk.download('punkt')

base_path = 'data/reli'
ReLiTrain = []
TweetSentBRTrain = []
covidOptionsBRTest = []

files = [os.path.join(base_path, f) for f in os.listdir(base_path)]

for file in files:
    t = 1 if '_Positivos' in file else -1
    with open(file, 'r', encoding = "ISO-8859-1") as content_file:
        content = content_file.read()
        all = re.findall('\[.*?\]', content)
        for w in all:
          ReLiTrain.append((w[1:-1], t))


def clean_tweet(tweet):
    string = str(unicodedata.normalize('NFKD', tweet).encode('ascii','ignore'))[2:]
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", string).split())
    
# Train by Henrico DATASET
filePos = open('data/tweentsentbr/trainTT.pos', 'r')
fileNeg = open('data/tweentsentbr/trainTT.neg', 'r')
for line in filePos:
  TweetSentBRTrain.append((clean_tweet(line[19:]), 1))
for line in fileNeg:
  TweetSentBRTrain.append((clean_tweet(line[19:]), -1))


# Make test Using CovidOptions.BR
# ----------------------
file = csv.reader(open('data/test/SentCovid-BR.csv'), delimiter=',')
for line in file:
  tweet = line[1]
  sentiment = int(line[2])
  covidOptionsBRTest.append((clean_tweet(tweet), sentiment))




with open('resultado.txt', 'a') as f:
  def evaluate_model(model, X, y, X_test, y_test, modelName):
    model.fit(X, y)

    with open('data/modelos/' + modelName, 'wb') as file:
        pickle.dump(model, file)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    # precision = precision_score(y_test, y_pred)
    # f1_score_variable = f1_score(y_test, y_pred)
    # recall_score_variable = recall_score(y_test, y_pred)
    print("Accuracy", accuracy, file=f)
    # print("precision", precision, file=f)
    # print("f1_score", f1_score_variable, file=f)
    # print("recall_score", recall_score_variable, file=f)
    print("Classification report", file=f)
    print(classification_report(y_test, y_pred), file=f)
    print("\n", file=f)

  def Experiment(trainData, testData, extractor, basepath):
    feats = extractor
    train_sentences = []
    train_labels = []
    test_sentences = []
    test_labels = []


    for sentence, sentiment in trainData:
      train_sentences.append(sentence)
      train_labels.append(sentiment)

    for sentence, sentiment in testData:
      test_sentences.append(sentence)
      test_labels.append(sentiment)

    feats.make_bow(train_sentences, test_sentences)

    X_train = feats.get_representation(train_sentences)
    y_train = np.array(train_labels)

    X_test  = feats.get_representation(test_sentences)
    y_test = np.array(test_labels)

    print("----------- DecisionTreeClassifier --------------", file=f)
    evaluate_model(DecisionTreeClassifier(), X_train, y_train, X_test, y_test, basepath + 'DecisionTreeClassifier.pkl')

    print("----------- NaiveBayesClassifier --------------", file=f)
    evaluate_model(GaussianNB(), X_train, y_train, X_test, y_test, basepath + 'GaussianNB.pkl')

    print("----------- SVM - SVC(kernel='poly', degree=2) --------------", file=f)
    evaluate_model(SVC(kernel='poly', degree=2), X_train, y_train, X_test, y_test, basepath + 'SVC-poly.pkl')

    print("----------- SVM - LinearSVC --------------", file=f)
    evaluate_model(LinearSVC(C=0.25, penalty="l1", dual=False, random_state=1), X_train, y_train, X_test, y_test, basepath + 'LinearSVC.pkl')

    print("----------- SVM - SVC(kernel='sigmoid') --------------", file=f)
    evaluate_model(SVC(kernel='sigmoid'), X_train, y_train, X_test, y_test, basepath + 'SVC-sigmoid.pkl')

    print("\n\n", file=f)



  # Experiments
  # Experiment - Train With ReLI 
  print("1. Experimento - Treinamento apenas com o ReLi", file=f)
  feats =  FeatureExtractor()
  Experiment(ReLiTrain, covidOptionsBRTest, feats, 'polarity/reli/')


  # # Experiment - Train With TweetSentBR 
  print("2. Experimento - Treinamento com TweetSentBR", file=f)
  feats =  FeatureExtractor()
  Experiment(TweetSentBRTrain, covidOptionsBRTest, feats, 'polarity/tweentsentbr/')


  # Experiment - Train With ReLI + TweetSentBR 
  print("3. Experimento - Treinamento com ReLI + TweetSentBR", file=f)
  feats =  FeatureExtractor() 
  Experiment(ReLiTrain + TweetSentBRTrain, covidOptionsBRTest, feats, 'polarity/reli-tweentsentbr/')


  # Experiment - Train With ReLI + TweetSentBR + CovidOptions.BR
  print("4. Experimento - Treinamento com ReLI + TweetSentBR + CovidOptions.BR (.25 separado para teste)", file=f)
  train, test = train_test_split(covidOptionsBRTest, test_size=0.25)
  feats =  FeatureExtractor() 
  Experiment(ReLiTrain + TweetSentBRTrain + train, test, feats, 'polarity/reli-tweentsentbr-covidopbr/')

  # Experiment - Train With CovidOptions.BR
  print("5. Experimento - CovidOptions.BR (.25 separado para teste)", file=f)
  feats =  FeatureExtractor() 
  Experiment(train, test, feats, 'polarity/covidopbr/')


  # ASPECTOS
  # ----------
  aspects = AspectExtractor()
  sentencas = []
  for sentence, sentiment in covidOptionsBRTest:
    sentencas.append(sentence)

  # --- COM LEMATIZAÇÃO ----
  covidOptionsBRcomAspectos = aspects.get_sentences_classified(sentencas)
  pd.DataFrame(covidOptionsBRcomAspectos).to_csv("file_metodo_um.csv")

  # --- SEM LEMATIZAÇÃO ----
  # covidOptionsBRcomAspectos = []
  # file = csv.reader(open('file_metodo_um.csv'), delimiter=',')
  # for line in file:
  #   tweet = line[1]
  #   sentiment = line[2]
  #   covidOptionsBRcomAspectos.append((clean_tweet(tweet), sentiment))


  # Experimento com aspectos
  train, test = train_test_split(covidOptionsBRcomAspectos, test_size=0.25)
  print("EXTRA. Experimento - detectar qual é o assunto (educação,saúde,politico-social,etc)", file=f)
  Experiment(train,test, aspects, 'aspects/')
© 2020 GitHub, Inc.