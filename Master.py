__Author__  = 'Soumil Nitin Shah'
__Version__ = "0.0.1"
__Email__ = 'shahsoumil519@gmail.com'

try:
    import requests
    from bs4 import BeautifulSoup
    import json
    import sys
    import os
    import pandas as pd
    import sqlite3
    import datetime
    import logging
except Exception as e:
    print("Some Modules are Missing {}".format(e))


class Meta(type):

    """ singleton Design  Pattern  """

    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Meta, cls).__call__(*args, **kwargs)
            return cls._instance[cls]

class log(object):

    """ Create a Log File regarding Execution Time memory Address size etc """

    def __init__(self, func):
        """ Constructor  """
        self.func = func

    def __call__(self, *args, **kwargs):
        """ Wrapper Function """

        start = datetime.datetime.now()     # start time
        Tem = self.func(self, *args, **kwargs)    # call Function
        FunName = self.func.__name__        # get Function Name
        end = datetime.datetime.now()       # End time

        message = """                       # Form Message
            
            Function : {}
            Execution Time : {}
            Address : {}
            Memory: {} Bytes
            Date: {}
            Args: {}
            Kwargs {}
            
            """.format(FunName,
                       end-start,
                       self.func.__name__,
                       sys.getsizeof(self.func),
                       start, args, kwargs)

        cwd = os.getcwd()                       # get CWD
        folder = 'Logs'                         # Create Folder Logs
        newPath = os.path.join(cwd, folder)     # change Path

        try:
            """ try to create directory """
            os.mkdir(newPath)                   # create Folder
            logging.basicConfig(filename='{}/log.log'.format(newPath), level=logging.DEBUG)
            logging.debug(message)

        except Exception as e:

            """ Directory already exists """

            logging.basicConfig(filename='{}/log.log'.format(newPath), level=logging.DEBUG)
            logging.debug(message)

        return Tem

class UrlFetcher(object):

    __slots__ = ["headers", "url"]

    def __init__(self):
        self.headers = {'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'http://www.wikipedia.org/',
    'Connection': 'keep-alive'}

    def GetUrl(self, url = 'https://watchbase.com/apple/watch'):

        """
        Just Supply the URL for any watch
        :return: List of Url
        """

        self.url = url
        data = requests.get(url= self.url, headers = self.headers)
        print(data)
        soup = BeautifulSoup(data.text, 'html.parser')

        return [q["href"] for q in soup.findAll('a', href=True)]


class Watch(object):

    def __init__(self):
        pass

    def getData(self, url):
        data = requests.get(url)
        soup = BeautifulSoup(data.content,'lxml')
        content = soup.find('div',id='content')

        data_dict = {}
        for table in content.find_all('table', attrs={'class':'info-table'}):
            table_rows = table.find_all('tr')
            for tr in table_rows:
                for th in tr:
                    th = tr.find('th')
                    td = tr.find('td')
                    data_dict[th.text] = td.text

        desc = content.find('div' ,class_ = 'row')
        desc_head = desc.find_all('p')[1]
        data_dict['product_desc'] = desc_head.text[0:-21]

        brand_img_link = content.find('img',class_ = 'lazy pull-right brand-logo')['data-original']
        data_dict['brand_img_link'] =  brand_img_link

        prdct_img_link = content.find('img',class_ = 'thumb')['src']
        data_dict['prdct_img_link'] = prdct_img_link

        return data_dict


class Database(object):

    def __init__(self):
        pass

    @log
    def upload(self,url, data):

        self.conn = sqlite3.connect("Watch.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS watch 
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
         url TEXT,
         Data TEXT)""")

        self.cursor.execute("""INSERT INTO watch (url, Data) VALUES (?, ?)""", (url, data))

        print("Uploaded on Database ")

        self.conn.commit()
        self.cursor.close()
        self.conn.close()


class Facade(metaclass=Meta):

    def __init__(self):
        self._urlfetcher = UrlFetcher()
        self._watch = Watch()
        self._database = Database()

    def getUrl(self):

        data = self._urlfetcher.GetUrl()

        for c, x in enumerate(data):

            try:

                mdict = self._watch.getData(url=x)
                self._database.upload(url=str(x), data=str(mdict))
                print("Done ")
            except Exception as e:
                pass


if __name__ == "__main__":
    obj = Facade()
    print(obj.getUrl())
