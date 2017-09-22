from selenium import webdriver
from urllib import parse
from bs4 import BeautifulSoup
import urllib.request
import json
import random


def getPic(search):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        url = "https://www.google.com/search?tbm=isch&q=" + search
        driver.get(url)

        element = driver.find_element_by_id('rg_s')
        a = element.find_element_by_tag_name('a')
        href = str(parse.unquote(a.get_attribute('href')))

        piclink0 = href.find("imgurl=", 0, len(href)) + 7
        piclink1 = href.find("&", piclink0, len(href))
        # all fucked up when it comes to parsing different words pages
        piclink = href[piclink0:piclink1]
        if "?" in piclink:
            piclink1 = piclink.find("?", 0, len(piclink))
            piclink = piclink[0:piclink1]
            # piclink.replace("?", "")
        picextension = piclink[piclink.rfind(
            ".", 0, len(piclink)): len(piclink)]

        print(piclink)

        f = open('images\pic' + picextension, 'wb')
        # f.flush()
        # f.write(urllib.request.urlopen(piclink).read())
        # f.close()
    except:
        driver.close()
        print("ERROR in getPic() trying again")
        getPic(search)

    driver.close()
    return piclink


def dlPic(piclink):
    picextension = piclink[piclink.rfind(
        ".", 0, len(piclink)): len(piclink)]
    f = open('images\pic' + picextension, 'wb')
    f.flush()
    req = urllib.request.Request(piclink, headers={'User-Agent': 'Mozilla/5.0'})
    openurl = urllib.request.urlopen(req)
    r = openurl.read()
    f.write(r)
    f.close()
    return picextension


def getTweet(search):
    url = "http://www.dictionary.com/browse/" + search
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, 'lxml')
    data = soup.find_all("meta")
    definition = str(data[len(data) - 2])
    def0 = definition.find(",", 0, len(definition)) + 2
    def1 = definition.find(".", 0, len(definition))
    definition = definition[def0:def1]
    definition = definition.replace("(", "")
    print(definition)
    return search + " - " + definition


def outputJson(tweet, picextension):
    out = {
        'tweet': tweet,
        'filename': "images\pic" + str(picextension)
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



searchword = getWord()
scrape(searchword)
# getPic("mommy")
# getTweet("boy")
# print("spleeping....")
# time.sleep(3)
print("scraper ended.")
