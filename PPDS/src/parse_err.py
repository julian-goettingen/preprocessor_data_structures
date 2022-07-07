class PPDSParseError(Exception):

    def __init__(self, reason, detail="", filename=None, position=None):
        # filename None means current file
        self.reason = reason
        self.detail = detail
        self.position = position

class ErrorContext():

    def __init__(self, filename, lineno, line):
        self.filename = filename
        self.lineno = lineno
        self.line = line
    
    def set_lineno(self, newlineno):
        self.lineno = newlineno

