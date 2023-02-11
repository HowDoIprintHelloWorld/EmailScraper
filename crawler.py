import requests
import bs4
from urllib.parse import urlparse
import threading



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
    self.done.append(URL)
    self.todo.pop(0)
    print('\rURLs scanned: ({}/{});   Active threads: {}'.format(str(len(self.done)), str(len(self.todo) + len(self.done)), str(threading.active_count())),end='',flush=True)


  def crawl(self):
    while True:
      url = self.todo[0]
      if url not in self.done:
        #self.getLinks(url)
        threads = []
        for _ in range(8):
          x = threading.Thread(target=self.getLinks, args=(url,), daemon=True)
          x.start()
          threads.append(x)
          #self.todo.pop(0)
        for i, x in enumerate(threads):
          x.join()
      if not self.todo:
        print("")
        return self.done