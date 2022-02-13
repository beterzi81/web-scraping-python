from base64 import encode
from distutils import errors
from lib2to3.pgen2 import parse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import subprocess
import os
from urllib.parse import urlparse
import re

a="https://codesque.github.io/BMGproje/"
b="https://docs.python.org/3/library/urllib.parse.html"
parse=urlparse(b)
print(parse.path)
