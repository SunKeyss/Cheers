# utf-8
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import os
import time
import threading
import pygame

from Selenium_Try import Try_Search, Try_Download

window = tk.Tk()  # Create instance
window.title("酱油团子")
window.geometry("900x550+200+100")  # (200,100)
window.resizable(False, False)


# 下载模块
# 自带一个self参数传递
def download_song(self):
    flag = Try_Download.Call_On_Download_Song(listbox_singer)
    if flag == True:
        download_tips.configure(text='下载' + name.get() + '  成功！')
        loadMusic()
        # time.sleep(2)
        # download_tips.configure(text='')
    else:
        download_tips.configure(text='下载' + name.get() + '  失败！')
        # time.sleep(2)
        # download_tips.configure(text='')


# 调用外函数搜索模块
# Button Function
def Click_Search():
    listbox_singer.delete(0, tk.END)
    a_lable.configure(foreground='red')
    a_lable.configure(text='You are searching   ' + name.get())
    Try_Search.CallOn_Click_Search(name, listbox_singer)


# 用来保存下载信息
# def save_json(data, path)
#     try:
#         save_path = path
#         f_obj = open(save_path, 'a')
#         f_obj.write(data)
#         f_obj.close()
#     except:
#         print('保存json信息失败')


# add a lable
a_lable = ttk.Label(window, text='请输入完整歌名或歌手')
a_lable.place(x=50, y=80, width=300, height=30)
download_tips = ttk.Label(window, text='')
download_tips.place(x=50, y=130, width=300, height=30)  # 提示下载成功或失败
listbox_singer = tk.Listbox(window, selectmode=tk.BROWSE)
listbox_singer.place(x=50, y=155, width=265, height=300)
listbox_singer.bind('<Double-Button-1>', download_song)

# add a button
action = ttk.Button(window, text='Click Me!', command=Click_Search)
action.place(x=230, y=40, width=80, height=30)
# action.configure(state='disabled')  # Disable the Button Widget

# add a text box
name = tk.StringVar()  # 声明name变量是tk.StringVar()类型的
name_enter = ttk.Entry(window, width=15, textvariable=name)
name_enter.place(x=50, y=40, width=150, height=30)
name_enter.focus_set()

'''==========================================================================================================='''

folder = 'F:\\Web_Music'
res = []
num = 0
var2 = tkinter.StringVar()


# 预加载文件夹中的歌曲
def loadMusic():
    global folder
    global res
    global lb
    global var2
    res = []  # 构建缓存队列准备播放
    ret = []  # 显示加载赋值给列表，顺序一致
    try:
        # 列表生成式
        if folder:
            # folder = tkinter.filedialog.askdirectory()  打开选取文件夹
            musics = [folder + '\\' + music
                      for music in os.listdir(folder) \
                      if music.endswith(('.mp3', '.wav', '.ogg', '.m4a'))]  # 在该目录下所有以以上格式为结尾的文件被读取
            # res = musics
            print(res)  # 检查
            for i in musics:
                ret.append(i.split('\\')[-1])
                res.append(i)
            # 将ret曲目加载到播放器,更新列表
            var2.set(ret)
        if not folder:
            return
    except Exception as e:
        print(e)
        print('文件歌曲读入错误')
    global playing
    playing = True  # 播放标记

    # 根据情况禁用和启用相应的按钮
    buttonPlay['state'] = 'normal'  # 开启
    buttonStop['state'] = 'normal'
    buttondelete['state'] = 'normal'
    pause_resume.set('播放')  # 改变组件值为播放


# 播放音乐函数
def play():
    # 初始化混音器设备
    if len(res):
        pygame.mixer.init()
        s['state'] = 'normal'
        global num
        while playing:
            if not pygame.mixer.music.get_busy():
                nextMusic = res[num]
                print(nextMusic)
                print(num)
                next_Music = nextMusic.split('\\')[-1]
                musicName.set('     正在播放....' + ''.join(next_Music))

                try:
                    pygame.mixer.music.load(nextMusic.encode())  # 加载音乐
                except:
                    print('播放空源或无法识别的格式，请尝试本地播放')
                s.set(0.5)  # 音量值初始化为0.5
                # 播放一次
                pygame.mixer.music.play(1)

                # time.sleep(0.2)
                # buttonNextClick()
                # break   #可以做一个循环和顺序变换按钮

            else:
                time.sleep(0.2)
                # print('pygame.mixer.music is busy')


# 点击播放
def buttonPlayClick():
    buttonNext['state'] = 'normal'
    buttonPrev['state'] = 'normal'

    if pause_resume.get() == '播放':
        pause_resume.set('暂停')

        global playing
        playing = True
        # 创建一个线程来播放音乐，当前主线程用来接收用户操作
        t = threading.Thread(target=play)
        t.start()
    elif pause_resume.get() == '暂停':
        # pygame.mixer.init()
        pygame.mixer.music.pause()
        pause_resume.set('继续')
    elif pause_resume.get() == '继续':
        # pygame.mixer.init()
        pygame.mixer.music.unpause()
        pause_resume.set('暂停')


# 停止播放
def buttonStopClick():
    global playing
    playing = False
    pygame.mixer.music.stop()


# 下一首
def buttonNextClick():
    global playing
    playing = False
    pygame.mixer.music.stop()
    #
    # pygame.mixer.quit()
    global num
    if len(res) - 1 == num:
        num = 0
    else:
        num = num + 1
    playing = True
    # 创建一个线程来执行播放函数，当前主线程用来接收用户操作
    t = threading.Thread(target=play)
    t.start()


# 上一首
def buttonPrevClick():
    global playing  # 定义此函数中的playing可以影响全局，即全局变量
    playing = False
    pygame.mixer.music.stop()
    # pygame.mixer.quit()
    global num
    if 0 == num:
        num = len(res) - 1
    else:
        num -= 1
    playing = True
    # 创建一个线程来播放音乐，当前主线程用来接收用户操作
    t = threading.Thread(target=play)
    t.start()


# 关闭窗口
def closeWindow():
    # 修改变量，结束线程中的循环
    global playing
    playing = False
    time.sleep(0.3)
    try:
        # 停止播放，如果已停止，
        # 再次停止时会抛出异常，所以放在异常处理结构中
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        time.sleep(1.5)
        window.destroy()
    except:
        pass
        window.destroy()


# 声音控制
def control_voice(value=0.5):
    # 设置背景音乐的音量。取值从0.0到1.0。在新的音乐加载前设置,音乐播放时生效。
    # 注意; 音乐播放时生效
    pygame.mixer.music.set_volume(float(value))


# 双击响应播放函数
def pickplay(self):
    buttonNext['state'] = 'normal'
    buttonPrev['state'] = 'normal'
    pause_resume.set('暂停')
    # 停止播放
    global playing
    playing = False
    try:
        pygame.mixer.music.stop()
        time.sleep(0.3)
    except:
        pass
    # 处理序号
    global num
    num = lb.index(lb.curselection())
    print('=======================    num turn to:' + str(num))

    playing = True
    # 创建一个线程来执行播放函数，当前主线程用来接收用户操作
    t = threading.Thread(target=play)
    t.start()


# 删除函数
def deletemusic():
    try:
        delete_name = lb.get(lb.curselection())
        file_path = 'F:\\Web_Music\\' + delete_name
        os.remove(file_path)
        print('删除成功 ：   ' + delete_name)
        time.sleep(0.2)
        # 更新列表
        loadMusic()
        pause_resume.set('暂停')  # 改变组件值为播放
    except Exception as e:
        print(e)
        print('删除操作失败')


window.protocol('WM_DELETE_WINDOW', closeWindow)  # 通过协议去监测窗口 调用方法

# 右边列表
lb = tkinter.Listbox(window, listvariable=var2)  # 将加载的变量集合带过来赋值显示
lb.place(x=450, y=155, width=300, height=300)
lb.bind('<Double-Button-1>', pickplay)

# 删除歌曲
buttondelete = tkinter.Button(window, text='删除此曲', command=deletemusic)
buttondelete.place(x=800, y=165, width=80, height=40)
buttondelete['state'] = 'disabled'

# 加载
buttonChoose = tkinter.Button(window, text='加载', command=loadMusic)  # 预加载音乐
buttonChoose.place(x=450, y=40, width=50, height=20)

# 播放
#  控制按钮的状态
pause_resume = tkinter.StringVar(window, value='播放')
buttonPlay = tkinter.Button(window, textvariable=pause_resume, command=buttonPlayClick)
buttonPlay.place(x=590, y=40, width=50, height=20)
buttonPlay['state'] = 'disabled'

# 停止播放
buttonStop = tkinter.Button(window, text='停止', command=buttonStopClick)
buttonStop.place(x=520, y=40, width=50, height=20)
buttonStop['state'] = 'disabled'

# 下一首
buttonNext = tkinter.Button(window, text='下一首', command=buttonNextClick)
buttonNext.place(x=660, y=40, width=50, height=20)
buttonNext['state'] = 'disabled'

# 上一首
buttonPrev = tkinter.Button(window, text='上一首', command=buttonPrevClick)
buttonPrev.place(x=730, y=40, width=50, height=20)
buttonPrev['state'] = 'disabled'

musicName = tkinter.StringVar(window, value='请先加载音乐...')  # StringVar对象用来跟踪变量
labelName = tkinter.Label(window, textvariable=musicName)
labelName.place(x=430, y=70, width=400, height=20)

# HORIZONTAL表示为水平放置，默认为竖直,竖直为vertical
s = tkinter.Scale(window, label='', from_=0, to=1, orient=tkinter.HORIZONTAL,
                  length=200, showvalue=1, tickinterval=10, resolution=0.1, command=control_voice)  # 分成10段
s.place(x=450, y=90, width=300)
s['state'] = 'disabled'

window.mainloop()  # Start GUI
