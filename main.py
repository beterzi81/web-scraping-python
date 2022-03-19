import getJSsites
import urllib.request
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
import re
import os.path
import ssl
import sqlite3

#########################Gerekli fonksiyonların tanımlanması##########################
def lineCounter(filename):#Parametreyle verilen dosyanın satır sayısını bulan fonksiyon 
    file = open(filename, "r")
    line_count = 0
    for line in file:
        if line != "\n":
            line_count += 1
    file.close()
    return line_count

def tokenize(d):#verilen parametredeki html tag'ini tokenize ediyor ve temel tag olarak döndürüyor
  yield f'<{d.name}>'
  for i in d.contents:
     if not isinstance(i, str):
       yield from tokenize(i)
     else:
       yield from i.split()
  yield f'</{d.name}>'


def filtertokenized(rawHTML):
    tokenizedHTML = list(tokenize(BeautifulSoup(rawHTML, 'html.parser')))#html belgesini tokenize ediyoruz
    filteredHTML = [item for item in tokenizedHTML if bool(BeautifulSoup(item, "html.parser").find())]#bu tokenize edilmiş elemanların içinden html tagi olmayanları ayıklıyoruz
    toList=''
    for i in filteredHTML:#veritabanımıza girerken text olarak gireceğiz bu yüzden list türündeki filteredHTML değişkenini bir str değişkenine dönüştürüyoruz
        toList+=i
    return toList


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
        if re.search(r'html$',j) and not (re.search(r'^index.html',j) and not re.search(r'[.][.]',j)):#html ile biten ve index.html ile başlamayan bütün iç linkleri bir listeye atadık.bunun sebebi de arada youtube linkleri de olabiliyor, ilerde alt sayfaları gezmeye çalışırken sorun olacaktır
            regulatedInsideLinks.append(j)
    for k in regulatedInsideLinks:
        encodedInsideLinks.append(urllib.parse.quote(k))
    return regulatedInsideLinks,encodedInsideLinks

def getHTML(link):
    try: 
        gcontext = ssl.SSLContext()
        req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        requestingHTML= urllib.request.urlopen(req,context=gcontext).read()
        decodedHTML=requestingHTML.decode("utf-8",errors='ignore')
        return decodedHTML
    except TimeoutError:
        print("Böyle bir bağlantı yok!")
        return 1
    except urllib.error.URLError:
        print("Böyle bir bağlantı yok!")
        return 1
    except ConnectionResetError:
        getHTML(link)
    

def start():
    try:
        os.mkdir("Siteler")  
        print("Gerekli klasörler oluşturuldu!")
    except FileExistsError:
        print("Gerekli klasörler zaten mevcut, işleme devam ediliyor.")
#########################Linkleri listeye aktarma##########################
#önce linkleri tek tip haline getirmemiz lazım
start()
database_connect = sqlite3.connect("siteler.db")#Database'imizi oluşturuyoruz
cursor=database_connect.cursor()#imlecimizi de atadık
temizlensin_mi=input("Daha önceden oluşturulmuş veritabanını temizlemek istiyor musunuz? (İstiyorsanız e/E girişini yapın, istemiyorsanız herhangi bir tuşa basın.)\n")
needSelenium='This site requires Javascript to work, please enable Javascript in your browser or use a browser with Javascript support'#bazı siteler freewebhosting dışında hosting kullandığı için javascript desteği gerekiyor, request ile js gerektiren siteler alınamadığı için bu siteleri selenium ile almamız gerekiyor
if temizlensin_mi=='E' or temizlensin_mi=='e':
    cursor.execute("DROP TABLE IF EXISTS siteler")#E girişi verilirse tablumuzu siliyoruz
cursor.execute("CREATE TABLE IF NOT EXISTS siteler(id INTEGER PRIMARY KEY AUTOINCREMENT,site_adi TEXT,dosya_adi TEXT,dosya_icerigi TEXT,UNIQUE(site_adi, dosya_adi))")#tablomuzu da oluşturduk
pageNotFound='PAGE NOT FOUND, FILE NOT FOUND or WEBSITE NOT FOUND!!!'#hedef site bulunamadığında default olarak gönderilen sitede ayrıştırıcı string olarak bu stringi buldum ve bunu değişkende tutup indirdiğimiz htmllerde bulunup bulunmadığını tespit edip sayfanın var olup olmadığını kontrol ediyoruz
adBanner='<div style="text-align:right;position:fixed;bottom:3px;right:3px;width:100%;z-index:999999;cursor:pointer;line-height:0;display:block;"><a target="_blank" href="https://www.freewebhostingarea.com" title="Free Web Hosting with PHP5 or PHP7"><img alt="Free Web Hosting" src="https://www.freewebhostingarea.com/images/poweredby.png" style="border-width: 0px;width: 180px; height: 45px; float: right;"></a></div>'#bu etiket freeWHA sitesinin reklan bannerının html kodu, bunu indirdiğimiz htmllerden kaldıracağız

linkler=[]
f=open('a.txt','r')#linklerin olduğu txt dosyasını açtık
linkSatirSayisi=lineCounter("a.txt")
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
    
    duzenliLinkler.append(i)
ctr=0
for i in duzenliLinkler:#düzenli linkleri her satıra bir link gelecek şekilde yerleştirdik
    i=i.replace("\n","")
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
for i in duzenliLinkler:#isimlendirme için her linkin netloc kısmını alıp klasör ismi olarak gösterdik
    parseLink=urlparse(i)
    klasorIsimleri.append(parseLink.netloc)
for i in klasorIsimleri:#klasör mevcut mu değil mi kontrol ettik
    try:
        os.mkdir("Siteler" + os.sep + i )
        print(i+" adlı klasör oluşturuldu! ")
    except FileExistsError:
        print(i+ " adlı klasör zaten mevcut!")


#########################Linklere gidip html içeriğini alma##########################
cwd=os.getcwd()#şuanki adresimizi alıyoruz ki elimizde mutlak bir adres oluşturabilelim
klasorIsimleriIterator=0#klasör isimlerini tek tek gezmek için bir iteratöre ihtiyacımız vardı
seleniumSites=[]
for i in duzenliLinkler:
    decodedHTML=getHTML(i)#listedeki linkin html kısmını getirdik
    if needSelenium in decodedHTML:
        seleniumSites.append(klasorIsimleri[klasorIsimleriIterator])
        getJSsites.getSite(klasorIsimleri[klasorIsimleriIterator])
        klasorIsimleriIterator+=1
        continue
    if adBanner in decodedHTML:
        decodedHTML=decodedHTML.replace(adBanner,' ')
    if not (pageNotFound in decodedHTML):#aldığımız html default html değilse işlemimizi gerçekleştiriyoruz
        indx="index.html"#ilk olarak index sayfasını indirdiğimiz için index.html olarak adlandırdık
        os.chdir(cwd+"/Siteler/"+klasorIsimleri[klasorIsimleriIterator])#temiz bir şekilde klasörümüzü oluşturacağımız mutlak yolu seçiyoruz
        structureOfHTML=filtertokenized(decodedHTML)
        cursor.execute("INSERT OR IGNORE INTO siteler (site_adi,dosya_adi,dosya_icerigi) VALUES(?,?,?)",(klasorIsimleri[klasorIsimleriIterator],indx,structureOfHTML))#index sayfamızı bu şekilde insert ettik
        saveFile = open(indx,"w",encoding='utf-8')#dosyamızı açtık
        saveFile.write(str(decodedHTML))#içine html içeriğini yazdık
        saveFile.close()#kapattık
    else:
        print("Böyle bir dosya yok!")
    #yukardaki cwd değişkeni tanımlamasından bu yorum satırına kadar olan kısım bütün linklerden gelen index.html içeriği ilgili klasöre index.html adı altında oluşturulup kaydediliyor.
    #döngümüze devam ederken alıp kaydettiğimiz index.html dosyasıyla işimiz daha bitmedi. burada bu içeriği fonksiyonumuza verip içinden isimlendirmede kullanacağımız regulatedInsideLinks ve path oluşturmada kullanacağımız encodedInsideLinks listesini elde ediyoruz
    regulatedInsideLinks,encodedInsideLinks=regulatedAndEncoded(decodedHTML)#index.html dosyasının içindeki diğer .html uzantılı adresleri alıyoruz ve gerekli listelere atamalarımızı yapıyoruz,regulated dediğimiz düz bir şekilde yazım, encoded ise aynı stringin utf-8 haline dönüştürülmüşü, encoded olmazsa html isteği yollayamayız
    
    getPath=urlparse(i)#düzenli hale getirdiğimiz linkimizi parçalıyoruz
    pth=getPath.path#path kısmını alıyoruz
    lgt=len(os.path.split(pth)[1])#path kısmının en son kısmını alıyor bu fonksiyon
    orgI=i[:len(i) - lgt]#organized i değişkenimiz düzenli linkimizin son path kısmı çıkarılmış hali oluyor
    isimlendirmeSayaci=0#içerideki html dosyalarına isimlendirme için bu değişkeni tutuyoruz
    for l in encodedInsideLinks:#sonra her iç düzenli link için elimizdeki düzenli linki manipüle edip o adrese gidip html dosyasını indirip kaydediyoruz
        os.chdir(cwd+"/Siteler/"+klasorIsimleri[klasorIsimleriIterator])#ne olur ne olmaz diye tekrar mutlak adresini bildiğimiz konuma gidiyoruz
        fileName=regulatedInsideLinks[isimlendirmeSayaci]#baştaki uzantıyı alıyoruz ki onun adıyla bir html oluşturacağız
        cwdInside=cwd+"/Siteler/"+klasorIsimleri[klasorIsimleriIterator]#bu değişkeni, iç linklerin içinde olup indexte olmayan sayfaları bulmak için kullanıyoruz, daha doğrusu o türdeki linklerdeki path farklı olduğu için klasörleme sistemine ihtiyacımız olacak,bunu da bu değişken sağlayacak
        lastPath=os.path.split(fileName)[1]#en sondaki .html kısımlı path parçasını alıyoruz
        if '/' in fileName:#eğer path'ta / varsa burada klasörleme var demektir o zaman giriyoruz buraya
            directoryNames=fileName.split('/')#path'ı / ile ayırıyoruz
            for i in directoryNames:
                if i != lastPath:#eğer path'taki son eleman olan .html'li kısımda değilsek
                    os.chdir(cwdInside)#cwdinside yoluna gidiyoruz
                    try:
                        os.mkdir(i)#mevcut pathı oluşturuyoruz
                    except FileExistsError:#eğer varsa böyle bir klasör
                        cwdInside=cwdInside+"/"+i#bir sonraki path kısmına geçişi hazırlıyoruz
                        continue
                    print(i + " oluşturuldu")
                    cwdInside=cwdInside+"/"+i
                else:
                    os.chdir(cwdInside)#eğer lastpath'taysak da tekrar bir geçiş yapıp en içe html dosyamızın adını veriyoruz
                    fileName=lastPath
        isimlendirmeSayaci+=1    
        #artırıyoruz ikinci link adına geçsin diye
        l=orgI+l#encode edilmiş html pathımızı organize edilmiş netloc ve scheme kısmıyla birleştirip bütün linki çıkarttık
        print(l+ " linki indirilmeye başlandı...")
        sideHTML=getHTML(l)#içerdeki encode ettiğimiz linkin html içeriğini getirdik
        if adBanner in sideHTML:
            sideHTML=sideHTML.replace(adBanner,' ')
        if not(pageNotFound in sideHTML):#aldığımız html default html değilse işlemimizi gerçekleştiriyoruz
            insideReg,insideEnc=regulatedAndEncoded(sideHTML)#iç linklerimizin htmline bakıp içindeki linkleri hem regular hem encoded hale getirip atama yapıyoruz
            sEnc=set(encodedInsideLinks)
            sReg=set(regulatedInsideLinks)
            if(all(x in encodedInsideLinks for x in insideEnc)):#burada iç htmldeki encoded linklerin listesinin indexteki linklerin listesinin alt kümesi olup olmadığını kontrol ediyoruz, eğer alt kümesi ise o zaman iç linkten gidebileceğiniz her yere index linkinden de gidebiliyoruz demektir
                pass
            else:#yok eğer iç linkte encoded haldeki linklerin listesinde farklı bir link varsa
                differentEncLinks=[x for x in insideEnc if x not in sEnc]#o zaman indexte olmayıp insidelinklerde olan farklı linkleri yeni bir listeye attık, hem encoded hem regulated için iki sefer şart koymadım çünkü ikisi de aynı string listesinin farklı şekilde yazılmış halleri
                differentRegLinks=[x for x in insideReg if x not in sReg]
                for t in differentEncLinks:#bütün farklı encoded linkleri içinde dolaştığımız listeye ekliyorum
                    encodedInsideLinks.append(t)
                for z in differentRegLinks:#bütün farklı regulated linkleri de içinden isimlendirme yaptığımız listeye ekliyorum
                    regulatedInsideLinks.append(z)
            
            silinecekler=[]#eğer ../../ şeklinde göreceli olarak atanmış bir değer bulursak bunu çıkarmalıyız
            for o in range(0,len(encodedInsideLinks)):
                if '../' in encodedInsideLinks[o]:
                    silinecekler.append(o)
            silinecekler.reverse()
            for u in silinecekler:
                encodedInsideLinks.pop(u)
                regulatedInsideLinks.pop(u)
            encodedInsideLinks=list(filter(None, encodedInsideLinks))#Boş elemanları çıkarıyoruz ki indirmeye çalışmasın null linki
            regulatedInsideLinks=list(filter(None, regulatedInsideLinks))
            structureOfSideHTML=filtertokenized(sideHTML)
            cursor.execute("INSERT OR IGNORE INTO siteler (site_adi,dosya_adi,dosya_icerigi) VALUES(?,?,?)",(klasorIsimleri[klasorIsimleriIterator],fileName,structureOfSideHTML))#index sayfamızı bu şekilde insert ettik
            saveFile = open(fileName,"w",encoding="utf-8")
            saveFile.write(str(sideHTML))
            saveFile.close()
            print("İndirme tamamlandı!")
        else:
            print("Böyle bir dosya yok!")
    klasorIsimleriIterator+=1#ve ana linkimizin indexindeki, indexinin gösterdiği sayfaları ve iç sayfaların iç sayfalarını da indirdikten sonra diğer linke geçiyoruz
database_connect.commit()
f=open('selenium_sites.txt','w')
for i in seleniumSites:
    f.write(i+'\n')
f.close()

