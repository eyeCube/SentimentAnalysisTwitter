
class TrainingData:
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            self.__dict__[k] = v

t=TrainingData(
    k='blime', f='nig', g=1
    )
print(t.k)
print(t.f)
print(t.g)
