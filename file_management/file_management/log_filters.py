import logging

class UserAndDocumentFilter(logging.Filter):
    def __init__(self, user = 'None', document = 'None', template = 'None', step = 'None', flow = 'None'):
        self.user = user
        self.document = document
        self.template = template
        self.step = step
        self.flow = flow

    def filter(self, record):
        wordsInMessage = record.msg.split()
        foundUser = False
        foundDocument = False
        foundTemplate = False
        foundStep = False
        foundFlow = False
        user = self.user
        document = self.document
        template = self.template
        step = self.step
        flow = self.flow
        for word in wordsInMessage:
            if foundUser:
                user = word
                foundUser = False
            if foundDocument:
                document = word
                foundDocument = False
            if foundTemplate:
                template = word
                foundTemplate = False
            if foundStep:
                step = word
                foundStep = False
            if foundFlow:
                flow = word
                foundFlow = False
            if word == 'User':
                foundUser = True
            if word == 'Document':
                foundDocument = True
            if word == 'Template':
                foundTemplate = True
            if word == 'Step':
                foundStep = True
            if word == 'Flow':
                foundFlow = True
        record.user = user
        record.document = document
        record.template = template
        record.step = step
        record.flow = flow
        return True