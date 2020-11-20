from psychopy import visual
import pandas as pd
import numpy as np
from experiment_classes import Experiment, VisualTrial

# This is a very simple reaction-time experiment, that simply asks you to
#   respond as quickly as possible after a stimulus has been presented.
# It's simply a mock experiment to show you how it works.

# Initialize the experiment
experiment = Experiment((800, 600), (-1, -1, -1), (1, 1, 1))

# Load one of the stimuli files as a dataframe
stimuli = pd.read_csv('picture_verification_stimuli.csv')

# Turn the stimuli into trials
trials = []
for i, row in stimuli.iterrows():
    image = visual.ImageStim(experiment.window, image=row['image_file'])
    trials.append(VisualTrial(experiment, row['item'] + '_image', image))

# Here we randomly permute the trials
trials = np.random.permutation(trials)

# Show a starting screen
experiment.show_message('You will be shown a series of images, ' +
                        'press z or m as quickly as possible after an image is shown. ' +
                        'Press any key to start the experiment.')

# Run through all the trials
results = []
for trial in trials:
    result = trial.run()
    results.append(result)

# Create a dataframe based on the results, and store them to a csv file
results = pd.DataFrame(results)
results['reaction_time'] = results['end_time'] - results['start_time']  # Calculate all the reaction times
results.to_csv('results.csv')
