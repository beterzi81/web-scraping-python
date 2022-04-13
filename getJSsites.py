from selenium import webdriver
import time

# start web browser


def main():
    pass

if __name__ == "__main__":
    main()


def getSite(site):
    a=r"/opt/homebrew/bin/chromedriver"#chromedriver.exe dosyasının mutlak konumunu yazıp parametre olarak veriyoruz. bu sadece webdriver olarak chromedriver kullanıyorsak geçerli
    browser=webdriver.Chrome(executable_path=a)

    # get source code
    browser.get(site)
    html = browser.page_source
    time.sleep(2)
    

    # close web browser
    browser.close()
    return html

