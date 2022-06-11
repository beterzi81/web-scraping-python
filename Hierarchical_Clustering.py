import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import dendrogram
from matplotlib import pyplot as plt
from urllib.parse import urlparse
import re
import sqlite3
import numpy as np

def getBeforePath(parsedURL):
    return parsedURL.scheme+ '://'+ parsedURL.netloc

def lineCounter(filename):#Parametreyle verilen dosyanın satır sayısını bulan fonksiyon 
    file = open(filename, "r")
    line_count = 0
    for line in file:
        if line != "\n":
            line_count += 1
    file.close()
    return line_count

def regulatedSiteLinks():
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
        normalizedPath=''

        if not re.search(r'^/',str(parseLink.path)):#path kısmının başında / karakteri yoksa ekledik
            normalizedPath+='/'+str(parseLink.path)
            i= getBeforePath(parseLink)+ normalizedPath
            i=i.replace("\n","")
        
        duzenliLinkler.append(i)
    return duzenliLinkler
#Elimizdeki hazır txt içinden verilerimizi okup bir matrise atıyoruz
with open("Data Compare/Levenshtein/levenshtein_similarity_result.txt") as dataSet:
    data=np.array([line.split(";")  for line in dataSet])
floatData=[]
for i in range(0,len(data)):
    floatData.append(list(map(float, data[i])))


names=[]
#İsimlendirme için sitelerimizi de çektik
databaseConnect = sqlite3.connect('siteler.db')#veritabanına bağlandık
databaseConnect.row_factory = lambda cursor, row: row[0]
cursor = databaseConnect.cursor()#cursorımızı oluşturuk
dbItems = cursor.execute('SELECT id FROM siteler').fetchall()#bütün id değerlerini aldık,
dbItems.sort()#id değerleri sırasız geliyordu sıraladık
for i in dbItems:
    i=str(i)
    names.append(cursor.execute('SELECT site_adi FROM siteler WHERE id='+i).fetchall() + cursor.execute('SELECT dosya_adi FROM siteler WHERE id='+i).fetchall())


for i in range(0,len(names)):
    names[i]=names[i][0] +'->' +names[i][1]
    

condensedData = squareform(floatData)
#Dendogramımızı çiziyoruz
Z = sch.linkage(condensedData, 'single')
fig = plt.figure()
dn = dendrogram(Z,labels=names)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
