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
a="https://codesque.github.io"
b="https://docs.python.org/3/library/urllib.parse.html"

url = 'http://www.example.com/hithere/something/else'

PurePosixPath(unquote(urlparse(url).path)).parts[1]