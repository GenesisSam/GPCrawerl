# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import threading
import re
# start url
# https://play.google.com/store

depth = 0
datas = []
urls = []
thd_flag = False

thrd = []

f = "https://play.google.com"
uuu = [
    "/store/apps",
    "/store/apps/category/GAME",
    "/store/apps/category/FAMILY",
    "/store/apps/category/LIFESTYLE",
"/store/apps/category/COMICS",
"/store/apps/category/MEDIA_AND_VIDEO",
"/store/apps/category/BUSINESS",
"/store/apps/category/PHOTOGRAPHY",
"/store/apps/category/PRODUCTIVITY",
"/store/apps/category/SOCIAL",
"/store/apps/category/SHOPPING",
"/store/apps/category/SPORTS",
"/store/apps/category/ENTERTAINMENT",
"/store/apps/category/TRAVEL_AND_LOCAL",
"/store/apps/category/APP_WIDGETS",
"/store/apps/category/MUSIC_AND_AUDIO",
"/store/apps/category/MEDICAL",
"/store/apps/category/COMMUNICATION",
"/store/apps/category/ANDROID_WEAR",
"/store/apps/category/GAME",
"/store/apps/category/GAME_EDUCATIONAL",
"/store/apps/category/GAME_WORD",
"/store/apps/category/GAME_ROLE_PLAYING",
"/store/apps/category/GAME_BOARD",
"/store/apps/category/GAME_SPORTS",
"/store/apps/category/GAME_SIMULATION",
"/store/apps/category/GAME_ARCADE",
"/store/apps/category/GAME_ACTION",
"/store/apps/category/GAME_ADVENTURE",
"/store/apps/category/GAME_MUSIC",
"/store/apps/category/GAME_RACING",
"/store/apps/category/GAME_STRATEGY",
"/store/apps/category/GAME_CARD",
"/store/apps/category/GAME_CASINO",
"/store/apps/category/GAME_CASUAL",
"/store/apps/category/GAME_TRIVIA",
"/store/apps/category/GAME_PUZZLE",
"/store/apps/category/FAMILY",
"/store/apps/category/FAMILY?age=AGE_RANGE1",
"/store/apps/category/FAMILY?age=AGE_RANGE2",
"/store/apps/category/FAMILY?age=AGE_RANGE3",
"/store/apps/category/FAMILY_EDUCATION",
"/store/apps/category/FAMILY_BRAINGAMES",
"/store/apps/category/FAMILY_ACTION",
"/store/apps/category/FAMILY_PRETEND",
"/store/apps/category/FAMILY_MUSICVIDEO",
"/store/apps/category/FAMILY_CREATE",
    "/store/apps/category/HEALTH_AND_FITNESS",
    "/store/apps/category/PERSONALIZATION",
    "/store/apps/category/WEATHER",
    "/store/apps/category/TOOLS",
    "/store/apps/category/FINANCE",
    "/store/apps/category/EDUCATION",
    "/store/apps/category/TRANSPORTATION",
    "/store/apps/category/NEWS_AND_MAGAZINES",
    "/store/apps/category/BOOKS_AND_REFERENCE",
    "/store/apps/category/APP_WALLPAPER",
    "/store/apps/category/LIBRARIES_AND_DEMO",
"/store/apps/category/MEDIA_AND_VIDEO/collection/topselling_paid",
"/store/apps/category/MEDIA_AND_VIDEO/collection/topselling_paid",
"/store/apps/category/MEDIA_AND_VIDEO/collection/topselling_free",
"/store/apps/category/MEDIA_AND_VIDEO/collection/topselling_free"]


def main():
    global datas
    global urls
    global depth


    # url = "https://play.google.com/store/apps"

    for d in uuu:
        urls.append(f+d)

    while len(urls) > 0:

        url = urls.pop(0)

        print "\t[-] url left: %d" % len(urls)

        res = requests.get(url)

        if res.status_code == 200:
            html = res.text
            soup = BeautifulSoup(html, "html.parser")

            for d in soup.find_all("a"):
                d = d.get("href")

                p = re.compile(r"^/store/apps/details\?id=")
                p2 = re.compile(r"^/store/apps/[developer|dev]+\?id=")
                p3 = re.compile(r"^/store/apps/category/[a-zA-Z]+")

                if p.match(d):
                    datas.append(f+d)
                # elif p2.match(d):
                #     if len(urls) > 500:
                #         return
                #
                #     urls.append(f+d)
                #     urls = list(set(urls))
            print "[+] Added, %d" % len(datas)



def getData(name):

    while len(datas) > 0:
        i = datas.pop(0)
        print "\t[- %s] data left: %d" % (name, len(datas))
        if thd_flag == True:
            break

        r = requests.get(i)

        if r.status_code ==200:
            html = r.text
            soup = BeautifulSoup(html, "html.parser")

            with open('result.txt', 'a') as f:
                f.write("%s\n" % i)

                try:
                    f.write("[+] 제목: %s\n" % (soup.find("div", {"class":"id-app-title"}).text).encode("utf-8"))
                except AttributeError as err:
                    # 해당 하는 속성이 없을수도 있기 때문에에
                    pass

                try:
                    f.write("[+] 제작자: %s, 장르: %s\n" %(soup.find("span", {"itemprop":"name"}).text.encode("utf-8"), soup.find("span", {"itemprop":"genre"}).text.encode("utf-8")))
                except AttributeError as err:
                    # 해당 하는 속성이 없을수도 있기 때문에에
                    pass

                try:
                    f.write("[+] 평점: %s\n" % soup.find("div", {"class":"tiny-star star-rating-non-editable-container"}).get("aria-label").encode("utf-8"))
                except AttributeError as err:
                    # 해당 하는 속성이 없을수도 있기 때문에에
                    pass

                try:
                    f.write("[+] 평가 참가자수: %s\n" % soup.find("span", {"class":"reviews-num"}).text.encode("utf-8"))
                except AttributeError as err:
                    # 해당 하는 속성이 없을수도 있기 때문에에
                    pass

                try:
                    f.write("[+] 총평점: %s\n" % soup.find("div", {"class":"score"}).text.encode("utf-8"))
                except AttributeError as err:
                    # 해당 하는 속성이 없을수도 있기 때문에에
                    pass

                try:
                    f.write("[+] 업데이트일자: %s\n" % soup.find("div", {"itemprop":"datePublished"}).text.encode("utf-8"))
                except AttributeError as err:
                    # 해당 하는 속성이 없을수도 있기 때문에에
                    pass

                try:
                    f.write("[+] 파일크기: %s\n" % soup.find("div", {"itemprop":"fileSize"}).text.encode("utf-8"))
                except AttributeError as err:
                    # 해당 하는 속성이 없을수도 있기 때문에에
                    pass

                try:
                    f.write("[+] 다운수: %s\n" % soup.find("div", {"itemprop":"numDownloads"}).text.encode("utf-8"))
                except AttributeError as err:
                    # 해당 하는 속성이 없을수도 있기 때문에에
                    pass

                try:
                    f.write("[+] 콘텐츠등급: %s\n" % soup.find("div", {"itemprop":"contentRating"}).text.encode("utf-8"))
                except AttributeError as err:
                    # 해당 하는 속성이 없을수도 있기 때문에에
                    pass

                f.write("\n")

def thr():

    for i in range(0, 5):
        print "==============================="
        print "[+] Thread created and run"
        print "==============================="
        thrd.append(threading.Thread(target=getData, args=(str(i))).start())

    for i in range(0, len(thrd)):
        try:
            thrd[i].join()
        except AttributeError as err:
            pass

    print "[+] All process work done"


if __name__=="__main__":
    try:
        main()
        datas = list(set(datas))
        print "[+] %d data start." % len(datas)
        thr()
    except KeyboardInterrupt as err:
        import sys
        thd_flag = True
        sys.exit(1)