import os
from Document import Document

from threading import Thread


class StanfordReader:

	# CONSTRUCTOR
	def __init__(self):
		self.common_words = []
		self.dir_path = os.path.dirname(__file__)
		self.docs = dict()


	def read_collection(self):
		path = self.dir_path + '/collections/cs276'

		self.read_common_words()

		thread_list = []
		id_start = 1

		for directory in os.listdir(path):
			if not directory.startswith('.'):
				thread_list.append(ReaderThread(self, path, directory, id_start))
				id_start += len(os.listdir(path + '/' + directory))

		for th in thread_list:
			th.start()

		for th in thread_list:
			th.join()
			self.docs.update(th.docs)


	# On recupere les common words de Cacm pour cette collection egalement 
	def read_common_words(self):

		with open(self.dir_path + '/collections/cacm/common_words', 'r') as common_words:

			word = common_words.readline().rstrip('\n')
			while word != '':
				self.common_words.append(word)
				word = common_words.readline().rstrip('\n')



class ReaderThread(Thread):

	def __init__(self, stanford_reader, path, dir_number, first_id):
		super().__init__()
		self.stanford_reader = stanford_reader
		self.path = path
		self.dir_number = dir_number
		self.docs = dict()
		self.id_generator = first_id


	def read_and_tokenize_doc(self, file_name):
		doc_reader = open(self.path + '/' + self.dir_number + '/' + file_name, 'r')
		doc = Document(self.id_generator)
		self.id_generator += 1
		doc.ref = str(self.dir_number) + ' - ' + file_name
		doc.summary = doc_reader.readline()
		doc.terms = doc.summary.split(' ')
		doc.stop_words(self.stanford_reader.common_words)
		self.docs[doc.id] = doc


	def run(self):
		for file_name in os.listdir(self.path + '/' + self.dir_number):
			self.read_and_tokenize_doc(file_name)
	