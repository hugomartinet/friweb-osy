import os

from Document import Document


class CacmReader:

	important_tags = ['.I', '.T', '.W', '.K']

	# CONSTRUCTOR
	def __init__(self):
		self.file_path = os.path.dirname(__file__)
		self.common_words = []
		self.file = None
		self.current_line = ''
		self.finished = False

	
	# METHODS
	# needs to be used before any other method
	def open_cacm_file(self):
		self.file = open(self.file_path + '/collections/cacm/cacm.all', 'r')
		self.read_next_line()


	# reads the next line in the doc
	def read_next_line(self):
		try:
			self.current_line = self.file.readline().rstrip('\n')
		except AttributeError:
			raise CacmReaderError('You did not open any file.')


	# determines if the reader is located on a tagged line
	def is_on_tagged_line(self):
		try:
			return self.current_line[0] == '.'
		except IndexError:
			self.file.close()
			self.finished = True
			return True


	# reaches the next tag in text
	def go_to_next_tag(self):
		text = ''
		self.read_next_line()
		while not self.is_on_tagged_line():
			text += self.current_line + ' '
			self.read_next_line()
		return text


	# creates the next document object from file
	def build_next_document(self):

		try:
			new_doc = Document(int(self.current_line[3:]))
		except ValueError:
			raise CacmReaderError('Cannot find doc_id in line : ' + self.current_line)
		finally:
			self.go_to_next_tag()
		
		while True:

			current_tag = self.current_line[:2]

			# if not an important tag, pass this one
			if current_tag not in CacmReader.important_tags:
				if current_tag == '':
					break

				self.go_to_next_tag()
				continue

			# if .I, it means we reached the next document
			if current_tag == '.I':
				break

			elif current_tag == '.T':
				new_doc.title = self.go_to_next_tag()

			elif current_tag == '.W':
				new_doc.summary = self.go_to_next_tag()

			elif current_tag == '.K':
				new_doc.keywords = self.go_to_next_tag().split(',')

		new_doc.ref = str(new_doc.id) + ' - ' + str(new_doc.title)
		
		return new_doc


	
	# creates the list of common words to remove
	def read_common_words(self):

		with open(self.file_path + '/collections/cacm/common_words', 'r') as common_words:

			word = common_words.readline().rstrip('\n')
			while word != '':
				self.common_words.append(word)
				word = common_words.readline().rstrip('\n')
			






class CacmReaderError(Exception):

	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message