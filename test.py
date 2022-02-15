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


'''
getPath=urlparse(e)
pth=parse.path
normalizedPath=''
print(os.path.split(pth)[1])
'''
a="http://abdullahbilgi.orgfree.com/okculukekipmanlari.html"

req = urllib.request.Request(a, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
requestingHTML= urllib.request.urlopen(req).read()
decodedHTML=requestingHTML.decode("utf-8",errors='ignore')
print(decodedHTML)
