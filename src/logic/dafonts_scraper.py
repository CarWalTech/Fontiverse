from enum import Enum
from bs4 import BeautifulSoup, ResultSet
from bs4.element import Tag
import bs4
import requests
import os
import re
import json
import datetime

from selenium import webdriver
from selenium.webdriver.remote.webdriver import *
from selenium.webdriver.common.by import By

from ..paths import ROOT_DIR

class LogLevel(Enum):
    Lowest=0
    Locations=1
    Steps=2
    StepDetail=3
    SuperDetail=4
    PreStepDetail=5
    Warnings=6


class DaFonts_Scraper:


    def isDebug():
        return False
    
    def isLogging(logLevel: int = 0):
        match logLevel:
            case LogLevel.Lowest: 
                return True
            case LogLevel.Locations: 
                return False
            case LogLevel.Steps: 
                return True
            case LogLevel.StepDetail: 
                return False
            case LogLevel.PreStepDetail: 
                return False
            case LogLevel.SuperDetail: 
                return False
            case LogLevel.Warnings: 
                return True
            case _: 
                return True

    def get_themes_info(driver: WebDriver):

        themes = {}

        table_div: WebElement = driver.find_element(By.CSS_SELECTOR, '#menuthemes')
        theme_links: list[WebElement] = table_div.find_elements(by=By.CSS_SELECTOR, value='a')

        # alpha_ = re.compile('\w')

        category = None

        for theme_link in theme_links:
            if DaFonts_Scraper.isLogging(LogLevel.StepDetail): print(f'cat: {theme_link.get_attribute("innerHTML")} link: {theme_link.get_attribute("href")}')
            key = theme_link.get_attribute("innerHTML").strip().replace(' ', '_')
            key = re.sub('\W', '', key)
            if DaFonts_Scraper.isLogging(LogLevel.StepDetail): print(f'key: {key}')

            if re.search('bitmap.php', theme_link.get_attribute("href")):
                if DaFonts_Scraper.isLogging(LogLevel.Warnings): print(f'WARNING: skipping bitmap fonts.')
            elif re.search('mtheme', theme_link.get_attribute("href")):
                category = key
                themes[category] = {}
            elif category is not None:
                themes[category][key] = theme_link.get_attribute("href")
            else:
                if DaFonts_Scraper.isLogging(LogLevel.Warnings): print(f'WARNING: skipping {key} because no {category} is set.')

        return themes

    def get_fonts(driver: WebDriver, url, category, theme, free_only: bool = False):
        fonts = []
        fonts_per_page = 200
        url += f'&sort=date&fpp={fonts_per_page}'

        if free_only:
            url += '&l[]=10&l[]=1'

        driver.get(url)
        if DaFonts_Scraper.isLogging(LogLevel.Locations): print(url)

        # max_page_count
        noindex_div: WebElement = driver.find_elements(by=By.CSS_SELECTOR, value=".noindex")[0]
        page_links: list[WebElement] = noindex_div.find_elements(by=By.CSS_SELECTOR, value='a')
        max_page_count = 1
        for l in page_links:
            try:
                num = int(l.text)
                max_page_count = max(max_page_count, num)
            except ValueError:
                pass

        if DaFonts_Scraper.isLogging(LogLevel.PreStepDetail): print(max_page_count)

        for i in range(max_page_count):
            page_num = i + 1
            page_url = url + '&page=' + str(page_num)

            if DaFonts_Scraper.isLogging(LogLevel.Steps): 
                print(f"Page: {page_num}/{max_page_count}")
                print(f"Link: {page_url}")

            found_fonts = DaFonts_Scraper.collect_font_info(driver, page_url, category, theme)
            fonts.extend(found_fonts)

            if DaFonts_Scraper.isDebug():
                break
        
        return fonts

        # max_page_count

    def collect_font_info(driver: WebDriver, page_url: str, category, theme):
        fonts = []

        driver.get(page_url)
        
        info_elements = driver.find_elements(by=By.CSS_SELECTOR, value='.lv1left')
        download_elements = driver.find_elements(by=By.CSS_SELECTOR, value='.dl')

        if DaFonts_Scraper.isLogging(LogLevel.PreStepDetail): print(f"Info Elements: {len(info_elements)}, Download Elements: {len(download_elements)}")

        assert(len(info_elements) == len(download_elements))

        for i in range(len(info_elements)):
            info_e = info_elements[i]
            download_e = download_elements[i]

            info_links = info_e.find_elements(by=By.CSS_SELECTOR, value='a')
            if len(info_links) < 2:
                continue
            font_name = info_links[0].text
            font_link = info_links[0].get_attribute('href').split('?')[0]
            font_creator = info_links[1].text
            font_download = download_e.get_attribute('href')
            if DaFonts_Scraper.isLogging(LogLevel.StepDetail): print(f"Font #{i+1}: {font_name}")

            font = {
                'name': font_name,
                'dafont_link': font_link,
                'creator': font_creator,
                'download': font_download,
                'category': category,
                'theme': theme,
            }

            fonts.append(font)

            # if debug:
            #   break
        
        return fonts

    def scrape():   
        themes_cache: str = "{0}/resources/cache/dafont-themes.json".format(ROOT_DIR)
        out_path: str = "{0}/resources/cache/dafont-list.json".format(ROOT_DIR)

        use_themes_cache = True
        update_themes_cache = False

        free_only = False
        


        try:
            options = webdriver.FirefoxOptions()
            options.page_load_strategy = 'eager'
            options.add_argument("--headless")
            options.set_preference('permissions.default.image', 2)
            options.set_preference("permissions.default.stylesheet", 2)
            options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

            driver = webdriver.Firefox(options=options)
            driver.get("https://www.dafont.com/")
            assert "DaFont" in driver.title

            if use_themes_cache and os.path.exists(themes_cache):
                f = open(themes_cache, 'r')
                themes = json.load(f)
            else:
                if not os.path.exists(os.path.dirname(themes_cache)):
                    os.makedirs(os.path.dirname(themes_cache))
                    
                themes = DaFonts_Scraper.get_themes_info(driver)
                if update_themes_cache:
                    f = open(themes_cache, 'w') 
                    json.dump(themes, f, indent=4) 
                    f.close()

            if DaFonts_Scraper.isLogging(LogLevel.SuperDetail): print(themes)

            all_fonts = []

            for category in themes.keys():
                for theme in themes[category].keys():
                    fonts = DaFonts_Scraper.get_fonts(driver, themes[category][theme], category, theme, free_only)
                    all_fonts.extend(fonts)

                    if DaFonts_Scraper.isDebug():
                        break
                if DaFonts_Scraper.isDebug():
                    break

            if DaFonts_Scraper.isLogging(LogLevel.SuperDetail): print(all_fonts)

            d_name = 'dafonts-'
            if free_only:
                d_name += 'free'
            else:
                d_name += 'nonfree'

            font_list = {
                'dataset_name': d_name,
                'date': str(datetime.datetime.now()),
                'font_info': all_fonts
            }

            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            f = open(out_path, 'w') 
            json.dump(font_list, f, indent=4) 
            f.close()
        except Exception as e:
            print(e)
        finally:
            driver.close()

        return font_list
