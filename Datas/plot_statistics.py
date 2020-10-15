import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import statistics as stat
from sklearn import preprocessing
import numpy as np




df = pd.read_csv("LAB_Statistics.csv")

print(type(df))

print("Dataset dimensions" ,df.shape)

print(" \n \n-------------------- \n\n Dataset head \n-------------------- \n\n\n")
print(df.head())
print(" \n \n-------------------- \n\n  Dataset info \n-------------------- \n\n \n")
df.info()

print(" \n \n-------------------- \n\n  Dataset basic stat \n-------------------- \n\n \n")

print(df.describe())

def normalize(dataset):
    return( (dataset - dataset.min())/(dataset.max() -dataset.min()))

#print( df["Timestamp"][0])

fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('')
df["Timestamp"] = list(range(0, len(df["Delta"] )))

df["Normalized_delta"] = normalize(df["Delta"])
df["Normalized_latency"] = normalize(df["Latency"] )

ax1.plot(df["Delta"] , label="Delta[ms]")
ax1.plot([ df["Delta"].mean()] *len(df["Delta"] ) ,"-", label="Average")
ax1.set_title('Delta between messages ')

ax2.plot(df["Latency"] , label="Latency[ms]")
ax2.plot([ df["Latency"].mean()] *len(df["Latency"] ),"-", label="Average")
ax2.set_title('Latency from data generation and reception')

ax1.legend()
ax2.legend()

# df.plot(kind='line' ,y=["Delta", "Latency"], subplots = True, ax=ax1)

fig2, (bx1,bx2) = plt.subplots(2)
bx1.hist(df["Delta"] ) #, label=signals[i].name, '*')
bx2.hist(df["Latency"]) #, label=signals[i].name, '*')

fig3, (cx1,cx2) = plt.subplots(2)
cx1.hist(df["Normalized_delta"] ,bins=10 ) #, label=signals[i].name, '*')
cx2.hist(df["Normalized_latency"],bins=10) #, label=signals[i].name, '*')


plt.show()






