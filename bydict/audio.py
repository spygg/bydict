#!/usr/bin/env python
# coding=utf-8
from pydub import AudioSegment
from pydub.playback import play
import urllib.request
import tempfile
from multiprocessing import Process
import sys
import logging
import threading

def play_mp3(filename):
    if not filename:
        return

##    l = logging.getLogger("pydub.converter")
##    l.setLevel(logging.DEBUG)
##    l.addHandler(logging.StreamHandler())
    
    if filename.startswith("http"):
        try:
            mp3file = urllib.request.urlopen(filename)
            with tempfile.NamedTemporaryFile() as tmpfile:
                tmpfile.write(mp3file.read())
                tmpfile.seek(0)
                song = AudioSegment.from_mp3(tmpfile)
                play(song)
                return
        except:
            print("Open file From Url failed")
            return

    else:
        song = AudioSegment.from_mp3(filename)
        play(song)

    print('Finsh play')

#尝试使用线程,失败!
def play_mp3_by_thread(filename):
    print("here start")
    t = threading.Thread(target=_play, args = (filename,))
    t.start()

#尝试使用进程,失败!     
def play_mp3_by_process(filename):
    p = Process(target=play, args=(filename,))
    p.start()
    p.join()
        
if __name__ == '__main__':
    filename = 'https://dictionary.blob.core.chinacloudapi.cn/media/audio/tom/d8/6c/D86CEAEFA3504E6E1368552B058AD528.mp3'
    play_mp3(filename)
    print("finshed!")

