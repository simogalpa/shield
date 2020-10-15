import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import statistics as stat
from sklearn import preprocessing
import numpy as np




df = pd.read_csv("Stress_test_5.csv")

print(type(df))

print("Dataset dimensions" ,df.shape)

print(" \n \n-------------------- \n\n Dataset head \n-------------------- \n\n\n")
print(df.head())
print(" \n \n-------------------- \n\n  Dataset info \n-------------------- \n\n \n")
df.info()

print(" \n \n-------------------- \n\n  Dataset basic stat \n-------------------- \n\n \n")

#df = df[150:]
print(df.describe())

def normalize(dataset):
    return( (dataset - dataset.min())/(dataset.max() -dataset.min()))


def normalize_array(array):
    return( (array - min(array))/(max(array) -min(array)))

def zero_to_nan(values):
    """Replace every 0 with 'nan' and return a copy."""
    return [float('nan') if x==0.0 else x for x in values]

starting_topic = -1
df["New_topic"] = [0]* len(df["Num_of_topics"])
df["Delta_ma"] = [df["Delta"].mean()] *len(df["Delta"])
df["Latency_ma"] = [df["Latency"].mean()] *len(df["Latency"])



for i, data in enumerate(df["Num_of_topics"]):
    if starting_topic != data:
        df["New_topic"][i] = 1
        starting_topic = data
        #print("Topic_addition")

mean = df["Delta"].mean()
sigma = df["Delta"].std()

splitted_dataframes = list()


for  i, dato in enumerate(df["Delta"]):
    #print(dato)
    #print((mean + 3* sigma))
    if dato > (mean + 2* sigma):
        #print(i)
        df["Delta"][i] = df["Delta"][i-1]
#print( df["Timestamp"][0])

###-----
ma_parameter = 20
for i in range (len(df["Delta"])):
    if i > ma_parameter:
        sum = 0
        asum = 0
        for k in range(ma_parameter):
            kk = ma_parameter -k
            #print(kk)
            sum += df["Delta"][i-kk]*(ma_parameter-kk)
            asum += (ma_parameter-kk)
            #print(sum, asum)
        df["Delta_ma"][i] = sum/asum 

###-------
for i in range (len(df["Latency"])):
    if i > ma_parameter:
        sum = 0
        asum = 0
        for k in range(ma_parameter):
            kk = ma_parameter -k
            #print(kk)
            sum += df["Latency"][i-kk]*(ma_parameter-kk)
            asum += (ma_parameter-kk)
            #print(sum, asum)
        df["Latency_ma"][i] = sum/asum 


### ------
df["Delta_ma_ana"] = [0]* len(df["Delta"])
df["Latency_ma_ana"]= [0]* len(df["Latency"])

for i , data  in enumerate(df["Delta"]):
    if data > df["Delta"].mean() + 3* df["Delta"].std():
        df["Delta_ma_ana"][i] = 1
        #print("Error, violating Delta contraints with {} topics".format(df["Num_of_topics"][i]))

for i , data  in enumerate(df["Latency"]):
    if data > df["Latency"].mean() + 3* df["Latency"].std():
        df["Latency_ma_ana"][i] = 1
        #print("Error, violating Latency contraints with {} topics".format(df["Num_of_topics"][i]))


###----

last_value = -1
for i , value in enumerate(df["New_topic"]):
    if value == 1:
        if last_value > 0:
            splitted_dataframes.append(df[last_value: i ])
        last_value = i+1

delta_mean_over_topics = list()
delta_std_over_topics = list()
latency_mean_over_topics = list()
latency_std_over_topics = list()


#print(len(splitted_dataframes))
for dataframe in splitted_dataframes:
    
    delta_mean_over_topics.append(dataframe["Delta"].mean())
    delta_std_over_topics.append(dataframe["Delta"].std())
    latency_mean_over_topics.append(dataframe["Latency"].mean())
    latency_std_over_topics.append(dataframe["Latency"].std())



#print(delta_mean_over_topics)
fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('')
df["Timestamp"] = list(range(0, len(df["Delta"] )))

df["Normalized_delta"] = normalize(df["Delta"])
df["Normalized_latency"] = normalize(df["Latency"] )

#ASSE 1

ax1.plot(df["Delta"] , label="Delta")
#ax1.plot([ df["Delta"].mean()] *len(df["Delta"] ) ,"-", label="Average")
ax1.plot(df["Delta_ma"],"-", label="Average")
#ax1.plot(zero_to_nan(df["Delta_ma_ana"]),"*",color="red", label="Performaces drop")
ax1.set_ylabel('Seconds')
ax1.set_xlabel('Message n°')
ax1.grid(True)
ax1.legend()
ax1.set_title('Delta between messages ')

#ASSE 2

ax2.plot(df["Latency"] , label="Latency")
ax2.plot(df["Latency_ma"] ,"-", label="Average")
#ax2.plot(zero_to_nan(df["Latency_ma_ana"]*10),'*',color="red", label="Performaces drop")
#ax2.plot( df["New_topic"],"-")
ax2.set_ylabel('Seconds')
ax2.set_xlabel('Message n°')
ax2.grid(True)
ax2.legend()
ax2.set_title('Latency from data generation and reception')





# df.plot(kind='line' ,y=["Delta", "Latency"], subplots = True, ax=ax1)
"""
fig2, (bx1,bx2) = plt.subplots(2)
bx1.hist(df["Delta"] ) #, label=signals[i].name, '*')
bx2.hist(df["Latency"]) #, label=signals[i].name, '*')

fig3, (cx1,cx2) = plt.subplots(2)
cx1.hist(df["Normalized_delta"] ,bins=10 ) #, label=signals[i].name, '*')
cx2.hist(df["Normalized_latency"],bins=10) #, label=signals[i].name, '*')
"""
fig4, (dx1,dx2) = plt.subplots(2)

dx1.plot(normalize_array(delta_mean_over_topics) , label = "Delta [Norm]")
dx1.plot(normalize_array(latency_mean_over_topics), label = "Latency [Norm]" ) #, label=signals[i].name, '*') ,
#dx1.plot(delta_mean_over_topics , label = "Delta")
#dx1.plot(latency_mean_over_topics, label = "Latency") #, label=signals[i].name, '*') ,
dx1.set_title("Mean value of parameters over number of topics" , )
dx1.set_ylabel('Seconds')
dx1.set_xlabel('Number of topics')
dx1.grid(True)
dx1.legend()

dx2.plot(normalize_array(delta_std_over_topics), label = "Delta")
dx2.plot(normalize_array(latency_std_over_topics), label = "Latency") #, label=signals[i].name, '*') ,
dx2.set_title("Standard deviation of parameters over number of topics")

#dx2.set_ylabel()
dx2.set_xlabel('Number of topics')
dx2.grid(True)
dx2.legend()

#dx1.hist(latency_mean_over_topics ,bins=10 ) #, label=signals[i].name, '*') 
#dx2.hist(df["Normalized_latency"],bins=10) #, label=signals[i].name, '*')


plt.show()






