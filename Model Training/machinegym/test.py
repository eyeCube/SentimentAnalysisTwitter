
# generic
def _issentiment(func):
    def inner(*args, **kwargs):
        print("hi!")
        print(args[0])
        return func(*args, **kwargs)
    return inner
    
# happy
@_issentiment
def ishappy(text):
    print("yo.")

ishappy("blah~")
