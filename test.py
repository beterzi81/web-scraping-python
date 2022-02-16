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
reg=['aciktekerlek.html', 'gt\n.html', 'rally.html', 'moto.html', 'iletisim.html', 'otherpages/favpages/aciktekerlek/f1.html', 'otherpages/favpages/gt/lemans.html', 'otherpages/favpages/rally/wrc.html', 'otherpages/favpages/moto/motogp.html', 'otherpages/favpages/moto/worldsuperbike.html', 'otherpages/favpages/gt/nascar.html', 'otherpages/favpages/aciktekerlek/indycar.html', 'otherpages/favpages/gt/porschesupercup.html', 'backpages/aciktekerlek/f1.html', 'backpages/aciktekerlek/f2.html', 'backpages/aciktekerlek/fe.html', 'backpages/aciktekerlek/indycar.html', 'backpages/gt/lemans.html', 'backpages/gt/nascar.html', 'backpages/gt/porschesupercup.html', 'backpages/rally/wrc.html', 'backpages/rally/dakar.html', 'backpages/moto/motogp.html', 'backpages/moto/worldsuperbike.html', '../../../index.html', '../../../gt.html', '../../../rally.html', '../../../moto.html', '../../../iletisim.html']

for i in reg:
    if '../' or '\n' in i:
        print(i)

