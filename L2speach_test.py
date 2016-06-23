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

introMessage = "Welcome to our cognitive brain Test! \nYou will be given a break at the end of movie. Please rest for as long as you need to during the breaks given, or continue to the next round if you are able to power through!\nPlease ensure that you are in a quiet room and have earphones to listen to the words before starting the task.\nPress SPACEBAR when you are ready."

restMessage = "You can now take a break for as long as you need to before continuing.\nPlease press SPACEBAR when you are ready to continue."

halfwayMessage = "WELL DONE! You are halfway done!\n"+restMessage

goodbyeMessage = "You have now come to the end of our experiment.\nFor more information on our study, please refer to our debrief notes.\nThank you for your time and participation!"

Symbols = 'L R'.split()

orderFile = 'C:/Users/sun/Downloads/Nanyang/leapEEG/order.txt'

AudioDir = 'C:/Users/sun/Downloads/Nanyang/real/'
AudioFiles = os.listdir(AudioDir)
StimsAudio = [ sound.Sound(AudioDir+filename) for filename in AudioFiles ]

intro = visual.TextStim(win, text=introMessage, height = .07, wrapWidth = 1.5)
rest = visual.TextStim(win, text=restMessage)
halfway = visual.TextStim(win, text=halfwayMessage)
goodbye = visual.TextStim(win, text=goodbyeMessage)

mov = visual.MovieStim(win, name='mov',filename=u'movie.mp4', size=[480,360], flipVert=False, flipHoriz=False, loop=False)

#enable parallel port access with:
#sudo modprobe -r lp

#port = parallel.ParallelPort('/dev/paAurport0')
#core.wait(2)
#port.setData(0)

data = []


def setSymbols():
    lookupDict = {}
    for symbol, audio in zip(Symbols, StimsAudio):
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
isi=0

while continueMovie:
    t = testClock.getTime()
    frameN = frameN + 1
    
    if t >= 0.0 and mov.status == NOT_STARTED:
        # keep track of start time/frame for later
        mov.tStart = t  # underestimates by a little under one frame
        mov.frameNStart = frameN  # exact frame index
        mov.setAutoDraw(True)
        
    if t >= isi:
        if LRorder['symbols'][num] == 'L':
            print("L")
            #port.setData(1)
        elif LRorder['symbols'][num] == 'R':
            #port.setData(2)
            print("R")
        else:
            print("there is error for LRorder")
        audioPlay(num).tStart = t  # underestimates by a little under one frame
        audioPlay(num).frameNStart = frameN  # exact frame index
        audioPlay(num).play()
        num = num + 1
        isi = isi + 3
        #port.setData(0)
    if mov.status == FINISHED:  # force-end the routine
        continueMovie = False
    
#    mov.draw()
#    win.flip()
    if event.getKeys(keyList=['escape','q']):
        win.close()
        core.quit()
        
    
    # refresh the screen
    if continueMovie:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()
    


rest.draw()
win.flip()
event.waitKeys(keyList=['space'])

goodbye.draw()
win.flip()
event.waitKeys(keyList=['space'])
win.close()
core.quit()



