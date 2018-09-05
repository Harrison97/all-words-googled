from selenium import webdriver
from urllib import parse
from bs4 import BeautifulSoup
import urllib.request
import json
import random
from selenium.webdriver.support.ui import WebDriverWait


def getPic(search):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
#    url = "https://www.google.com/search?tbm=isch&q=" + search
    url = "https://duckduckgo.com/?q=" + search + "&iax=images&ia=images"
    driver.get(url)


    


#    while True:
#        try:
#            driver.find_element_by_xpath('//*[@id="rg_s"]/div[1]/a').click()
#            break
#        except:
#            print("trying to click...")

    while True:
        try:
            piclink = driver.find_element_by_xpath('//*[@id="zci-images"]/div[1]/div[2]/div/div[1]/div[1]/span/img').get_property('src')
            break
        except:
            print("trying to get href...")
   
    print("LINK:" + str(piclink))   
    if "." in piclink[len(piclink) - 5:len(piclink)]:
        picextension = piclink[piclink.rfind(
            ".", 0, len(piclink)): len(piclink)]
    else:
        picextension = ".png"
    
    print(piclink)
    print(picextension)
    driver.quit()
    return piclink

def dlPic(piclink):
    if "." in piclink[len(piclink) - 5:len(piclink)]:
        picextension = piclink[piclink.rfind(
            ".", 0, len(piclink)): len(piclink)]
    else:
        picextension = ".png"
    f = open('pic' + picextension, 'wb')
    f.flush()
    req = urllib.request.Request(
        piclink, headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'})
    openurl = urllib.request.urlopen(req)
    r = openurl.read()
    f.write(r)
    f.close()
    return picextension


def getTweet(search):
    url = "http://www.dictionary.com/browse/" + search
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, 'lxml')
    #print(soup)
    data = soup.find_all("meta")
    #print(data)
    definition = str(data[1])
    #print(definition)
    def0 = definition.find(",", 0, len(definition)) + 2
    def1 = definition.find(".", 0, len(definition))
    definition = definition[def0:def1]
    definition = definition.replace("(", "")
    if definition[-1].isdigit():    definition = definition[:-1]
    print(definition)
    return search + " - " + definition


def outputJson(tweet, picextension):
    out = {
        'tweet': tweet,
        'filename': "pic" + str(picextension)
    }

    # if os.path.isfile('data.json'):
    #     os.remove('data.json')

    f = open('data.json', 'w')
    f.flush()
    f.write(json.dumps(out))
    f.close()
    # print("OMMGGGGG")
    # while True:s
    #     if os.path.isfile('data.json'):
    #         break


def getWord():
    wordlist = "wordlist.txt"
    usedwordlist = "usedwords.txt"

    f = open(wordlist, 'r+')
    a = f.readlines()
    random.seed(a=None)
    i = random.randrange(0, len(a), 1)
    word = a[i]
    f.seek(0)
    a = f.read()
    # a = a.replace(word + "\\n", "")
    f.close()

    f = open(usedwordlist, 'a')
    f.write(word)
    f.close()

    f = open(wordlist, 'w')
    f.truncate()
    f.write(a)
    f.close()

    a = ""
    filein = open(wordlist)
    for line in filein:
        line = line.replace(word, "")
        a = a + line
    filein.close()
    fileout = open(wordlist, "w+")
    fileout.write(a)
    fileout.close()

    return word.replace("\n", "")


def scrape(search):
    print("searching pic : " + search)
    picextension = dlPic(getPic(search))
    print("searching tweet : " + search)
    tweet = getTweet(search)
    if len(tweet) > 140:
        tweet = tweet[0:tweet.find(";", 0, len(tweet))]
    outputJson(tweet, picextension)
    print(tweet)


searchword = getWord()
scrape(searchword)
# getPic("mommy")
#getTweet("daddy")
# print("spleeping....")
# time.sleep(3)
print("scraper ended.")

