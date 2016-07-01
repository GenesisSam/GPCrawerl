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

def main():
    global datas
    global urls
    global depth


    # url = "https://play.google.com/store/apps"
    urls.append("https://play.google.com/store/apps")

    while len(urls) > 0:

        for url in urls:

            urls.pop(0)

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
                    elif p2.match(d) or p3.match(d):
                        if len(urls) > 500:
                            return

                        urls.append(f+d)
                        urls = list(set(urls))
                print "[+] Added, %d" % len(datas)

def getData(name):
    for i in datas:
        datas.pop(0)
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

        if len(thrd) < 5:
            if len(thrd) >= 0 and len(thrd) <= 5:
                print "==============================="
                print "[+] Thread created and run"
                print "==============================="
                thrd.append(threading.Thread(target=getData, args=(str(i))).start())
            else:
                pass

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