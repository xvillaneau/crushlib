
class Devices():

    def __init__(self):
        self.list = []

    def add(self, num):
        if type(num) is not int or num < 0:
            raise ValueError(
                "Devices must be identified by a positive integer")

        if num not in self.list:
            self.list.append(num)
        else:
            raise IndexError("Device {} already exists".format(num))

    def get_next_number(self):

        if not self.list:
            return 0

        candidates = [x for x in range(0, max(self.list) + 2)
                      if x not in self.list]
        return min(candidates)
