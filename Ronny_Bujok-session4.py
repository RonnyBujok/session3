# Lexical Decision Task

#I know that I could put the classes in a separate document but for convenience I have only one document

from psychopy import visual, sound, event, core
import pandas as pd
import numpy as np


#------------------------------- Classes -----------------------------------------

class Experiment:
    def __init__(self,window_size,text_color,background_color):
        self.text_color = text_color
        self.window = visual.Window(window_size, color=background_color)
        self.text = visual.TextStim(self.window, text='Word?\n\nNo               Yes', color=self.text_color)
        self.fixation = visual.TextStim(self.window, text='+',color=self.text_color)
        self.clock = core.Clock()

    def show_message(self,message):
        stimulus = visual.TextStim(self.window, text=message, color=self.text_color)
        stimulus.draw()
        self.window.flip()
        keys = event.waitKeys(keyList=['space'])
        if keys == 'space':
            return

    def show_fixation(self,time=0.5):
        self.fixation.draw()
        self.window.flip()
        core.wait(time)

    def show_trial(self):
        self.text.draw()

class Trial:
    def __init__(self, experiment, stimulus, name, type, fixation_time=0.5, max_key_wait=5, keys=['z', 'm']):
        self.name = name
        self.stimulus = stimulus
        self.type = type
        self.experiment = experiment
        self.fixation_time = fixation_time
        self.max_key_wait = max_key_wait
        self.keys = keys

    def run(self):
        self.experiment.show_fixation(self.fixation_time)
        self.experiment.window.flip()
        self.stimulus.play()
        self.experiment.show_trial()
        self.experiment.window.flip()

        start_time = self.experiment.clock.getTime()
        keys = event.waitKeys(maxWait=self.max_key_wait, keyList=self.keys, timeStamped=self.experiment.clock,
                              clearEvents=True)  # timestamp shows that the first item in the list is earlier
        if keys is not None:
            if keys[0][0] == 'm':
                key, end_time = keys[0]
            if keys[0][0] == 'z':
                key, end_time = keys[0]
        else:
            key = None
            end_time = self.experiment.clock.getTime()

        # ---------------------output------------------

        return{
            'word': self.name,
            'type': self.type,
            'key': key,
            'reaction_time': end_time - start_time
        }


#-----------------------preloading all the stimuli and randomizing ----------------------------


experiment = Experiment((800,600),(-1,-1,-1),(1,1,1))
stimuli = pd.read_csv('lexical_decision_stimuli.csv')

audios = []
hf_path = 'sounds/HF/'
lf_path = 'sounds/LF/'
nw_path = 'sounds/NW/'

# I'm pretty sure I could make a class out of this as well but I have spent quite some time on it and couldn't make it work

for i,row in stimuli.iterrows():
    templist = []
    if row['freq_category'] == 'LF':
        templist.append(sound.Sound(lf_path+row['word']+'.wav'))
        templist.append(row['word'])
        templist.append(row['freq_category'])
    if row['freq_category'] == 'HF':
        templist.append(sound.Sound(hf_path+row['word']+'.wav'))
        templist.append(row['word'])
        templist.append(row['freq_category'])
    if row['freq_category'] == 'none':
        templist.append(sound.Sound(nw_path+row['word']+'.wav'))
        templist.append(row['word'])
        templist.append(row['freq_category'])
    audios.append(Trial(experiment,templist[0], templist[1],templist[2]))
audios = np.random.permutation(audios)

# Show a starting screen
experiment.show_message('This is a lexical decision task.\n\nIf you think you hear a word press "m". If you think you hear a nonword press "z"\n\nPress SPACE to start!')

#Run trials and append results
results=[]
for audio in audios:
    result = audio.run()
    results.append(result)

results = pd.DataFrame(results)
results.to_csv('results.csv')



