import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
from lifelines import KaplanMeierFitter

file = "X:\\Su Lab\\TCGA\\Data\\Matrix\\TCGA-BRCA-total-matrix.csv"
matrix = pd.read_csv(file, sep = '\t')

def is_number(s):
	if pd.isnull(s):
		return False
	else:
		try:
			float(s)
			return True
		except ValueError:
			return False
		except TypeError:
			return False
		
def event(c):
	if c['vital_status'] == "dead":
		return 1
	elif c['vital_status'] == "alive":
		return 0
def duration(c):
	if is_number(c['days_to_death']) == True:
		t = float(c['days_to_death'])*4/(365*3 + 366) 
		return t
	elif is_number(c['year_of_birth']) == True and is_number(c['age_at_diagnosis']) == True and is_number(c['days_to_death']) == False:
		t = 2018 - float(c['year_of_birth']) - (float(c['age_at_diagnosis'])*4/(365*3 + 366))
		return t
	else:
		return "NotApplicable"

matrix['duration'] = matrix.apply(duration, axis = 1)
matrix['event'] = matrix.apply(event, axis = 1)
matrix = matrix[['bcr_sample_barcode', 'duration', 'event']]
#new_header = matrix.iloc[0] #grab the first row for the header
#matrix = matrix[1:] #take the data less the header row
#matrix.columns = new_header
matrix = matrix[matrix['duration']!="NotApplicable"]


kmf = KaplanMeierFitter()
kmf.fit(durations = matrix.duration, event_observed = matrix.event)

kmf.survival_function_

# plot the KM estimate
kmf.plot()
# Add title and y-axis label
plt.title("The Kaplan-Meier Estimate for BRCA (total)")
plt.ylabel("Probability a patient is still active")

plt.show()


