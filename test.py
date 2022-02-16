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
a=['aciktekerlek.html', 'gt.html', 'rally.html', 'moto.html', 'iletisim.html', 'otherpages/favpages/aciktekerlek/f1.html', 'otherpages/favpages/gt/lemans.html', 

'otherpages/favpages/rally/wrc.html', 'otherpages/favpages/moto/motogp.html', 'otherpages/favpages/moto/worldsuperbike.html', 'otherpages/favpages/gt/nascar.html', 

'otherpages/favpages/aciktekerlek/indycar.html', 'otherpages/favpages/gt/porschesupercup.html']


b=['backpages/aciktekerlek/f1.html', 'backpages/aciktekerlek/f2.html', 'backpages/aciktekerlek/fe.html', 

'backpages/aciktekerlek/indycar.html']
for i in a:
        
    s=set(a)
    if(all(x in b for x in a)):
        print("alt kümesi")
    else:
        print("değil")
        c=[x for x in b if x not in s]
        for j in c:
            a.append(j)

print(a)
if(all(x in a for x in b)):
    print("alt kümesi")