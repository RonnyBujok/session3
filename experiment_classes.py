from psychopy import core, visual, event

# This class defines the general experiment properties, like the window and text color.
# It also provides some helper methods to show the fixation cross or a message on the screen.
class Experiment:
    def __init__(self, window_size, text_color, background_color):
        self.text_color = text_color
        self.window = visual.Window(window_size, color=background_color)
        self.fixation = visual.TextStim(self.window, text='+', color=text_color)
        self.clock = core.Clock()
    
    # Show the given message on the experiment window and wait until a key is pressed.
    def show_message(self, message):
        stimulus = visual.TextStim(self.window, text=message, color=self.text_color)
        stimulus.draw()
        self.window.flip()
        event.waitKeys()
    
    # Show a fixation cross on the experiment window for the given amount of time.
    def show_fixation(self, time=0.5):
        self.fixation.draw()
        self.window.flip()
        core.wait(time)

# This class defines a single item of an experiment, and serves as a helper to generate image and text trials.
class Item:
    def __init__(self, experiment, name, image):
        self.name = name
        self.experiment = experiment
        self.text = visual.TextStim(experiment.window, text=name, color=experiment.text_color)
        self.image = visual.ImageStim(experiment.window, image=image)
    
    # Create a visual trial for showing the image.
    def get_image_trial(self, fixation_time=0.5, max_key_wait=5, keys=['z', 'm']):
        return VisualTrial(self.experiment, f'{self.name}_image', self.image, fixation_time=fixation_time, max_key_wait=max_key_wait, keys=keys)
    
    # Create a visual trial for showing the word.
    def get_text_trial(self, fixation_time=0.5, max_key_wait=5, keys=['z', 'm']):
        return VisualTrial(self.experiment, f'{self.name}_text', self.text, fixation_time=fixation_time, max_key_wait=max_key_wait, keys=keys)

# This class defines a single visual trial of an experiment.
class VisualTrial:
    def __init__(self, experiment, name, stimulus, fixation_time=0.5, max_key_wait=5, keys=['z', 'm']):
        self.name = name
        self.experiment = experiment
        self.stimulus = stimulus
        self.fixation_time = fixation_time
        self.max_key_wait = max_key_wait
        self.keys = keys
    
    # Runs the current trial.
    def run(self):
        # Show the trial
        self.experiment.show_fixation(self.fixation_time)
        self.stimulus.draw()
        self.experiment.window.flip()
        
        # Wait for user input
        start_time = self.experiment.clock.getTime()  # You could also start a new clock for each user input
        keys = event.waitKeys(maxWait=self.max_key_wait, keyList=self.keys, timeStamped=self.experiment.clock, clearEvents=True)
        if keys is not None:
            key, end_time = keys[0]
        else:  # If no keys were pressed:
            key = None
            end_time = self.experiment.clock.getTime()
        
        # Return the results
        return {
            'trial': self.name,
            'key': key,
            'start_time': start_time,
            'end_time': end_time
        }
