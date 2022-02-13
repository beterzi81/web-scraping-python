from base64 import encode
from distutils import errors
from lib2to3.pgen2 import parse
import urllib.request
from urllib.request import Request, urlopen
import subprocess
import os
from urllib.parse import urlparse
import re



os.mkdir("Siteler/sdfg")



'''
cmd = "cat links.txt | cut -d '.' -f 1 | cut -d '/' -f 3"#links.txt dosyasındaki linklerin isimlendirmeye uygun kısımlarını kestik
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
temp = process.communicate()[0]
isim=temp.decode()#bytes türünde dönen isimlendirmede kullanılacak kısımlar stringe dönüştürüldü
isimArray=isim.split('\n')#string türünden string array türüne dönüştürüldü
for i in isimArray:#her isim için aynı adda bir klasör oluşturuldu,1 kez yapılmalı
    command = "cd /Users/beterzi/Desktop/Web-Scraping/Siteler; mkdir " + i
    subprocess.run(command, capture_output=True, shell=True)
    '''