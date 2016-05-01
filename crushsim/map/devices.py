
class Devices():

    def __init__(self):
        self.list = []

    def add(self, num=None):

        if not num:
            num = self.get_next_number()

        try:
            num = int(num)
            if num < 0:
                raise ValueError
        except ValueError:
            raise ValueError(
                "Devices must be identified by a positive integer")

        if num not in self.list:
            self.list.append(num)
        else:
            raise IndexError("Device {} already exists".format(num))

        return num

    def get_next_number(self):

        if not self.list:
            return 0

        candidates = [x for x in range(0, max(self.list) + 2)
                      if x not in self.list]
        return min(candidates)
