#utf-8
import requests
from urllib.request import urlretrieve


def Call_On_Download_Song(listbox_singer):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Origin': 'https: // y.qq.com',
        'Referer': 'https: // y.qq.com / portal / search.html'
    }
    try:
        print('下载:' + listbox_singer.get(listbox_singer.curselection()))
        info_murl = listbox_singer.get(listbox_singer.curselection()).split(' - ')[-1]
        info_mname = listbox_singer.get(listbox_singer.curselection()).split(' - ')[0] \
                     + '-' +listbox_singer.get(listbox_singer.curselection()).split(' - ')[1]
        result = requests.get(info_murl, headers=headers, stream=True)
        path = r'F:\\Web_Music\\' + info_mname + '.mp3'

        print(info_murl)
        print(info_mname)
        print(path)
        #download modle


        try:
            # 下载mp3文件
            # urlretrieve(info_murl, path)
            with open(path, 'wb') as f:
                f.write(result.content)
            print('下载成功')
            return True
        except Exception as e:
            print(e)
            print('该版本获取失败！')

        # #播放音乐
        # pygame.mixer.init()
        # track = pygame.mixer_music.load(path)
        # while True:
        #     if pygame.mixer_music.get_busy()==False:
        #         pygame.mixer_music.play()
        # time.sleep(20)
        # pygame.mixer_music.stop()
    except Exception as e:
        print(e)
        return False
