import requests
import bs4
from urllib.parse import urlparse



class Crawler():
  def __init__(self, start):
    self.start = start
    self.base = self.getBase()
    self.done = []
    self.todo = []
    self.todo.append(self.start)



  def getBase(self):
    newInit = ""
    init = self.start[::-1]
    if "//" in init:
      init = init[:init.index("//")]
    foundStop = False
    for letter in init:
      if letter in ["."]:
        if foundStop:
          return newInit[::-1]
        foundStop = True
      newInit += letter
    return newInit[::-1]


  
  def getLinks(self, URL):
    response = requests.get(URL)
    links = bs4.BeautifulSoup(response.text, 'html.parser').select("a")
    for link in links:
      if link.get('href') != None:
        linky = link.get("href")
        hostname = urlparse(linky).hostname
        if not hostname:
          continue
        if hostname.endswith(self.base):
          if linky not in self.done and linky not in self.todo:
            self.todo.append(linky)
          else:
            pass
    print(self.done)
    self.done.append(URL)


  def crawl(self):
    while True:
      url = self.todo[0]
      if url not in self.done:
        self.getLinks(url)
        self.todo.pop(0)
      if not self.todo:
        return self.done