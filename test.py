from base64 import encode
from distutils import errors
from lib2to3.pgen2 import parse
import urllib.request
from urllib.request import Request, urlopen
import subprocess
import os
from urllib.parse import urlparse
import re

def lineCounter(filename):
    file = open(filename, "r")
    line_count = 0
    for line in file:
        if line != "\n":
            line_count += 1
    file.close()
    return line_count
#########################Linkleri listeye aktarma##########################
#önce linkleri tek tip haline getirmemiz laızm
linkler=[]
f=open('links.txt','r')#linklerin olduğu txt dosyasını açtık
linkSatirSayisi=lineCounter("links.txt")
for i in range(0,linkSatirSayisi):
    linkler.append(f.readline())#Her linki bir indexe attık
f.close()
#Artık bütün linklerimizi barındıran bir listemiz var
duzenliLinkler=[]#linklerimizi düzenleyip bu listeye koyacağız
for i in linkler:
    parseLink=urlparse(i)#her linki parçaladık
    if(re.search(r'filedn.eu',i) or re.search(r'codesque.github.io',i) or re.search(r'orgfree.com',i)) :#burada bir istisna var, filedn.eu şeklindeki bir link var ve tam link girilmedikçe doğru adrese gitmiyor onun için o istisnayı düzeltiyoruz.ikinci istisna da github.io linklerinde, onu da düzelttik
        duzenliLinkler.append(i)
    else:
        di=parseLink.scheme+"://"+parseLink.netloc  #scheme ve netloc kısmını :// stringi ile birleştirdiğimizde elimizde tertemiz bir index linki oluyor
        duzenliLinkler.append(di)

f=open('duzenli.txt','w')
for i in duzenliLinkler:
    f.write(i+"\n")
f.close()