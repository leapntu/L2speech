# -*- coding: utf-8 -*-
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from psychopy import visual, core, parallel, event, gui, sound
import pyglet, os, random, copy
from pyo import *
import sys # to get file system encoding
from psychopy.constants import *  # things like STARTED, FINISHED

###ENVIRONMENT AND LOADING###
win = visual.Window([1920,1280])
    
loadMessage = visual.TextStim(win, text="Loading Stimuli\n\nPlease Wait")
loadMessage.draw()

win.flip()

info = []



def get_metadata():
  global info
  myDlg = gui.Dlg(title="JWP's experiment")
  myDlg.addText('Participant Information')
  myDlg.addField('Name:')
  myDlg.addField('Age:')
  myDlg.addText('Experiment Information')
  myDlg.addField('RA:')
  myDlg.show()
  if myDlg.OK:
      info = myDlg.data
  else:
      print 'user cancelled'
      
get_metadata()

###CONSTANTS AND PARAMETERS###

preIntroMessage = "Welcome to the LEAP Lab!\n We have prepared some tests for you to measure your ability to distinguish English sounds.\n The whole testing session will take about 1 and half hour including the break time.\n It is important that you pay attention during each test. If you feel tired you can always take a break after each test. \n If you have any questions, please ask the assistant before and after each test.\n\n Ready? Let's begin! Press the 'SPACEBAR' to begin."
preIntroMessageJa = "LEAPラボへようこそ！\n私たちは、英語の発音をあなたがどれくらい聞き取れているかを測るテストをいくつか用意しました。\n全体のテストセッションは、休憩時間を含めて約1時間半かかります。\nテスト中は、集中して受けてください。\n疲れを感じた場合は、各テストセッション終了後に休憩をとることができます。\n質問がある場合は、それぞれのテストの前後にアシスタントに聞いてください。\n\n準備はよろしいですか？ それでは、はじめます!\n  [スペースキー]を押して開始してください。"

introMessage = "For this test, you will watch a silent cartoon of the movie, while listening to English sounds.\n Please sit comfortably on your chair and try to stay comfortably still, without moving your head, arms and hands too much. \n At the end of the movie, I will ask you about the movie so please focus on it.\nAfter that, you can take a rest for as long as you need to.\n \nPress SPACEBAR when you are ready."
introMessageJa = "このテストでは、英語の音を聞きながら映画のサイレント漫画を観てもらいます。\n快適な椅子に座り、頭や腕や手をあまり動かさないようにしてください。 \n映画が終わったら、映画についてお聞きするので、注意してご覧ください。 \nそのあとで、必要であれば休憩をとるとこができます。 \n\n準備が出来たら、[スペースキー]を押してください。 "

restMessage = "You can now take a break for as long as you need to before continuing.\n Please press SPACEBAR when you are ready to continue."
restMessageJa = "次のテストに入る前に必要であれば休憩を取ることができます。\n 準備が出来たら、[スペースキー]を押してください。"

intro2Message = "For this test, you will also watch another silent cartoon with different sounds.\n Please sit comfortably on your chair and try to stay comfortably still, without moving your head, arms and hands too much.\n At the end of the movie, I will ask you about the movie so please focus on it.\n Please press SPACEBAR when you are ready to continue.\n" 
intro2MessageJa = "このテストでは、先程とは違うサイレント漫画を違う音と一緒に観てもらいます。\n快適な椅子に座り、頭や腕や手をあまり動かさないようにしてください。 \n映画が終わったら、映画についてお聞きするので、注意してご覧ください。\n 準備が出来たら、[スペースキー]を押してください。" 

goodbyeMessage = "You have now come to the end of first experiment.\n\n Press 'SPACEBAR' for more test."
goodbyeMessageJa = "これで、 最初の語学テストは終了です \n\n [スペースキー]を押して、終了してください。" 

Symbols = 'L R'.split()
Symbols2 = 'T D'.split()

orderFile = '/home/leapadmin/Desktop/L2speech/order.txt'
orderFile2 = '/home/leapadmin/Desktop/L2speech/order2.txt'

AudioDir = '/home/leapadmin/Desktop/L2speech/real/'
AudioDir2 = '/home/leapadmin/Desktop/L2speech/real2/'
AudioFiles = os.listdir(AudioDir)
AudioFiles2 = os.listdir(AudioDir2)
StimsAudio = [ sound.Sound(AudioDir+filename) for filename in AudioFiles ]
StimsAudio2 = [ sound.Sound(AudioDir2+filename) for filename in AudioFiles2 ]

preintro = visual.TextStim(win, text=preIntroMessage, height = .07, wrapWidth = 1.5)
intro = visual.TextStim(win, text=introMessage, height = .07, wrapWidth = 1.5)
rest = visual.TextStim(win, text=restMessage,pos = (0,0.4), height = .07, wrapWidth = 1.5)
intro2 = visual.TextStim(win, text=intro2Message, height = .07, wrapWidth = 1.5)
goodbye = visual.TextStim(win, text=goodbyeMessage,height = .07,pos = (0,0.4), wrapWidth = 1.5)

preintroJa = visual.TextStim(win, text=preIntroMessageJa, height = .06, wrapWidth = 1.5,font='TakaoMincho')
introJa = visual.TextStim(win, text=introMessageJa, height = .07, wrapWidth = 1.5,font='TakaoMincho')
restJa = visual.TextStim(win, text=restMessageJa,pos = (0,-0.4),font='TakaoMincho', height = .07, wrapWidth = 1.5)
intro2Ja = visual.TextStim(win, text=intro2MessageJa, height = .07, wrapWidth = 1.5,font='TakaoMincho')
goodbyeJa = visual.TextStim(win, text=goodbyeMessageJa,height = .07,pos = (0,-0.4), wrapWidth = 1.5,font='TakaoMincho')

mov = visual.MovieStim(win, name='mov',filename=u'mov.mp4', size=[480,360], flipVert=False, flipHoriz=False, loop=False)
mov2 = visual.MovieStim(win, name='mov2',filename=u'mov2.mp4', size=[480,360], flipVert=False, flipHoriz=False, loop=False)

#enable parallel port access with:
#sudo modprobe -r lp

preintro.draw()
win.flip()
event.waitKeys(keyList=['space'])
preintroJa.draw()
win.flip()
event.waitKeys(keyList=['space'])

port = parallel.ParallelPort('/dev/parport0')
core.wait(2)
port.setData(0)

data = []


def setSymbols():
    lookupDict = {}
    for symbol, audio in zip(Symbols, StimsAudio):
        lookupDict[symbol] = [audio]
    return lookupDict
    
def setSymbols2():
    lookupDict = {}
    for symbol, audio in zip(Symbols2, StimsAudio2):
        lookupDict[symbol] = [audio]
    return lookupDict

def parseBlocks(orderFile):
    LRorder = { 'symbols': [] }
    parseData = { 'line': '', 'reader': open(orderFile) }
    def init(template):
        return lambda : copy.deepcopy(template)
    
    def nextline():
        parseData['line'] = parseData['reader'].readline()
    
    def getline():
        return parseData['line']
        
    nextline()
    LRorder['symbols'] = getline().split()
    return LRorder

lookup = setSymbols()
LRorder = parseBlocks(orderFile)
intro.draw()
win.flip()
event.waitKeys(keyList=['space'])
introJa.draw()
win.flip()
event.waitKeys(keyList=['space'])

print('orig movie size=%s' %(mov.size))
print('duration=%.2fs' %(mov.duration))
globalClock = core.Clock()

def audioPlay(num):
    audio = lookup[LRorder['symbols'][num]]
    return audio[0]
    

testClock = core.Clock()
testClock.reset()
continueMovie = True
t=0
frameN = -1
num=0
isi=1.2
l_port = 1

while continueMovie:
    t = testClock.getTime()
    frameN = frameN + 1
    
    
    if t >= 0.0 and mov.status == NOT_STARTED:
        # keep track of start time/frame for later
        mov.tStart = t  # underestimates by a little under one frame
        mov.frameNStart = frameN  # exact frame index
        mov.setAutoDraw(True)
        
    if t >= isi:
        port.setData(0)
        if LRorder['symbols'][num] == 'L' and LRorder['symbols'][num-1] == 'R':
            print("RL")
            port.setData(4)
        elif LRorder['symbols'][num] == 'L' and LRorder['symbols'][num-1] == 'L':
            print("L")
            if l_port == 1:
                port.setData(1)
                l_port = 2
            elif l_port == 2:
                port.setData(2)
                l_port = 1
        elif LRorder['symbols'][num] == 'R':
            port.setData(3)
            print("R")
        else:
            print("there is error for LRorder")
        audioPlay(num).tStart = t  # underestimates by a little under one frame
        audioPlay(num).frameNStart = frameN  # exact frame index
        audioPlay(num).play()
        num = num + 1
        isi = isi + 1.2
        
        
    if mov.status == FINISHED:  # force-end the routine
        continueMovie = False
    if num == 300:
        continueMovie = False
            
#    mov.draw()
#    win.flip()
    if event.getKeys(keyList=['escape','q']):
        win.close()
        core.quit()
        
    
    # refresh the screen
    if continueMovie:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

mov.setAutoDraw(False)    
core.wait(3)

rest.draw()
restJa.draw()
win.flip()
event.waitKeys(keyList=['space'])

lookup2 = setSymbols2()
TDorder = parseBlocks(orderFile2)
intro2.draw()
win.flip()
event.waitKeys(keyList=['space'])
intro2Ja.draw()
win.flip()
event.waitKeys(keyList=['space'])

print('orig movie size=%s' %(mov2.size))
print('duration=%.2fs' %(mov2.duration))

def audioPlay2(num):
    audio = lookup2[TDorder['symbols'][num]]
    return audio[0]
    
test2Clock = core.Clock()
test2Clock.reset()
continueMovie2 = True
t2=0
frameN2 = -1
num2=0
isi2=1.2
t_port = 5

while continueMovie2:
    t2 = test2Clock.getTime()
    frameN2 = frameN2 + 1
    
    
    if t2 >= 0.0 and mov2.status == NOT_STARTED:
        # keep track of start time/frame for later
        mov2.tStart = t2  # underestimates by a little under one frame
        mov2.frameNStart = frameN2  # exact frame index
        mov2.setAutoDraw(True)
        
    if t2 >= isi2:
        port.setData(0)
        if TDorder['symbols'][num2] == 'T' and TDorder['symbols'][num2-1] == 'D':
            print("DT")
            port.setData(8)
        elif TDorder['symbols'][num2] == 'T' and TDorder['symbols'][num2-1] == 'T':
            print("T")
            if t_port == 5:
                port.setData(5)
                t_port = 6
            elif t_port ==6:
                port.setData(6)
                t_port = 5
        elif TDorder['symbols'][num2] == 'D':
            port.setData(7)
            print("D")
        else:
            print("there is error for TDorder")
        audioPlay2(num2).tStart = t2  # underestimates by a little under one frame
        audioPlay2(num2).frameNStart = frameN2  # exact frame index
        audioPlay2(num2).play()
        num2 = num2 + 1
        isi2 = isi2 + 1.2
        
    if mov2.status == FINISHED:  # force-end the routine
        continueMovie2 = False
    if num2 == 300:
        continueMovie2 = False
            
#    mov.draw()
#    win.flip()
    if event.getKeys(keyList=['escape','q']):
        win.close()
        core.quit()
        
    
    # refresh the screen
    if continueMovie2:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

mov2.setAutoDraw(False)    
core.wait(3)

goodbye.draw()
goodbyeJa.draw()
win.flip()
event.waitKeys(keyList=['space'])
win.close()
core.quit()



