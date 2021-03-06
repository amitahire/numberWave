#!/usr/bin/env python


from spider import *
sys.path.append("..")
from utils import Utils

class ProjectPaperSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.utils = Utils()
        self.school = "project-papers"

    def doWork(self):
        self.getWastonPapers()
        self.getSTAIRPapers()
        self.getSTARTPapers()
        self.getSparkPapers()
        self.getHadoopPapers()
        #self.getRoboBrainPapers()
        self.getMobileEyePapers()
        self.getAutonomousDrivingPapers()

        self.getCALOPapers()
    def getCALOPapers(self):
        r = requests.get('http://www.ai.sri.com/pubs/search.php?project=179')
        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name("eecs/" + self.school + "/" + "CALO", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all('li'):
            title = li.p.strong.text.strip()
            link = 'http://www.ai.sri.com' + li.p.a['href']
            print title
            self.count += 1
            self.write_db(f, 'calo-' + str(self.count), title, link)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getAutonomousDrivingPapers(self):
        r = requests.get("http://driving.stanford.edu/papers.html")
        soup = BeautifulSoup(r.text)
        title = ""
        author = ""
        journal = ""
        desc = ""
        url = ""
        file_name = self.get_file_name("eecs/" + self.school + "/" + "AutonomousDriving", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        for p in soup.find_all("p"):
            if p.span != None:
                sp = BeautifulSoup(p.prettify())
                title = sp.find('span', class_='papertitle').text.strip()
                author = "author:" + self.utils.removeDoubleSpace(sp.find('span', class_='authors').text.strip().replace('\n', '')) + " "
                journal = "journal:" + sp.find('span', class_='meeting').text.strip()
                journal += " " + sp.find('span', class_='year').text.strip() + " "
                desc = "description:" +  self.utils.removeDoubleSpace(sp.find('span', class_='summary').text.strip().replace('\n', ''))
            if p.a != None and p.a['href'].find(".pdf") != -1:
                if p.a['href'].startswith('http'):
                    url = p.a['href']
                else:
                    url = 'http://driving.stanford.edu/' + p.a['href']
                self.count += 1
                self.write_db(f, "autonomousdriving-paper-" + str(self.count), title, url, author + journal + desc)
                title = ""
                author = ""
                journal = ""
                desc = ""
                url = "" 
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getMobileEyePapers(self):
        file_name = self.get_file_name("eecs/" + self.school + "/" + "MobileEye", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for i in range(1, 3):
            r = requests.get("http://www.mobileye.com/technology/mobileye-research/page/" + str(i))
            soup = BeautifulSoup(r.text)

            for div in soup.find_all("div", class_="ContentItemText"):
                title = div.h2.text.strip()
                link = div.h2.a['href']
                author = "author:" + div.p.text.strip()
                print title
                self.count += 1
                self.write_db(f, "mobileeye-paper-" + str(self.count), title, link, author)
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getHadoopPapers(self):
        r = requests.get("http://wiki.apache.org/hadoop/Papers")
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name("eecs/" + self.school + "/" + "hadoop", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all("li"):
            if li.p != None:
                print li.p.a.text
                self.count += 1
                self.write_db(f, "hadoop-paper-" + str(self.count), li.p.a.text, li.p.a["href"])

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getSparkPapers(self):
        r = requests.get("http://spark.apache.org/documentation.html")
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name("eecs/" + self.school + "/" + "spark", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all("li"):
            if li.a != None and li.a["href"].find("pdf") != -1 and li.em != None:
                title = li.a.text
                author =  "author:" + li.prettify()[li.prettify().find('</a>') + 7: li.prettify().find('<em>')].strip() + " "
                journal = "journal:" + li.em.text
                print title
                self.count += 1
                self.write_db(f, "spark-paper-" + str(self.count), title , li.a["href"], author + journal)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"



    def getSTARTPapers(self):
        r = requests.get("http://start.mit.edu/publications.php")
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name("eecs/" + self.school + "/" + "START", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
       
        link = ""
        title = ""
        journal = ""
        author = ""
        for td in soup.find_all("td"):
            if td.a != None and td.strong == None and td.a["href"] != "index.php":
                print ""
                if td.a["href"].find("http") == -1:
                    link = "http://start.mit.edu/" + td.a["href"]
                else:
                    link = td.a["href"]
                print link
            else:
                if td.strong != None:
                    if td.em != None:
                        journal = "journal:" + td.em.text + " "
                        print journal
                    if td.strong != None:
                        title = td.strong.text
                        print title
                else:
                    if td.em != None:
                        title = td.em.text
                        print title
                if td.text.find(".") != -1:
                    author = "author:" + td.text[0 : td.text.find(".")] + " "
                    print author
                    print ""
                    self.count += 1
                    self.write_db(f, "start-paper-" + str(self.count), title, link, author + journal)
                    title = ""
                    link = ""
                    author = ""
                    journal = ""

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getSTAIRPapers(self):
        r = requests.get("http://stair.stanford.edu/papers.php")
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name("eecs/" + self.school + "/" + "STAIRP", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all("li"):
            title = ""
            link = ""
            if li.span == None:
                continue
            title = li.span.text
                
            if li.a != None:
                link = li.a['href']
            self.count += 1
            self.write_db(f, "STAIRP-paper-" + str(self.count), title, link)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getRoboBrainPapers(self):
        r = requests.get("http://robobrain.me/#/about")
        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name("eecs/" + self.school + "/" + "robotbrain", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        print r.text
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


    def getWastonPapers(self):
        r = requests.get('http://researcher.watson.ibm.com/researcher/view_group_pubs.php?grp=2099')
        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name("eecs/" + self.school + "/" + "waston", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for div in soup.find_all("div", class_="publication"):
            link = ""
            authors = ""
            journal = ""
            title = div.h4.text.strip()
            if div.h4.a != None:
                link = div.h4.a['href']
            sp = BeautifulSoup(div.prettify())
            count = 0
            for span in sp.find_all("span", class_="pubspan"):
                count += 1
                data = self.utils.removeDoubleSpace(span.text.strip().replace("\n", ""))
                if count == 1:
                    authors = "author:" + data + " "
                if count == 2:
                    journal = "journal:" + data
            print title
            print authors
            print journal
            print link
            self.count += 1
            self.write_db(f, "waston-paper-" + str(self.count), title, link, authors + journal)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = ProjectPaperSpider()
start.doWork()
