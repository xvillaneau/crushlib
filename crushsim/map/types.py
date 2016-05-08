
class Types():

    def __init__(self):
        self.list = []

    def add(self, name, id):

        if self.exists(name=name):
            raise IndexError("Name '{}' is already taken".format(name))
        if self.exists(id=id):
            raise IndexError("ID #{} is already taken".format(id))

        type_obj = Type(name, id)
        self.list.append(type_obj)

    def get(self, name=None, id=None):

        # Argument checking
        if not (id is None or name is None):
            raise ValueError("Only id or name can be searched at once")
        if id is not None and type(id) is not int:
            raise TypeError("Argument 'id' expected to be an integer")
        if name is not None and type(name) not in (str, unicode):
            raise TypeError("Argument 'name' expected to be a string")
        if name is not None and name == "":
            raise ValueError("Argument 'name' cannot be an empty string")

        # Processing the actual request
        if id is not None:
            tmp = [t for t in self.list if t.id == id]
        elif name is not None:
            tmp = [t for t in self.list if t.name == name]
        else:
            return self.list

        if not tmp:
            raise IndexError("Could not find type with {}={}".format(
                'name' if name else 'id', name if name else id))
        return tmp[0]

    def exists(self, name=None, id=None):
        try:
            self.get(name=name, id=id)
        except IndexError:
            return False
        return True

    @staticmethod
    def create_set(type_list):

        if type(type_list) is not list:
            raise TypeError("Input must be a list of strings")
        for t in type_list:
            if type(t) not in (str, unicode):
                raise TypeError("Input must be a list of strings")

        if not type_list:
            raise ValueError("Input cannot be an empty list")
        if len(type_list) != len(set(type_list)):
            raise ValueError("All elements in input must be unique")

        types = Types()
        for t in type_list:
            types.add(t, type_list.index(t))
        return types


class Type():

    def __init__(self, name, id):
        if type(id) is not int:
            raise TypeError("Argument 'id' expected to be an integer")
        if type(name) not in (str, unicode):
            raise TypeError("Argument 'name' expected to be a string")
        if name == '':
            raise ValueError("Argument 'name' cannot be an empty string")

        self.name = name
        self.id = id
        self.buckets = []

    def link_bucket(self, bucket_obj):
        self.buckets.append(bucket_obj)
