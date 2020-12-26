from PyQt5.QtCore import *
import random
import requests
from bs4 import BeautifulSoup

class Worker(QThread):

    finished = pyqtSignal(list)

    def __init__(self):
        self.keyword = list()
        self.blog_url_list = list()
        super(Worker, self).__init__()
        self.is_PC = True
        self.is_test = 1

    def run(self):
        temp_blog_soonwi = self.crawl(self.keyword,self.blog_url_list)
        self.finished.emit(temp_blog_soonwi)
        self.msleep(3000)

    def crawl(self,keyword, blog_url_list):
        temp_blog_soonwi = [0 for i in range(len(blog_url_list))]
        if self.is_test == 1:
            rand_k = random.randrange(1,9)
            temp_blog_soonwi = [rand_k for i in range(len(blog_url_list))]
            print(keyword + " : " + str(temp_blog_soonwi))
        else :
            if self.is_PC:
                url = "https://search.naver.com/search.naver?sm=mtp_hty.top&where=m&query="+keyword.replace(" ","+")
                source = requests.get(url).text
                soup = BeautifulSoup(source, "html.parser")
                source1 = soup.select("section.sp_nreview")

                if len(source1)>0:
                    source2 = source1[0].ul.find_all('li')
                    index_view_blog = 0
                    for key in source2:
                        blog_url = key.select("div.total_sub")[0].a['href']
                        index_blog_url = 0
                        for key in blog_url_list:
                            if key in blog_url:
                                temp_blog_soonwi[index_blog_url] = index_view_blog+1
                            index_blog_url += 1
                        if index_view_blog >= 6:
                            break
                        index_view_blog += 1
            else:
                url = "https://m.search.naver.com/search.naver?sm=mtp_hty.top&where=m&query="+keyword.replace(" ","+")
                source = requests.get(url).text
                soup = BeautifulSoup(source, "html.parser")
                source1 = soup.select("section.sp_nreview")

                if len(source1)>0:
                    source2 = source1[0].ul.find_all('li')
                    index_view_blog = 0
                    for key in source2:
                        blog_url = key.select("div.total_sub")[0].a['href']
                        index_blog_url = 0
                        for key in blog_url_list:
                            if key in blog_url:
                                temp_blog_soonwi[index_blog_url] = index_view_blog+1
                            index_blog_url += 1
                        if index_view_blog >= 6:
                            break
                        index_view_blog += 1
            print(keyword + " : " + str(temp_blog_soonwi))
        return temp_blog_soonwi