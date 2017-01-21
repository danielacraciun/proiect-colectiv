import logging

class UserAndDocumentFilter(logging.Filter):
	def __init__(self, user = 'None', document = 'None'):
		self.user = user
		self.document = document

	def filter(self, record):
		wordsInMessage = record.msg.split()
		foundUser = False
		foundDocument = False
		user = self.user
		document = self.document
		for word in wordsInMessage:
			if foundUser:
				user = word
				foundUser = False
			if foundDocument:
				document = word
				foundDocument = False
			if word == 'User':
				foundUser = True
			if word == 'Document':
				foundDocument = True

		record.user = user
		record.document = document
		return True