__Author__ = "soushah@my.bridgeport.edu"
__verison__ = '0.0.1'


try:
    import pandas as pd
    import ssl
    import os
    import datetime
    import logging
    import functools
    import sys
except Exception as e:
    print("Some Modules are missings ")


class Meta(type):

    _instance = {}      # class Variable

    def __call__(cls, *args, **kwargs):
        """ if instance already exist dont create one  """

        if cls not in cls._instance:
            cls._instance[cls] = super(Meta, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class Watch(object):

    __slots__ = ["url"]

    def __init__(self):
        self.url = "http://watchbase.com/tissot/t-classic/t063-610-16-057-00"

    @property
    def get(self):
        """

        :return: Description, case , Dial ,  Movement
        """
        df = pd.read_html(self.url, header=0)
        description = df[0]
        case = df[1]
        Dial = df[2]
        Movement = df[3]

        Description = list(zip(description["Brand:"].to_list(),description["Tissot"].to_list()))
        case = list(zip(case["Material:"].to_list(),case["Stainless steel"].to_list()))
        Dial = list(zip(Dial["Color:"].to_list(),Dial["Black"].to_list()))
        Movement = list(zip(Movement["Type:"].to_list(),Movement["Quartz"].to_list()))

        return Description, case, Dial, Movement


class Facade(metaclass=Meta):

    def __init__(self):
        self._watch = Watch()

    def getData(self):
        Description, case, Dial, Movement = self._watch.get
        return Description, case, Dial, Movement


if __name__ == "__main__":
    obj = Facade()
    Description, case, Dial, Movement  = obj.getData()
    print(Description)