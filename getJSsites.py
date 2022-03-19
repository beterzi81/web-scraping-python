from selenium import webdriver
import time
from webdriver_manager.chrome import OperaDriverManager

def main():
    pass

if __name__ == "__main__":
    main()


def getSite(site):
    browser=webdriver.Opera(executable_path=OperaDriverManager().install())#browserımızı çalıştırıyoruz
    browser.get("https://"+site)
    html = browser.page_source
    time.sleep(2)
    browser.close()
    print(html)
    print("-"*100)


