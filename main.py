from crawler import Crawler

from requests import get
import re    


def getHtml(site):
  return get(site).text


def getEmails(html):
  atIndx = 0
  emailList = []
  try:
    while True:
      html = html[atIndx:]
      atIndx = html.index("@") + 1
      emails = re.findall(r"(([a-z|A-Z])+@+.+\.+([a-z]|[A-Z]){2,})", html[atIndx-50:atIndx+50])
      if not emails: continue
      emails = emails[0][0]
      emailList.append(emails)
  except Exception as e:    
    emailList = validateEmailList(emailList)
    return emailList




def validateEmailList(emailList):
  newEmailList = []
  for email in emailList:
    if email.endswith(BASE):
      newEmailList.append(email)
  return newEmailList







if __name__ == "__main__":
  new = old = emailList = []
  INIT = input("URL>>    ")
  crawler = Crawler(INIT)
  crawler.getBase()
  BASE = crawler.base
  urls = crawler.crawl()
  print("URL-count: ", len(urls))
  emailList = []
  for url in urls:
    html = getHtml(INIT)
    emailList += getEmails(html)
  print("\n".join(emailList))
  