from psychopy import visual, sound, event, core
import pandas as pd
import numpy as np

# You may need to specify the full file path if you're working in the standalone version of Psychopy
# In that case, it might be useful to define your folder root location here, and replace other paths with
#   root + '/path/to/file.png'

# Create the experiment window with a given size and background color
window = visual.Window((800, 600), color=(1, 1, 1))

# Create a fixation cross with a given color
fixation = visual.TextStim(window, text='+', color=(-1, -1, -1))

# Show the fixation cross for 1 second
fixation.draw()
window.flip()
core.wait(1.0)

# Show a Gabor grating for 2 seconds
gabor = visual.GratingStim(window, tex='sin', mask='gauss', sf=10, name='gabor')
gabor.draw()
window.flip()
core.wait(2.0)

# Show an image for 2 seconds
image = visual.ImageStim(window, image='images/car.png')
image.draw()
window.flip()
core.wait(2.0)

# Play a sound
audio = sound.Sound('sounds/HF/auto.wav')
fixation.draw()
window.flip()
audio.play()
core.wait(audio.getDuration())

# Different timing methods
core.wait(2.0)  # wait for 2 seconds

# The following method allows you some more control about what happens while showing a stimulus
# e.g. you could animate it, add different stages, record intermediate timings, mouse movements or key presses
clock = core.Clock()
while clock.getTime() < 2:  # wait for (at least) 2 seconds
    fixation.draw()
    window.flip()
print(clock.getTime())

# The two methods above might be imprecise due to screen refresh rate timings
# To ensure perfect timing, count frames rather than seconds
# Note that this only works if no frames are dropped, which requires particular hardware settings
fixation.draw()
window.flip()
clock = core.Clock()  # start counting on the first frame flip
for i in range(99):  # wait for 100 frames (exactly): the 1 before and 99 here
    fixation.draw()
    window.flip()
window.flip()  # clear the fixation cross (it remains visible until the screen is flipped again)
print(clock.getTime())

# Record a user keypress (either z or m) and its timing
clock = core.Clock()
keys = event.waitKeys(maxWait=5, keyList=['z', 'm'], timeStamped=clock, clearEvents=True)
if keys is not None:
    key, reaction_time = keys[0]
    # The above line does the same as the following two lines combined:
    # key = keys[0][0]
    # reaction_time = keys[0][1]
else:  # If no keys were pressed:
    key = None
    reaction_time = 5
print(f'{key} was pressed after {reaction_time} seconds!')

# Load one of the stimuli files as a dataframe
stimuli = pd.read_csv('picture_verification_stimuli.csv')

# This is a way of looping over all the rows; we're using another way here, see below.
# for i, row in stimuli.iterrows():
#     print(row['image_file'])

# This is a way of looping over all the values in a given column.
# We use this to create a PsychoPy ImageStim for each stimulus.
images = []
for image in stimuli['image_file']:
    images.append(visual.ImageStim(window, image=image))

# Here we randomly permute the stimuli
images = np.random.permutation(images)

# This is a very simple reaction-time experiment, that simply asks you to
#   respond as quickly as possible after an image has been presented.
# It's simply a mock experiment to show you how it works.
clock = core.Clock()  # Start an overall experiment clock
results = []
for image in images:
    # Show the trial
    fixation.draw()
    window.flip()
    core.wait(0.5)

    image.draw()
    window.flip()
    
    # Wait for user input
    start_time = clock.getTime()  # You could also start a new clock for each user input
    keys = event.waitKeys(maxWait=5, keyList=['z', 'm'], timeStamped=clock, clearEvents=True)
    if keys is not None:
        key, end_time = keys[0]
    else:  # If no keys were pressed:
        key = None
        end_time = clock.getTime()
    
    # Store the results
    results.append({
        'image': image.image,
        'key': key,
        'start_time': start_time,
        'end_time': end_time
    })

# Create a dataframe based on the results, and store them to a csv file
results = pd.DataFrame(results)
results['reaction_time'] = results['end_time'] - results['start_time']  # Calculate all the reaction times
results.to_csv('results.csv')
