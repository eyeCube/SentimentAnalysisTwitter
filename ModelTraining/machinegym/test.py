
from textblob import TextBlob

def en_check(blob: TextBlob) -> bool: # is language of text English?
    return ( blob.detect_language()=='en' )

while(True):
    print(en_check(TextBlob(input())))
