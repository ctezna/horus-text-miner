class Appearance:
    """
    Represents the appearance of a term in a given document, along with the
    frequency of appearances in the same one.
    """
    def __init__(self, docId, frequency, idf=0):
        self.docId = docId
        self.frequency = frequency
        self.tfidf = idf * frequency
        
    def __repr__(self):
        """
        String representation of the Appearance object
        """
        return str(self.__dict__)


from json import JSONEncoder
class AppearanceEncoder(JSONEncoder):
    """
    Used to encode Appearance object to JSON
    """
    def default(self, o):
        return o.__dict__ 