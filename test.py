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
import urllib.request
import requests

'''
getPath=urlparse(e)
pth=parse.path
normalizedPath=''
print(os.path.split(pth)[1])


saveFile = open(fileName,"w")
saveFile.write(str())
saveFile.close()
'''
a="iotherpages-favpages-aciktekerlek-f1.html"
cwd=os.getcwd()
os.mkdir("A")
os.chdir(cwd+"/"+"A")
os.mkdir("b")