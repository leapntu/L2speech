from psychopy import visual, core, parallel, event, gui, sound
import pyglet, os, random, copy
from pyo import *
import sys # to get file system encoding
from psychopy.constants import *  # things like STARTED, FINISHED

###ENVIRONMENT AND LOADING###
win = visual.Window([1280,1024])
    
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

introMessage = "Welcome to our cognitive brain Test! \nFor this test, you need to focus on the silent cartoon.\nWe will ask you about the cartoon at the end of movie.\nAfter that, you will have a rest time.\nPlease rest for as long as you need to during the breaks given, or continue to the next test if you are able to power through!\nPress SPACEBAR when you are ready."

restMessage = "You can now take a break for as long as you need to before continuing.\nPlease press SPACEBAR when you are ready to continue."

intro2Message = "For this test, you will also watch another silent cartoon with differnt sound.\nPlease press SPACEBAR when you are ready to continue."

goodbyeMessage = "You have now come to the end of this experiment.\nFor more information on our study, please refer to our debrief notes.\nThank you for your time and participation!"

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

intro = visual.TextStim(win, text=introMessage, height = .07, wrapWidth = 1.5)
rest = visual.TextStim(win, text=restMessage)
intro2 = visual.TextStim(win, text=intro2Message, height = .07, wrapWidth = 1.5)
goodbye = visual.TextStim(win, text=goodbyeMessage)

mov = visual.MovieStim(win, name='mov',filename=u'mov.mp4', size=[480,360], flipVert=False, flipHoriz=False, loop=False)
mov2 = visual.MovieStim(win, name='mov2',filename=u'mov2.mp4', size=[480,360], flipVert=False, flipHoriz=False, loop=False)

#enable parallel port access with:
#sudo modprobe -r lp

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
    if num == 12:
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
win.flip()
event.waitKeys(keyList=['space'])

lookup2 = setSymbols2()
TDorder = parseBlocks(orderFile2)
intro2.draw()
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
t_port = 6

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
    if num2 == 12:
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
win.flip()
event.waitKeys(keyList=['space'])
win.close()
core.quit()



