
class Tunables():

    def __init__(self):
        self.settings = {}
        self.preset = None

    def update_setting(self, name, value):
        self.settings.setdefault(name, None)
        self.settings[name] = value
