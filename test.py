from base64 import encode
from distutils import errors
from lib2to3.pgen2 import parse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import subprocess
import os
from urllib.parse import urlparse
import re
from pathlib import PurePosixPath

def getBeforePath(parsedURL):
    return parsedURL.scheme+ '://'+ parsedURL.netloc
'''
getPath=urlparse(e)
pth=parse.path
normalizedPath=''
print(os.path.split(pth)[1])
'''
a="https://codesque.github.io"
a1="hat.html"
a2="kat.html"
a3="sat.html"
b="https://docs.python.org/3/library/sfwef/wdsgh/shdhy/fg/sdf/urllib.parse.html"
c="https://codesque.github.io/BMGproje/"
d="http://metehansozenli.orgfree.com/index.html"
e="http://abdulkadiryildirim1745.eu5.org/"
list=[a,b,c,d,e]
alist=[a1,a2,a3]
normalizedLinks=[]
parse=urlparse(d)
pth=parse.path
normalizedPath=''
print(os.path.split(pth)[1])


for i in list:
    getParse=urlparse(i)
    pth=getParse.path
    normalizedPath=''
    if not re.search(r'^/',str(getParse.path)):
        normalizedPath+='/'+str(getParse.path)
        i= getBeforePath(getParse)+ normalizedPath
    normalizedLinks.append(i)
print(normalizedLinks)


