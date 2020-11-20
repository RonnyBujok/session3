import pandas as pd
import numpy as np
from experiment_classes import Experiment, Item

# This is a very simple reaction-time experiment, that simply asks you to
#   respond as quickly as possible after a stimulus has been presented.
# It's simply a mock experiment to show you how it works.

# Initialize the experiment
experiment = Experiment((800, 600), text_color=(-1, -1, -1), background_color=(1, 1, 1))

# Load one of the stimuli files as a list of objects
stimuli_df = pd.read_csv('picture_verification_stimuli.csv')
items = []
for i, stimulus in stimuli_df.iterrows():
    items.append(Item(experiment, name=stimulus['item'], image=stimulus['image_file']))

# Turn the items into trials (image and text), and randomly permute the trial list
trials = []
for item in items:
    trials.append(item.get_image_trial())
    trials.append(item.get_text_trial())
trials = np.random.permutation(trials)

# Show a starting screen
experiment.show_message('You will be shown a series of images and words, ' +
                        'press z or m as quickly as possible after an image or word is shown. ' +
                        'Press any key to start the experiment.')

# Run through half the trials
halfway_point = int(len(trials) / 2)  # Half the number of trials, rounded down
results = []
for trial in trials[:halfway_point]:
    results.append(trial.run())

# Show a break screen
experiment.show_message('You can now take a short break. ' +
                        'Press any key to continue the experiment.')

# Run through the remainder of the trials
for trial in trials[halfway_point:]:
    results.append(trial.run())

# Create a dataframe based on the results, and store them to a csv file
results = pd.DataFrame(results)
results['reaction_time'] = results['end_time'] - results['start_time']  # Calculate all the reaction times
results.to_csv('results.csv')
