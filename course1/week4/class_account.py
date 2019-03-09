
class Value:

    def __init__(self):
        self.amount = 0

    def __get__(self, obj, obj_type):
        return self.amount

    def __set__(self, obj, value):
        self.amount = value * (1 - obj.commission)


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission
