#-*- coding: utf-8 -*-

from psychopy import visual
import time

win = visual.Window(size=(800, 800), fullscr=False, allowGUI=False, allowStencil=False, monitor=u'testMonitor', color=[0,0,0], colorSpace='rgb', blendMode='avg', useFBO=False)

instru_text_1 = visual.TextStim(win=win, ori=0, name='instru_text_1',
    text=u"欢迎参加实验。在本实验中你会在屏幕上读到一些句子。首先你会在屏幕正中央看到一个十字标志：\n\n",    font='',
    pos=[0, 0.2], height=0.085, wrapWidth=None, 
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0, 
    )

instru_text_1.setSize(5)

instru_text_1.setAutoDraw(True)
win.flip()

time.sleep(7)