# Lexical Decision Task

from psychopy import visual, sound, event, core
import pandas as pd
import numpy as np

#-----------------------defining all the variables-------------------------------

window = visual.Window((800,600),color=(1,1,1)) #grey is default
fixation = visual.TextStim(window, text='+', color=(-1,-1,-1)) #position is by default in the middle
word = visual.TextStim(window, text='word?', color=(1,-1,-1))
noyes = visual.TextStim(window, text='no                          yes', color=(-1,-1,-1),pos=(0,-0.3)) #position is by default in the middle
instructions = visual.TextStim(window, text='This is a lexical decision task.\n\nIf you think you hear a word press "m". If you think you hear a nonword press "z"\n\nPress SPACE to start!', color=(-1,-1,-1))
stimuli = pd.read_csv('lexical_decision_stimuli.csv')

audios = []
hf_path = 'sounds/HF/'
lf_path = 'sounds/LF/'
nw_path = 'sounds/NW/'

#-----------------------preloading all the stimuli and randomizing ----------------------------

for i,row in stimuli.iterrows():
    templist = []
    if row['freq_category'] == 'LF':
        templist.append(sound.Sound(lf_path+row['word']+'.wav'))
        templist.append(row['word'])
    if row['freq_category'] == 'HF':
        templist.append(sound.Sound(hf_path+row['word']+'.wav'))
        templist.append(row['word'])
    if row['freq_category'] == 'none':
        templist.append(sound.Sound(nw_path+row['word']+'.wav'))
        templist.append(row['word'])
    audios.append(templist)

audios = np.random.permutation(audios)

clock = core.Clock()
results = []


#----------------instructions-----------------

while True:
    instructions.draw()
    window.flip()
    keys = event.waitKeys(keyList=['space'])
    if keys == 'space':
        break
    break

#--------------------task-----------------------

for audio in audios:
    fixation.draw()
    window.flip()
    core.wait(1)

    audio[0].play()
    noyes.draw()
    word.draw()
    window.flip()
    start_time = clock.getTime()
    keys = event.waitKeys(maxWait=5,keyList=['z','m'], timeStamped=clock, clearEvents=True) #timestamp shows that the first item in the list is earlier
    if keys is not None:
        if keys[0][0] == 'm':
            key, end_time = keys[0]
            answer = 'yes'
        if keys[0][0] == 'z':
            key, end_time = keys[0]
            answer = 'no'
    else:
        key = None
        end_time = clock.getTime()
        answer = 'timeout'

#---------------------output------------------

    results.append({
        'audio': audio[1],
        'key': key,
        'answer': answer,
        'reaction_time': end_time - start_time
    })

results = pd.DataFrame(results)
results.to_csv('results.csv')


