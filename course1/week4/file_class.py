
import tempfile
import os


class File:

    def __init__(self, path):
        self.path = path

    def write(self, text):
        with open(self.path, 'w') as file:
            file.write(text)

    def __add__(self, obj):
        with open(os.path.join(tempfile.gettempdir(), "new_obj.txt"), 'w') as new_obj, \
                open(self.path) as first, open(obj.path) as second:
            result = first.read() + second.read()
            new_obj.write(result)

        return File(os.path.join(tempfile.gettempdir(), "new_obj.txt"))

    def __iter__(self):
        with open(self.path) as file:
            self.textlines = file.readlines()
            self.current = 0
            self.end = len(self.textlines)
        return self

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration

        result = self.textlines[self.current]
        self.current += 1
        return result

    def __str__(self):
        return self.path

