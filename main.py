from ast import expr_context
import urllib.request
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
import re
import os.path
import ssl

#########################Gerekli fonksiyonların tanımlanması##########################
def lineCounter(filename):#Parametreyle verilen dosyanın satır sayısını bulan fonksiyon 
    file = open(filename, "r")
    line_count = 0
    for line in file:
        if line != "\n":
            line_count += 1
    file.close()
    return line_count

def getBeforePath(parsedURL):
    return parsedURL.scheme+ '://'+ parsedURL.netloc

def regulatedAndEncoded(HTMLSource):
    soup = BeautifulSoup(HTMLSource, 'html.parser')
    insideLinks=[]
    for link in soup.find_all('a'):
        insideLinks.append(link.get('href'))
    
    insideLinks=list(dict.fromkeys(insideLinks))#tekrarlayan değerleri kaldırdık
    insideLinks=list(filter(None, insideLinks))#null yani boş string değerlerini de kaldırdık
    regulatedInsideLinks=[]#her döngüde üstüne eklenerek gitmesin diye burada listemizi boşaltıyoruz
    encodedInsideLinks=[]
    
    for j in insideLinks:
        if re.search(r'html$',j) and not (re.search(r'^index.html',j)):#html ile biten ve index.html ile başlamayan bütün iç linkleri bir listeye atadık.bunun sebebi de arada youtube linkleri de olabiliyor, ilerde alt sayfaları gezmeye çalışırken sorun olacaktır
            regulatedInsideLinks.append(j)
    for k in regulatedInsideLinks:
        encodedInsideLinks.append(urllib.parse.quote(k))
    return regulatedInsideLinks,encodedInsideLinks

def getHTML(link):
    try: 
        gcontext = ssl.SSLContext()
        req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        requestingHTML= urllib.request.urlopen(req,context=gcontext).read()
    except TimeoutError:
        print("Böyle bir bağlantı yok!")
        return "Böyle bir şey yok!"
    except urllib.error.URLError:
        print("Böyle bir bağlantı yok!")
        return "Böyle bir şey yok!"
    except ConnectionResetError:
        getHTML(link)
    decodedHTML=requestingHTML.decode("utf-8",errors='ignore')
    return decodedHTML

def start():
    try:
        os.mkdir("Siteler")  
        print("Gerekli klasörler oluşturuldu!")
    except FileExistsError:
        print("Gerekli klasörler zaten mevcut, işleme devam ediliyor.")
#########################Linkleri listeye aktarma##########################
#önce linkleri tek tip haline getirmemiz lazım
start()
linkler=[]
f=open('tst.txt','r')#linklerin olduğu txt dosyasını açtık
linkSatirSayisi=lineCounter("tst.txt")
for i in range(0,linkSatirSayisi):
    linkler.append(f.readline())#Her linki bir indexe attık
f.close()
#Artık bütün linklerimizi barındıran bir listemiz var
duzenliLinkler=[]#linklerimizi düzenleyip bu listeye koyacağız
for i in linkler:
    parseLink=urlparse(i)#her linki parçaladık
    normalizedPath=''

    if not re.search(r'^/',str(parseLink.path)):
        normalizedPath+='/'+str(parseLink.path)
        i= getBeforePath(parseLink)+ normalizedPath
    
    duzenliLinkler.append(i)
ctr=0
for i in duzenliLinkler:
    i=i.rstrip('\n')
    duzenliLinkler[ctr]=i
    ctr+=1
'''
#linkleri txt ile görmek istersek
f=open("duzenli.txt",'w')
for i in duzenliLinkler:
    f.write(i+'\n')
f.close()
'''
#listemizdeki bütün linkleri düzenli hale getirdik.

#########################Klasörleri oluşturma##########################
'''
Yorum satırıyla yazılan kısım güncellemeden önceki bash komutu kullanılarak işi yapan kısımdır, artık aynı işi bir python kütüphanesiyle yazarak daha gelişmiş bir uyumluluk sağlıyoruz

#cat links.txt | cut -d "." -f 1 | cut -d "/" -f 3
cmd = "cat links.txt | cut -d '.' -f 1 | cut -d '/' -f 3"#links.txt dosyasındaki linklerin isimlendirmeye uygun kısımlarını kestik
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
temp = process.communicate()[0]
isim=temp.decode()#bytes türünde dönen isimlendirmede kullanılacak kısımlar stringe dönüştürüldü
isimArray=isim.split('\n')#string türünden string array türüne dönüştürüldü
for i in isimArray:#her isim için aynı adda bir klasör oluşturuldu,1 kez yapılmalı
    command = "cd /Users/beterzi/Desktop/Web-Scraping/Siteler; mkdir " + i
    subprocess.run(command, capture_output=True, shell=True)
'''
klasorIsimleri=[]
for i in duzenliLinkler:
    parseLink=urlparse(i)
    klasorIsimleri.append(parseLink.netloc)
for i in klasorIsimleri:
    try:
        os.mkdir("Siteler/"+i)  
        print(i+" adlı klasör oluşturuldu! ")
    except FileExistsError:
        print(i+ " adlı klasör zaten mevcut!")


#########################Linklere gidip html içeriğini alma##########################
cwd=os.getcwd()
print(cwd)
klasorIsimleriIterator=0
for i in duzenliLinkler:
    decodedHTML=getHTML(i)
    
    indx="index.html"
    os.chdir(cwd+"/Siteler/"+klasorIsimleri[klasorIsimleriIterator])
    saveFile = open(indx,"w")
    saveFile.write(str(decodedHTML))
    saveFile.close()
    #yukardaki cwd değişkeni tanımlamasından bu yorum satırına kadar olan kısım artık bir simülasyon değil gerçek bir çalışma halinde. bütün linklerden gelen index.html içeriği ilgili klasöre index.html adı altında oluşturulup kaydediliyor.


    #döngümüze devam ederken alıp kaydettiğimiz index.html dosyasıyla işimiz daha bitmedi. burada bu içeriği fonksiyonumuza verip içinden isimlendirmede kullanacağımız regulatedInsideLinks ve path oluşturmada kullanacağımız encodedInsideLinks listesini elde ediyoruz
    regulatedInsideLinks,encodedInsideLinks=regulatedAndEncoded(decodedHTML)
    
    getPath=urlparse(i)#düzenli hale getirdiğimiz linkimizi parçalıyoruz
    pth=getPath.path#path kısmını alıyoruz
    lgt=len(os.path.split(pth)[1])#path kısmının en son kısmını alıyor bu fonksiyon
    orgI=i[:len(i) - lgt]#organized i değişkenimiz düzenli linkimizin son path kısmı çıkarılmış hali oluyor
    print(orgI)
    isimlendirmeSayaci=0
    for l in encodedInsideLinks:#sonra her iç düzenli link için elimizdeki düzenli linki manipüle edip o adrese gidip html dosyasını indirip kaydediyoruz
        print(encodedInsideLinks)
        os.chdir(cwd+"/Siteler/"+klasorIsimleri[klasorIsimleriIterator])
        fileName=regulatedInsideLinks[isimlendirmeSayaci]#baştaki uzantıyı alıyoruz ki onun adıyla bir html oluşturacağız
        cwdInside=cwd+"/Siteler/"+klasorIsimleri[klasorIsimleriIterator]
        lastPath=os.path.split(fileName)[1]
        if '/' in fileName:
            directoryNames=fileName.split('/')
            print(directoryNames)
            for i in directoryNames:
                if i != lastPath:
                    os.chdir(cwdInside)
                    print(cwdInside)
                    try:
                        os.mkdir(i)
                    except FileExistsError:
                        cwdInside=cwdInside+"/"+i
                        continue
                    print(i + " oluşturuldu")
                    cwdInside=cwdInside+"/"+i
                else:
                    os.chdir(cwdInside)
                    fileName=lastPath
            
        isimlendirmeSayaci+=1#artırıyoruz ikinci link adına geçsin diye
        l=orgI+l#encode edilmiş html pathımızı organize edilmiş netloc ve scheme kısmıyla birleştirip bütün linki çıkarttık
        print(l+ " linki indirilmeye başlandı...")
        sideHTML=getHTML(l)
        insideReg,insideEnc=regulatedAndEncoded(sideHTML)
        print(insideEnc)
        saveFile = open(fileName,"w")
        saveFile.write(str(sideHTML))
        saveFile.close()
        print("İndirme tamamlandı!")
    klasorIsimleriIterator+=1
    #Şimdi her iç linke gidip oradaki htmlleri de indirip içinde index'ten ve insideLinksArray'deki linklerden başka link var mı diye bakacağız

        