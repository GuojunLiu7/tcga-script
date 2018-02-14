import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from textwrap import wrap

def calculate(value):
	if (0 > value >= -0.001):
		return(-4)
	elif (-0.001 > value >= -0.01):
		return(-3)
	elif (-0.01 > value >= -0.05):
		return(-2)
	elif (-0.05 > value >= -0.1):
		return(-1)
	elif ((value < -0.1) | (value > 0.1)):
		return(0)
	elif (0.1 >= value > 0.05):
		return(1)
	elif (0.05 >= value > 0.01):
		return(2)
	elif (0.01 >= value > 0.001):
		return(3)
	elif (0.001 >= value > 0):
		return(4)
	

with open("gene.txt") as f:
	lines = f.read().split('\n')

file = "total_summary.csv"
df = pd.read_csv(file, sep = '\t')
df['calculate'] = df['logrank_P'].apply(calculate)
df['name'] = df['disease'] + df['subgroup']

df.reindex(lines)
u = df.pivot(index='gene', columns='name', values='calculate')
t = u.reindex(lines)
#print(u)
plt.subplots(figsize = (650,15))
plt.subplot_tool()
ax = sns.heatmap(t, annot=False, fmt="d", linewidths=.5, cmap="PiYG")
xticks = t.columns
yticks = t.index
xticks = [ '\n'.join(wrap(l, 40)) for l in xticks ]
ax.set_xticklabels(xticks, fontsize = 5)
ax.set_yticklabels(yticks, fontsize = 5)
#ax = sns.heatmap(data, vmin=-4, vmax=4)
cbar = ax.collections[0].colorbar
cbar.set_ticks([-4, -3, -2, -1, 0, 1, 2, 3, 4])
cbar.set_ticklabels(['Unfavorable p<0.001', "p<0.01", "p<0.05", "p<0.1", "NS", "p<0.1", "p<0.05", "p<0.01", "Favorable p<0.001"])

plt.savefig('total.svg')
