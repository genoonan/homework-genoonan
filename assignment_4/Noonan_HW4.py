#Gillian Noonan - Homework 4

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week4.txt'
filepath = os.path.join('data', filename)
print(os.getcwd())
print(filepath)

# %%
# DON'T change this part -- this creates the lists you 
# should use for the rest of the assignment
# no need to worry about how this is being done now we will cover
# this in later sections. 
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )
# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)
# Make a numpy array of this data
flow_data = data[['year', 'month','day', 'flow']].to_numpy()
# Getting rid of the pandas dataframe since we wont be using it this week
del(data)



# Jill Question Answering Code
#%%
print(flow_data)

# %%
type(flow_data)

# %%
flow_data.dtype

# %%
flow_data.ndim

# %%
flow_data.shape

# %%
#Set Wk4 predication variable
Wk4_prediction = 55.6
print(Wk4_prediction)

# %%
# Count the number of values with flow > Wk4prediction and month ==9
flow_count_greater = np.sum((flow_data[:,3] > Wk4_prediction) & (flow_data[:,1]==9))
print(flow_count_greater) 
# Count the number of total values with month ==9
flow_count_Sep = np.sum((flow_data[:,1]==9))
print(flow_count_Sep) 
#calculate percentage
print((flow_count_greater / flow_count_Sep)*100)

#%%
#In or before 2000: 
# Count the number of values with flow > Wk4prediction and month ==9 and year <=2000
flow_count_greater_1989_2000 = np.sum((flow_data[:,3] > Wk4_prediction) & (flow_data[:,1]==9) & (flow_data[:,0]<=2000))
print(flow_count_greater_1989_2000)
# Count the number of total values with month ==9 and year <=2000
flow_count_Sep_1989_2000 = np.sum((flow_data[:,1]==9) & (flow_data[:,0]<=2000))
print(flow_count_Sep_1989_2000) 
#calculate percentage
print((flow_count_greater_1989_2000 / flow_count_Sep_1989_2000)*100)

#%%
#In or after 2010: 
# Count the number of values with flow > Wk4prediction and month ==9 and year >=2010
flow_count_greater_2010_2020 = np.sum((flow_data[:,3] > Wk4_prediction) & (flow_data[:,1]==9) & (flow_data[:,0]>=2010))
print(flow_count_greater_2010_2020)
# Count the number of total values with month ==9 and year >=2010
flow_count_Sep_2010_2020 = np.sum((flow_data[:,1]==9) & (flow_data[:,0]>=2010))
print(flow_count_Sep_2010_2020) 
#calculate percentage
print((flow_count_greater_2010_2020 / flow_count_Sep_2010_2020)*100)


#%%
# Calculate the average flow for 1st half of September
print(flow_data)
flow_mean_Sep_begin = np.mean(flow_data[(flow_data[:,1]==9) & (flow_data[:,2]<=15), 3])
print(flow_mean_Sep_begin)

#%%
# Calculate the average flow for 2nd half of September
flow_mean_Sep_begin = np.mean(flow_data[(flow_data[:,1]==9) & (flow_data[:,2]>15), 3])
print(flow_mean_Sep_begin)


#Histogram Plotting
# %%
# Make a histogram of data (All flow data)
# Use the linspace  funciton to create a set  of evenly spaced bins
mybins = np.linspace(0, 1000, num=15)
# another example using the max flow to set the upper limit for the bins
#mybins = np.linspace(0, np.max(flow_data[:,3]), num=15) 
#Plotting the histogram
plt.hist(flow_data[:,3], bins = mybins)
plt.title('Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#%%
# Attempt: Isolate just September (All years)
flow_data_Sep1 = flow_data[flow_data[:,1] ==9]
mybins = np.linspace(0, 2000, num=20)
plt.hist(flow_data_Sep1[:,3], bins = mybins)
plt.title('September Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#%%
# Attempt: Isolate just September for last 10 years only
flow_data_Sep2 = flow_data[(flow_data[:,1] ==9) & (flow_data[:,0]>2010)]
mybins = np.linspace(0, 1000, num=20)
plt.hist(flow_data_Sep2[:,3], bins = mybins)
plt.title('September Streamflow 2010-2020')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#%%
# Attempt: Isolate just September for last 2 years only
flow_data_Sep3 = flow_data[(flow_data[:,1] ==9) & (flow_data[:,0]>2018)]
mybins = np.linspace(0, 200, num=20)
plt.hist(flow_data_Sep3[:,3], bins = mybins)
plt.title('September Streamflow 2018-2020')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#%%
# Attempt: Isolate just September for last 10 years only and week of 9/20 - 9/26
flow_data_Sep19_26_2010_2020 = flow_data[(flow_data[:,1] ==9) & (flow_data[:,0]>2010) & (flow_data[:,2] >=20) & (flow_data[:,2]<=26 )]
mybins = np.linspace(0, 250, num=20)
#mybins = np.linspace(0, np.max(flow_data_Sep19_26), num=20) 
plt.hist(flow_data_Sep19_26_2010_2020[:,3], bins = mybins)
plt.title('September Streamflow 2010-2020, Week of Sep20-26')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#%%
# Attempt: Isolate just September for last 2 years only and week of 9/20 - 9/26
flow_data_Sep19_26_2018_2020 = flow_data[(flow_data[:,1] ==9) & (flow_data[:,0]>=2018) & (flow_data[:,2] >=20) & (flow_data[:,2]<=26 )]
mybins = np.linspace(0, 160, num=10)
#mybins = np.linspace(0, np.max(flow_data_Sep19_26), num=20) 
plt.hist(flow_data_Sep19_26_2018_2020[:,3], bins = mybins)
plt.title('September Streamflow 2018-2020, Week of Sep20-26')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#%%
# Attempt: Isolate just September for 2020
flow_data_Sep2020 = flow_data[(flow_data[:,1] ==9) & (flow_data[:,0]==2020)]
mybins = np.linspace(0, 80, num=10)
#mybins = np.linspace(0, np.max(flow_data_Sep19_26), num=20) 
plt.hist(flow_data_Sep2020[:,3], bins = mybins)
plt.title('September Streamflow 2020')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')


#%%
# Attempt: Isolate week2 forecast period: for last 2 years only 9/27 - 9/30 and 10/1 - 10/3
# THIS ONE DOESN'T RUN - think it's the 'or' but not sure what else to use

#LC testing out just  the first  half of your logicfirst
flow_data_Sep27_30_Oct1_3_2018_2020 = flow_data[(flow_data[:,0]>=2018) & 
                                                ((flow_data[:,1] ==9) & 
                                                (flow_data[:,2] >=27) & 
                                                (flow_data[:,2]<=30 ))]

# LC Now testing out the second part after the or
flow_data_Sep27_30_Oct1_3_2018_2020 = flow_data[(flow_data[:,0]>=2018) & 
                                                ((flow_data[:,1] ==10) & 
                                                (flow_data[:,2] >=1) & 
                                                (flow_data[:,2]<=3))] 

# Putting them together
flow_data_Sep27_30_Oct1_3_2018_2020 = flow_data[(flow_data[:,0]>=2018) & 
                                                ((flow_data[:,1] ==9) & 
                                                (flow_data[:,2] >=27) & 
                                                (flow_data[:,2]<=30 )) |
                                                ((flow_data[:,1] ==10) & 
                                                (flow_data[:,2] >=1) & 
                                                (flow_data[:,2]<=3))] 
mybins = np.linspace(0, 500, num=10)
plt.hist(flow_data_Sep27_30_Oct1_3_2018_2020[:,3], bins = mybins)
plt.title('September-October Streamflow 2018-2020, Week of Sep27-Oct3')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#%%
# Attempt: Isolate just October for last 10 years only and days 1-3
flow_data_begOct10yr = flow_data[(flow_data[:,1] ==10) & (flow_data[:,0]>=2010) & (flow_data[:,2] >=1) & (flow_data[:,2]<=3)]
mybins = np.linspace(0, 500, num=10)
#mybins = np.linspace(0, np.max(flow_data_Sep19_26), num=20) 
plt.hist(flow_data_begOct10yr[:,3], bins = mybins)
plt.title('October 1-3 Streamflow 2010-2020')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#%%
# Attempt: Isolate just October 2019
flow_data_Oct2019 = flow_data[(flow_data[:,1] ==10) & (flow_data[:,0]==2019)]
mybins = np.linspace(0, 150, num=10)
#mybins = np.linspace(0, np.max(flow_data_Sep19_26), num=20) 
plt.hist(flow_data_Oct2019[:,3], bins = mybins)
plt.title('October Streamflow 2019')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#Quantiles
#%%
#Quantiles and stats for September 2020
flow_quants_Sep2020 = np.quantile(flow_data_Sep2020[:,3], q=[0,0.25, 0.5, 0.75])
print(flow_quants_Sep2020)
print(np.min(flow_data_Sep2020[:,3]))
print(np.max(flow_data_Sep2020[:,3]))
print(np.mean(flow_data_Sep2020[:,3]))
print(np.median(flow_data_Sep2020[:,3]))

#%%
#Quantiles and stats for early October, historical last 10 years
flow_quants_begOct10yr = np.quantile(flow_data_begOct10yr[:,3], q=[0,0.25, 0.5, 0.75])
print(flow_quants_begOct10yr)
print(np.min(flow_data_begOct10yr[:,3]))
print(np.max(flow_data_begOct10yr[:,3]))
print(np.mean(flow_data_begOct10yr[:,3]))
print(np.median(flow_data_begOct10yr[:,3]))

#%%
#Quantiles and stats for October 2019
flow_quants_Oct2019 = np.quantile(flow_data_Oct2019[:,3], q=[0,0.25, 0.5, 0.75])
print(flow_quants_Oct2019)
print(np.min(flow_data_Oct2019[:,3]))
print(np.max(flow_data_Oct2019[:,3]))
print(np.mean(flow_data_Oct2019[:,3]))
print(np.median(flow_data_Oct2019[:,3]))

# %%
