import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

results = pd.read_csv('results.csv')

# I just have one participant so I don't need to loop over participants to get the trials
# if I had several participants I would create a new dataframe and append all trials to it similar to the lecture

summary = results.groupby(by='type').aggregate( #multiple columns (by='id', 'condition')
    mean_RT = pd.NamedAgg('reaction_time',np.mean),
    std_RT = pd.NamedAgg('reaction_time',np.std)
)

#show general reaction times per item type. With LF and HF apart
sns.boxplot(x="type", y="reaction_time", data=results)
plt.show()

#show non-word vs. word comparison
results= results.replace(to_replace=["HF","LF"],value="word")
sns.boxplot(x="type", y="reaction_time", data=results)
plt.show()

#show LF vs. HF. comparison
results = pd.read_csv('results.csv')
results = results[results['type'] != 'none']
sns.boxplot(x="type", y="reaction_time", data=results)
plt.show()


#compare % correct responses between HF and LF words
results = pd.read_csv('results.csv')
results_HF = results[results['type'] == "HF"]
correct_HF = sum(results_HF['response_correct'])*2
results_LF = results[results['type'] == "LF"]
correct_LF = sum(results_LF['response_correct'])*2

#create new data frame with the percentage of correct responses
data = {
    'freq':['HF','LF'],
    'correct':[correct_HF,correct_LF]
}
errordf = pd.DataFrame(data, columns= ['freq','correct'])

sns.barplot(x="freq", y="correct", data=errordf)
plt.show()


# just out of curiosity let's compare the error rates between nonwords and HF and LF words
results_NW = results[results['type'] == 'none']
correct_nw = sum(results_NW['response_correct'])

data = {
    'type':['HF','LF','NW'],
    'correct':[correct_HF,correct_LF,correct_nw]
}
errordf = pd.DataFrame(data, columns= ['type','correct'])

sns.barplot(x="type", y="correct", data=errordf)
plt.show()