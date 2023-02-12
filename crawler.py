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
    if not URL:
      return
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
    self.done.append(URL)
    if self.todo:
      self.todo.pop(0)
    print('\rURLs scanned: ({}/{});   Active threads: {};'.format(str(len(self.done)), str(len(self.todo) + len(self.done)), str(threading.active_count())),end='',flush=True)


  def cutDupes(self):
    self.done = list(set(self.done))


  def checkDone(self):
    if not self.todo:
        for i, x in enumerate(self.threads):
          x.join()
        print("")
        self.cutDupes()
        with open("crawlresults/"+self.base + ".txt", "w") as f:
            for url in self.done:
                f.write(url+"\n")
        return True
    return False



  def crawl(self):
    self.threads = []
    while True:
      if len(self.threads) >= 10:
        self.threads = [x for x in self.threads if x.is_alive()]
        continue
      if self.checkDone():
        return self.done
      url = self.todo[0]
      if url not in self.done:
        #self.getLinks(url)
        x = threading.Thread(target=self.getLinks, args=(url,), daemon=True)
        x.start()
        self.threads.append(x)
          #self.todo.pop(0)
      if self.checkDone():
        return self.done
