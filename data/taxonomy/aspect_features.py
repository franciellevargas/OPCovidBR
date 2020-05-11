import numpy as np
import nlpnet
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from scipy import sparse
import unicodedata
import re
import spacy

class AspectExtractor:

	rep_size = 0
	nlp_pt = spacy.load('pt_core_news_sm')

	def __init__(self, bow=True, negation=True, emoticon=True, emoji=True, senti_words=True,
						   postag=True, bow_grams=1, verbose=True):
		self.verbose = verbose
		self.bow = bow
		self.negation = negation
		self.emoticon = emoticon
		self.emoji = emoji
		self.senti_words = senti_words
		self.postag = postag

		if verbose: print('using representation: ',end='')

		if senti_words:
			if verbose: print('senti_words ',end='')
			self.make_sentilex()
			self.sentilex_index = self.rep_size
			self.rep_size += 5

		if self.verbose: print()


	def clean_tweet(self, tweet):
	    string = str(unicodedata.normalize('NFKD', tweet).encode('ascii','ignore'))[2:]
	    string = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", string).split())

	    return self.lemmatizer(string)
	    

	def make_bow(self, *args):
		print("")

	def lemmatizer(self, sentence):
		new_sentence = ""
		doc = self.nlp_pt(sentence)
		for word in doc:
		    new_sentence += word.lemma_ + " "

		return new_sentence.strip().lower()
		

	def make_sentilex(self, path='./data/aspects/resources/sentilex-reduzido.txt'):
		self.sentilex = {}
		with open(path,'r') as sentilex_file:
			for line in sentilex_file:
				if line[0] != '#':
					line = line.strip().split(',')
					self.sentilex[self.clean_tweet(line[1])] = line[0]
					# self.sentilex[line[1]] = line[0]


	def get_representation(self, sentences):
		if self.verbose: print(len(sentences))
		if self.verbose: print(self.rep_size)

		new_sentences = np.zeros((len(sentences), len(self.sentilex)))

		for i, sent in enumerate(sentences):
			if self.verbose: print('%i/%i' % (i,len(sentences)),end='\r')

			sent = self.lemmatizer(sent)

			if self.senti_words:
				sent_words = [0] * len(self.sentilex)
				for sentilexWord in self.sentilex.keys():
					if sentilexWord in sent:
						list_values = list(self.sentilex.keys())
						index = list_values.index(sentilexWord)
						sent_words[index] += 1
				new_sentences[i,self.sentilex_index:self.sentilex_index+ len(self.sentilex)] += np.array(sent_words)

		if self.verbose: print('%i/%i' % (len(sentences),len(sentences)))
		return new_sentences


	def get_representation_sentences_classified(self, sentences):
		if self.verbose: print(len(sentences))
		if self.verbose: print(self.rep_size)
		myDict = {
			"economia": 0,
			"educação-ciência": 1,
			"localização": 2,
			"Político-social": 3,
			"saúde": 4
		}
		new_sentences = np.zeros((len(sentences), self.rep_size))

		for i, sent in enumerate(sentences):
			if self.verbose: print('%i/%i' % (i,len(sentences)),end='\r')

			sent = self.lemmatizer(sent)

			if self.senti_words:
				sent_words = [0,0,0,0,0]
				for sentilexWord in self.sentilex.keys():
					if sentilexWord in sent:
						index = myDict[self.sentilex[sentilexWord]]
						sent_words[index] += 1
				new_sentences[i,self.sentilex_index:self.sentilex_index+5] += np.array(sent_words)

		if self.verbose: print('%i/%i' % (len(sentences),len(sentences)))

		return new_sentences


	def get_sentences_classified(self, sentences):
		myDict = [
			"economia",
			"educação-ciência",
			"localização",
			"Político-social",
			"saúde"
		]

		new_sentences = self.get_representation_sentences_classified(sentences)

		new_sentences_classified = []
		i = 0

		for sentence in sentences:
			representation = new_sentences[i]

			#sistema de pontos
			j = 0
			for rep in representation:
				if j == 0:
					representation[j] *= 1
				if j == 1:
					representation[j] *= 1
				if j == 2:
					representation[j] *= 1			
				if j == 3:
					representation[j] *= 2
				if j == 4:
					representation[j] *= 3

				j += 1

			# Pega número maior
			finalIndex = 4
			j = 0
			for rep in representation:
				if rep > representation[finalIndex]:
					finalIndex = j

				j += 1

			i += 1

			new_sentences_classified.append((sentence.lower(), myDict[finalIndex]))

		return new_sentences_classified

