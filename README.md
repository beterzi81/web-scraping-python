# Static Website Scraper

Static Website Scraper, Python dili ile yazılmış, işletim sisteminden bağımsız çalışan, verilen statik sitelerin içeriğini bilgisayara indiren bir Web Scraping programıdır.


# Kullanılan teknolojiler

Bu proje Python dili kullanılarak hazırlanmış ve beautifulsoup kütüphanesiyle desteklenmiş bir programdır.

## Nasıl Kullanılır?

İlk önce aşağıdaki kodları terminalden çalıştırarak projemizin dosyalarını istediğimiz bir klasöre kuruyoruz:

    git clone https://github.com/beterzi81/web-scraping-python.git 


Hemen ardından da tekrar terminal üzerinden gerekli kütüphaneleri indirmek ve kurmak için aşağıdaki komutu giriyoruz:

    pip install -r requirements.txt

Artık projemiz bilgisayarımızda kullanıma hazır bir biçimde duruyor.

## Kullanım Kılavuzu
İlk önce dosyalarımızı tanıyalım:

 - main.py: Bu bizim ana python dosyamızdır, çalışması gereken bütün kodlar bu dosyanın içinde yazılıdır.
 - links.txt: Bu dosya, indirilmesini istediğimiz linkleri barındıran bir metin dosyasıdır.
 - requirements.txt: Bu metin dosyası ise hangi kütüphanelerin kurulması gerektiğini içeren dosyamızdır.
 - Siteler(Klasör): Bu klasörde önceden indirilmiş sitelerin klasörlenmiş şekilde HTML dosyaları vardır. 

Kendi linklerinizi programa indirtmek istiyorsanız links.txt dosyasını el ile manipüle edebilir, örnek sitelerin indirilmiş dosyalarından kurtulmak istiyorsanız da aynı şekilde el ile Siteler klasörünü silebilirsiniz.

İstediğiniz değişiklikleri yaptıktan sonra yapmanız gereken tek şey main.py dosyasını çalıştırmaktır.
