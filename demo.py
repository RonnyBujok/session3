from psychopy import visual, sound, core

window = visual.Window((400, 400))
note_c = sound.Sound('C', secs=1)
note_g = sound.Sound('G', secs=1)
message = visual.TextStim(window)

message.text = 'hello'
message.draw()
window.flip()
note_c.play()
core.wait(2.0)

message.text = 'world'
message.draw()
window.flip()
note_g.play()
core.wait(2.0)
