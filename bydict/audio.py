#!/usr/bin/env python
# coding=utf-8

import urllib.request
import tempfile
import sys
import logging

try:
    import playsound
except:
    from pydub import AudioSegment
    from pydub.playback import play


def play_mp3(filename):
    if not filename:
        return
    playsound.playsound(filename)
        
def play_mp3_pydub(filename):
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

        
if __name__ == '__main__':
    filename = 'https://dictionary.blob.core.chinacloudapi.cn/media/audio/tom/d8/6c/D86CEAEFA3504E6E1368552B058AD528.mp3'
    play_mp3(filename)
    
    print("finshed!")

