from base64 import encode
from distutils import errors
import urllib.request
from urllib.request import Request, urlopen
import subprocess
import os
from urllib.parse import urlparse
import re
req = urllib.request.Request('http://harrypotterbinalar.orgfree.com', headers={'User-Agent': 'Mozilla/5.0'})
requestingHTML= urllib.request.urlopen(req).read()
decodedHTML=requestingHTML.decode("utf-8",errors='ignore')#bu şekilde yazınca 8. linkte UnicodeDecodeError: 'utf-8' codec can't decode byte 0xdd in position 114: invalid continuation byte hatası alıyorum(bu hatayı, decode fonksiyonunun içinde errors='ignore' parametresi vererek çözdüm)     
# ayrıca bu kodla çalıştırınca da 32. sitede urllib.error.HTTPError: HTTP Error 403: Forbidden hatası alıyorum
#45-50 arası siteleri indirebiliyor muyum denemek için yazıldı simüle satırları onlar. normalde hepsini kendi klasörüne indireceğim

temp="ahmet.html"
saveFile = open(temp,"w")
saveFile.write(str(decodedHTML))
saveFile.write("*"*125)
saveFile.close()