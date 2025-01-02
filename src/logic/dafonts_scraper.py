from bs4 import BeautifulSoup, ResultSet
from bs4.element import Tag
import bs4
import requests
import os
import re
import json
import datetime

class DaFonts_Scraper:

    debug=False

    ## NOTE: NONE OF THIS WORKS RIGHT NOW BECAUSE I REWROTE THE CODE WITH BeautifulSoup 
    # IN MIND BUT IT DOESN'T WORK WITH JAVASCRIPT. SO WE WILL NEED REWRITE THE CODE AND FIND A EASY TO USE 
    # SCRAPING ENGINE.... PHANTOMJS WITH GHOST DRIVER MAYBE
    # https://stackoverflow.com/questions/13287490/is-there-a-way-to-use-phantomjs-in-python
    # https://github.com/detro/ghostdriver


    def request(url):
        respose=requests.post(url)
        return BeautifulSoup(respose.text, 'html5lib')

    def get_themes_info():

        themes = {}

        driver = DaFonts_Scraper.request("https://www.dafont.com/")
        print(driver)
        table_div: Tag = driver.find(id='menuthemes')
        print(table_div)
        theme_links: ResultSet[Tag] = table_div.findAll('a')

        # alpha_ = re.compile('\w')

        category = None

        for theme_link in theme_links:
            # print(f'cat: {theme_link.text} link: {theme_link.get("href")}')
            key = theme_link.text.strip().replace(' ', '_')
            key = re.sub('\W', '', key)
            # print(f'key: {key}')

            if re.search('bitmap.php', theme_link.get("href")):
                print(f'WARNING: skipping bitmap fonts.')
            elif re.search('mtheme', theme_link.get("href")):
                category = key
                themes[category] = {}
            elif category is not None:
                themes[category][key] = theme_link.get("href")
            else:
                print(f'WARNING: skipping {key} because no {category} is set.')

        return themes

    def get_fonts(url, category, theme, free_only: bool = False):
        fonts = []
        url += '&sort=date&fpp=200'

        if free_only:
            url += '&l[]=10&l[]=1'

        driver = DaFonts_Scraper.request(url)
        # print(url)

        # max_page_count
        noindex_div: Tag = driver.find(class_="noindex")[0]
        page_links: ResultSet[Tag] = noindex_div.findAll('a')
        max_page_count = 1
        for l in page_links:
            try:
                num = int(l.text)
                max_page_count = max(max_page_count, num)
            except ValueError:
                pass

        # print(max_page_count)

        for i in range(max_page_count):
            page_num = i + 1
            page_url = url + '&page=' + str(page_num)
            # print(page_url)

            fonts.extend(DaFonts_Scraper.collect_font_info(DaFonts_Scraper.request(page_url), category, theme))

            if DaFonts_Scraper.debug:
                break
        
        return fonts

        # max_page_count

    def collect_font_info(driver: BeautifulSoup, category, theme):
        fonts = []
        
        info_elements = driver.findAll(class_='lv1left')
        download_elements = driver.findAll(class_='dl')

        # print(len(info_elements), len(download_elements))

        assert(len(info_elements) == len(download_elements))

        for i in range(len(info_elements)):
            info_e = info_elements[i]
            download_e = download_elements[i]

            info_links = info_e.findAll('a')
            if len(info_links) < 2:
                continue
            font_name = info_links[0].text
            font_link = info_links[0].get_attribute('href').split('?')[0]
            font_creator = info_links[1].text
            font_download = download_e.get_attribute('href')

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
        themes_cache: str = "src/resources/cache/dafont-themes.json"
        use_cache = True
        free_only = False

        if use_cache and os.path.exists(themes_cache):
            f = open(themes_cache, 'r')
            themes = json.load(f)
        else:
            themes = DaFonts_Scraper.get_themes_info()
            if use_cache:
                f = open(themes_cache, 'w') 
                json.dump(themes, f, indent=4) 
                f.close()

        # print(themes)

        all_fonts = []

        for category in themes.keys():
            for theme in themes[category].keys():
                fonts = DaFonts_Scraper.get_fonts(themes[category][theme], category, theme, free_only)
                all_fonts.extend(fonts)

            if DaFonts_Scraper.debug:
                break
            if DaFonts_Scraper.debug:
                break

        # print(all_fonts)

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

        return font_list
