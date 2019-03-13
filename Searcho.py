from CacmReader import CacmReader
from StanfordReader import StanfordReader

from pprint import pprint
import matplotlib.pyplot as plt
from math import log, log10

import numpy as np
import operator

from tools.Color import Color
from tools.SelectMenu import SelectMenu




class Searcho:

	# CONSTRUCTOR
	def __init__(self):

		self.cacm_reader = CacmReader()
		self.stanford_reader = StanfordReader()

		self.active_collection = ''

		self.docs = dict()
		self.index = dict()
		self.vectors = dict()


	# METHODS
	def read_cacm_collection(self):
		self.active_collection = 'Cacm'

		self.cacm_reader.open_cacm_file()

		# read the documents
		while not self.cacm_reader.finished:
			doc = self.cacm_reader.build_next_document()
			self.docs[doc.id] = doc

		# read the common words
		self.cacm_reader.read_common_words()
		

	def read_cs276_collection(self):
		self.active_collection = 'Cs276'

		self.stanford_reader.read_collection()
		self.docs = self.stanford_reader.docs
		self.stanford_reader.read_common_words()


	def create_index_cacm(self):
		for doc in self.docs.values():
			doc.tokenize()
			doc.stop_words(self.cacm_reader.common_words)

			for word in doc.terms:
				if word not in self.index.keys():
					self.index[word] = dict()

				if doc.id not in self.index[word].keys():
					self.index[word][doc.id] = 0

				self.index[word][doc.id] += 1

	
	def create_index_cs276(self):
		for doc in self.docs.values():

			for word in doc.terms:
				if word not in self.index.keys():
					self.index[word] = dict()

				if doc.id not in self.index[word].keys():
					self.index[word][doc.id] = 0

				self.index[word][doc.id] += 1


	def boolean_request(self, request_words):
		if len(request_words) == 0:
			return set()

		# Si besoin, on separe en plusieurs requetes
		if 'and' in request_words or 'or' in request_words:

			try:
				and_index = request_words.index('and')
			except ValueError:
				and_index = float('inf')

			try:
				or_index = request_words.index('or')
			except ValueError:
				or_index = float('inf')

			first_op = min(and_index, or_index)

			ope, words1, words2 = request_words[first_op], request_words[:first_op], request_words[first_op+1:]

			if ope == 'and':
				return self.boolean_request(words1).intersection(self.boolean_request(words2))
			elif ope == 'or':
				return self.boolean_request(words1).union(self.boolean_request(words2))

		# Sinon, on verifie si il y a un NOT devant
		if request_words[0] == 'not':
			return set(self.docs.keys()).difference(self.boolean_request(request_words[1:]))

		# Sinon on renvoie les documents du mots
		try:
			return set(self.index[request_words[0]].keys())
		except KeyError:
			return set()



	def vectorize(self):

		vocab = list(self.index.keys())
		vocab.sort()

		# On cree les vecteurs pour toute la collection
		for doc in self.docs:
			self.vectors[doc.id] = [0] * len(vocab)

		# Puis on les peuple
		N = len(self.docs)
		for word in self.index.keys():
			df = sum(self.index[word].values())
			
			for doc in self.index[word].keys():
				voc_id = vocab.index(word)
				tf = self.index[word][doc]
				self.vectors[doc][voc_id] = (1 + log10(tf)) * log10(N / df)




	def vectorial_request(self, request_words):

		vocab = list(self.index.keys())
		vocab.sort()

		request_vector = [0] * len(vocab)

		N = len(self.docs)
		for word in request_words:
			try:
				voc_id = vocab.index(word)
				df = sum(self.index[word].values())
				tf = request_words.count(word)
				request_vector[voc_id] = (1 + log10(tf)) * log10(N / df)
			except ValueError:
				pass

		distances = dict()
		request_array = np.array(request_vector)

		for doc in self.docs:
			doc_array = np.array(self.vectors[doc.id])
			vdot = np.vdot(doc_array, request_array)
			if vdot != 0:
				distances[doc.id] = vdot / (np.linalg.norm(doc_array) * np.linalg.norm(request_array))

		result = sorted(distances.items(), key=operator.itemgetter(1), reverse=True)[:10]
		return [r[0] for r in result]


	# ===================================================
	# QUESTION 1
	def question1(self):
		tokens = 0
		for doc in self.docs:
			tokens += len(doc.terms)
		print(Color.GREEN + 'La collection ' + self.active_collection + ' contient ' + str(tokens) + ' tokens.\n' + Color.END)


	# ===================================================
	# QUESTION 2
	def question2(self):
		print(Color.GREEN + 'La taille du vocabulaire est ' + str(len(self.index)) + '.\n' + Color.END)


	# ===================================================
	# QUESTION 3
	def question3(self, to_print=True):
		# Full collection
		tokens = 0
		for doc in self.docs:
			tokens += len(doc.terms)
		vocab_size = len(self.index)

		# Half collection
		halfdocs = self.docs[:len(self.docs)//2]
		half_tokens = 0
		half_vocab = set()
		for doc in halfdocs:
			half_tokens += len(doc.terms)
			half_vocab = half_vocab.union(set(doc.terms))
		half_vocab_size = len(half_vocab)

		b = (log(vocab_size) - log(half_vocab_size)) / (log(tokens) - log(half_tokens))
		k = vocab_size / (tokens**b)

		if to_print:
			print(Color.GREEN + 'Collection complète :\n - Tokens : ' + str(tokens) + '\n - Vocab : ' + str(vocab_size) + '\n')
			print('Moitié de la collection :\n - Tokens : ' + str(half_tokens) + '\n - Vocab : ' + str(half_vocab_size) + '\n')

			print('Or M = kT^b\n')

			print('Donc b = ' + str(b) + ' et k = ' + str(k) + '\n' + Color.END)

		return k, b

	# ===================================================
	# QUESTION 4
	def question4(self):
		k, b = self.question3(to_print=False)

		print(Color.GREEN + 'Comme k = ' + str(k) + ' et b = ' + str(b) + ', ')
		print('la taille du vocabulaire pour 1 million de tokens serait ' + str(int(k*(1000000**b))) + '.\n' + Color.END)


	# ===================================================
	# QUESTION 5
	def question5(self):
		words = dict()
		for doc in self.docs:
			for term in doc.terms:
				if term not in words.keys():
					words[term] = 1
				else:
					words[term] += 1

		freqs = list(words.values())
		ranks = [i+1 for i in range(len(freqs))]
		freqs.sort(reverse=True)

		graph_menu = SelectMenu('Quel graphe ?', ['(f) en fonction de (r)', 'log(f) en fonction de log(r)'])
		graph_choice = graph_menu.run()

		# Graphe1 : f en fonction de r
		if graph_choice == 0:
			plt.plot(ranks, freqs)
			plt.ylabel('frequence')
			plt.xlabel('rang')
			plt.show()
		
		# Graphe2 : log(f) en fonction de log(r)
		elif graph_choice == 1:
			logrank = [log(rank) for rank in ranks]
			logfreq = [log(freq) for freq in freqs]
			plt.plot(logrank, logfreq)
			plt.ylabel('log(f)')
			plt.xlabel('log(r)')
			plt.show()