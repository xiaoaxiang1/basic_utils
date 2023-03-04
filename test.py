class Iterator:
    def __init__(self, it):
        self.it = it
        print("Iterator init called")
    
    def __next__(self):
        print("Iterator next called")
        return next(self.it)

class IterObj:
    def __init__(self, it):
        self.it = it
        print("IterObj init called")
    
    def __iter__(self):
        print("IterObj iter called")
        return Iterator(iter(self.it))

for i in Iterator([1,2,3]):
    print(i)