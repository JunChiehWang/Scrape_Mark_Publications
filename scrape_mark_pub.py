#
#  This python3 script scrapes Prof. Kushner's publiation webpage
#  (http://uigelz.eecs.umich.edu/publications.html)
#  and download the papers
#
#  usage: python3 ./scrape_mark_pub.py -D=Y 
#         -D=Y: download the paper
#         -D=N (default): don't download the papers
#
#  Jun-Chieh Wang
#  2017.11.20
#
#
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import sys
########################################
def getTitle(url):
    try:
        html = urlopen(url)       
    except HTTPError as e:
        print(e)
        return None
    try:
        bsObj = BeautifulSoup(html.read(),"html5lib")
        title = bsObj.body.h1
#       if the tag "body" doesnt exist => AttributeError         
    except AttributeError as e:
        return None
    return title
########################################
def getPaperList(url):
    html = urlopen(url)       
    try:
        bsObj = BeautifulSoup(html,"html.parser")
#       list of all papers (including titles and links)       
        List = bsObj.body.findAll("ol", {"class":"list"})[0].findAll('li')
#       link/path of all papers (../pub/articles/*.pdf)       
        Link = bsObj.findAll("a",{"href":re.compile("\.\.\/pub\/articles/.*\.pdf")})
    except: 
        return None
    return List, Link
########################################
#
website = "http://uigelz.eecs.umich.edu/publications.html"
#
########################################
# User default
#########################################
download="N"
########################################
#  Parse command line arguments
########################################
for arg in sys.argv:
    if arg.upper().find("-D=") > -1:
        temp = arg.find("=")
        download = arg[temp+1:]
########################################
#  Get title 
########################################
title = getTitle(website)
if title == None:
    print("Title could not be found")
    exit()    
else:
    print(title.get_text())
    print('----------------')
########################################
#  Get paper list
########################################
PaperList, PaperLink = getPaperList(website)
if PaperList == None:
    print("Paper list could not be found")
    exit()
elif PaperLink == None:
    print("Paper link could not be found")
    exit()        
else:
    listFile='paper_list.txt'
    fout = open(listFile,'w')
    for indx, paper in enumerate(PaperList):
#        
#       extract titles of the papers
#
        title = paper.get_text().strip()
        write_line = str(indx+1) + '\n' + 'Title: \n' + title + '\n'
        fout.write(write_line)
#        
#       extract link of the paper
#
        try:
            path = str(paper).split('href="')[1].split('"')[0]
#            write_line = 'path: \n' + path + '\n' 
#            fout.write(write_line)            
            FileName = path.split("articles/")[1]
            FilePath = "http://uigelz.eecs.umich.edu/pub/articles/"+FileName
            write_line='Absolute path: \n' + FilePath + '\n'
            fout.write(write_line)
            if download.upper() == "Y":
                urlretrieve (FilePath,FileName)
        except:
            write_line = 'path: \n' + 'No link found' +  '\n' 
            fout.write(write_line)
            write_line='absolute path: \n' + 'No link found' + '\n'
            fout.write(write_line)            

        write_line = '----------------\n'
        fout.write(write_line)
#
write_line = '\n' + str(indx+1) + ' papers have been found'
fout.write(write_line)
#
#    we can use this methode to get all links of papers and download them too : 
#    for file in PaperLink:
#        FileName = file["href"].split("articles/")[1]
#        FilePath = "http://uigelz.eecs.umich.edu/pub/articles/"+FileName
#        print(FilePath)
#        urlretrieve (FilePath,FileName)
#        print ('----------------')
#
