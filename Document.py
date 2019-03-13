from nltk import wordpunct_tokenize, word_tokenize
import re


class Document:

	# CONSTRUCTOR
	def __init__(self, id):
		self.id = id
		self.ref = ''
		self.title = ''
		self.summary = ''
		self.keywords = []
		self.terms = []


	# METHODS
	def __repr__(self):
		return 'doc %s\n    title - %s\n    summary - %s\n    keywords - %s\n\n' % (self.id, self.title, self.summary, self.keywords)


	def tokenize(self):
		words = []
		words += word_tokenize(self.title.lower())
		words += word_tokenize(self.summary.lower())
		for word in words:
			term = re.sub(r'[^\w\s]', '', word)
			if term != '':
				self.terms.append(term)

	
	def stop_words(self, common_words):
		for common in common_words:
			if common in self.terms:
				self.terms.remove(common)