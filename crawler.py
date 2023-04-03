import requests
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from bs4 import BeautifulSoup
import json
import io
import time
import os
from pathlib import Path
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


class Crawler:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/75.0.3770.80 Safari/537.36'}

        self.opts = FirefoxOptions()
        self.opts.add_argument("--headless")
        self.driver = webdriver.Firefox(service=FirefoxService(
            GeckoDriverManager().install()), options=self.opts)

    def __call__(self, url,output):
        self.output=output
        self.url = url
        self.urls = self.url.split("/")
        self.name = self.urls[-1].split(".")[0]
        self.gender = self.urls[-2]
        Path(os.path.join(self.output,self.name)).mkdir(parents=True, exist_ok=True)
        self.driver.get(self.url)
        lastHeight = self.driver.execute_script(
            "return document.body.scrollHeight")
        pause = 0.5
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause)
            newHeight = self.driver.execute_script(
                "return document.body.scrollHeight")
            if newHeight == lastHeight:
                break
            lastHeight = newHeight

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        self.images = soup.find_all("img")
        self.price = soup.find("p", {"data-component": "PriceLarge"})
        self.brand = soup.find(
            "a", {"class": "ltr-jtdb6u-Body-Heading-HeadingBold e1h8dali1"})
        self.desc = soup.find(
            "p", {"data-testid": "product-short-description"})
        self.highlights = soup.find_all(
            "li", {"class": "ltr-4y8w0i-Body e1s5vycj0"})
        self.Composition = soup.find_all(
            "span", {"class": "ltr-4y8w0i-Body e1s5vycj0"})
        self.hs = [h.text for h in self.highlights]
        self.Composition = [c.text for c in self.Composition]
        self.write_results()

    def write_results(self):
        for i, img in enumerate(self.images):
            try:
                img_url = img['src']
                res = requests.get(img_url)
                f_name=img_url.split("/")[-1]
                f = open(os.path.join(self.output,self.name,f_name), "wb")
                f.write(res.content)
            except Exception as e:
                print(e)

        results = {
            "full-name": self.name,
            "brand": self.brand.text,
            "gender": self.gender,
            "price": self.price.text[1:],
            "short-description": self.desc.text,
            "Highlights": self.hs,
            "Composition": self.Composition[:2],
            "farfetch-id": self.Composition[2],
            "brand-style-id": self.Composition[3]
        }

        obj = json.dumps(results, indent=4)
        with io.open(os.path.join(self.output,self.name, 'feature.json'), 'w') as db_file:
            db_file.write(obj)
