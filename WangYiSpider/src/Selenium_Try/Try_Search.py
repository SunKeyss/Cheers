# utf-8
from urllib.parse import urlencode

import requests
import time
import re
import json
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By


# 搜索函数
# Button Function 响应搜索请求
def CallOn_Click_Search(name, listbox_singer):
    try:
        # browser = webdriver.Chrome('E:\浏览器\Google\Chrome\Application\chromedriver.exe')
        # browser.minimize_window()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('log-level=3')
        browser = webdriver.Chrome(chrome_options=chrome_options,
                                   executable_path='E:\浏览器\Google\Chrome\Application\chromedriver.exe')

        # 以原始字符串的方式指定路径?????selenium不支持pj了???.......
        # browser = webdriver.PhantomJS(executable_path = r'G:\Python\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        try:
            params = {
                's': name.get(),
                'type': '1',
            }
            url = 'https://music.163.com/#/search/m/?' + urlencode(params)
            browser.get(url)
            time.sleep(2)
            # wait = WebDriverWait(browser, 60)
            # wait.until(EC.presence_of_element_located((By.__class__, 'td w0')))#等到id为m-search的元素加载完毕
            print(browser.current_url)
            print(browser.get_cookies())
            # print(browser.page_source)

            browser.switch_to.frame('contentFrame')
            try:
                # a[href^=\/song]
                # song_URL = find_infor.find_element(By.CLASS_NAME, 'w0').find_element(By.TAG_NAME, 'a')
                # print(song_URL.get_attribute('href'))
                URL_list = []  # 歌曲外链接
                Singer_list = []  # 歌手
                Song_name_list = []  # 歌名

                a = []
                # find_elements返回的是一个数组，只有数组才能遍历
                for each in browser.find_element(By.CLASS_NAME, 'srchsongst').find_elements(By.CLASS_NAME, 'h-flag'):
                    aa = []  # 声明数组
                    for each1 in each.find_element(By.CLASS_NAME, 'w0').find_elements_by_css_selector(
                            'a[href^=\/song]'):
                        surl = each1.get_attribute('href')  # 假链接
                        sid = surl.split('?')[-1]  # 获取id=xxx
                        download_url = 'http://music.163.com/song/media/outer/url?' + sid + '.mp3'
                        URL_list.append(download_url)
                        for each2 in each.find_elements(By.CLASS_NAME, 'w1'):
                            info_show = each1.text + ' - ' + each2.text + ' - ' + download_url  # 歌名+作者+链接
                            listbox_singer.insert(tk.END, info_show)  # 构造信息展示列表
                            print(info_show)


            except Exception as e:
                print(e)
                print('wrong for webmusic search %%%%%%%%%%%%%%%')

            #QQMusic 部分
            try:
                params = {
                    'searchid': '1',
                    'remoteplace': 'txt.yqq.top',
                    't': 'song',
                    'w': name.get()
                }

                url = 'https://y.qq.com/portal/search.html#page=1' + urlencode(params)
                # print('url=',url)  # ===========================================
                browser.get(url)
                time.sleep(2)

                print(browser.current_url)
                print(browser.get_cookies())
                # print(browser.page_source)
                # 等待播放列表加载完毕

                lis = browser.find_elements_by_class_name('mod_songlist')
                pattern = re.compile(r'https://y.qq.com/n/yqq/song/(\S+).html')

                for i in range(lis.__len__()):
                    li = lis.__getitem__(i)
                    a = li.find_element_by_class_name('js_song')
                    # 获得songid
                    href = a.get_attribute('href')
                    music_name = a.get_attribute('title').strip()

                    m = pattern.match(href)
                    songmid = m.group(1)
                    #根据songmid和musicname获取下载链接
                    url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=872989112&jsonpCallback=MusicJsonCallback06459212607938936&loginUin=11297258&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&callback=MusicJsonCallback06459212607938936&uin=11297258&songmid={0}&filename=C100{0}.m4a&guid=9136027940'.format(
                        songmid)
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                        'Origin': 'https: // y.qq.com',
                        'Referer': 'https: // y.qq.com / portal / search.html'
                    }
                    html = requests.get(url, headers=headers)
                    # 去掉jsonp
                    music_json = json.loads(re.findall(r'^\w+\((.*)\)$', html.text)[0])
                    filename = music_json['data']['items'][0]['filename']
                    vkey = music_json['data']['items'][0]['vkey']
                    qqdownload_url = 'http://dl.stream.qqmusic.qq.com/{}?vkey={}&fromtag=66'.format(filename, vkey).strip()


                    info_show =  music_name +  ' - qqmusic - ' + qqdownload_url  # 歌名+作者+链接
                    listbox_singer.insert(tk.END, info_show)  # 构造信息展示列表
                    print(info_show)
                    print(url)
                    # download_music(songmid, music_name)
            except Exception as e:
                print(e)
                print('wrong for QQMusic search %%%%%%%%%%%%%%%')
        finally:
            browser.quit()
            print('browser close successfully.')
        return listbox_singer
    except requests.ConnectionError:
        return None
