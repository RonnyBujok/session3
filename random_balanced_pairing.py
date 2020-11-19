import numpy as np

# Given a list of elements:
elements = [1, 2, 3, 4]

# First, randomly permute the list:
# For example: 2, 4, 3, 1
elements = np.random.permutation(elements)
print(elements)

# Then, create a second list with all element shifted one position (the first element becoming the last):
# For example: 4, 3, 1, 2
distractors = np.concatenate((elements[1:], elements[:1]))
print(distractors)

# Then, pair these two lists together:
# For example:
# 2, 4, 3, 1
# 4, 3, 1, 2
# > (2, 4), (4, 3), (3, 1), (1, 2)
pairs = list(zip(elements, distractors))
print(pairs)

# Finally, permute this list of pairs again:
# For example: (3, 1), (2, 4), (4, 3), (1, 2)
pairs = np.random.permutation(pairs)
print(pairs)

# You can access the values in these pairs in a for-loop as follows:
for cue, target in pairs:
    print(f'{cue} is paired with {target}')

# This will result in a random order of cues, paired with random distractor targets,
#   while each target only occurs once.
