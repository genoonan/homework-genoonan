#Gillian Noonan - Homework 5

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week5.txt'
filepath = os.path.join('data', filename)
print(os.getcwd())
print(filepath)

# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# %%
# Sorry no more helpers past here this week, you are on your own now :) 
# Hints - you will need the functions: describe, info, groupby, sort, head and tail.

# See what we've got going on in the dataframe "data"
data.head(3)

#%%
data.shape

# %%
#1) Provide a summary of the data frames properties.
data.shape

#%%
# What are the column names?
data.columns

#%%
# # What is its index?
data.index

#%%
# What data types do each of the columns have?
data.info()

#%%
#2) Provide a summary of the flow column including the min, mean, max, standard deviation and quartiles.
data[["flow"]].describe()

#%%
# #3) Provide the same information but on a monthly basis. (Note: you should be able to do this with one or two lines of code)
data.groupby("month")["flow"].describe()

#%%
#4)Provide a table with the 5 highest and 5 lowest flow values for the period of record. Include the date, month and flow values in your summary
data2 = data[['datetime', 'month', 'flow']]
data2

#%%
data2.sort_values(by="flow", ascending=False).head(5)

#%%
data2.sort_values(by="flow", ascending=False).tail(5)

#%%
#5)Find the highest and lowest flow values for every month of the year (i.e. you will find 12 maxes and 12 mins) and report back what year these occurred in
# THIS WORKS BUT IT'S CLUNKY AND LOOOOONG.  THERE HAS GOT TO BE A MORE EFFICIENT WAY TO DO THIS I'M SURE!!.....for now, it gives me the answers need though......
flow_by_month=data.groupby(["month"])[["flow"]].describe()
flow_by_month.columns=flow_by_month.columns.droplevel(0)
flow_by_month

#%%
data3= data[["year", "month", "flow"]]
data3

#PAINSTAKINGLY PULLING OUT YEARS 
#%%
x = 1
data_Jan = data3[data3["month"] == x]
print(data_Jan.sort_values(by = "flow", ascending = False).tail(1))
print(data_Jan.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 2
data_Feb = data3[data3["month"] == x]
print(data_Feb.sort_values(by = "flow", ascending = False).tail(1))
print(data_Feb.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 3
data_Mar = data3[data3["month"] == x]
print(data_Mar.sort_values(by = "flow", ascending = False).tail(1))
print(data_Mar.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 4
data_Apr = data3[data3["month"] == x]
print(data_Apr.sort_values(by = "flow", ascending = False).tail(1))
print(data_Apr.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 5
data_May = data3[data3["month"] == x]
print(data_May.sort_values(by = "flow", ascending = False).tail(1))
print(data_May.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 6
data_Jun = data3[data3["month"] == x]
print(data_Jun.sort_values(by = "flow", ascending = False).tail(1))
print(data_Jun.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 7
data_Jul = data3[data3["month"] == x]
print(data_Jul.sort_values(by = "flow", ascending = False).tail(1))
print(data_Jul.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 8
data_Aug = data3[data3["month"] == x]
print(data_Aug.sort_values(by = "flow", ascending = False).tail(1))
print(data_Aug.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 9
data_Sep = data3[data3["month"] == x]
print(data_Sep.sort_values(by = "flow", ascending = False).tail(1))
print(data_Sep.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 10
data_Oct = data3[data3["month"] == x]
print(data_Oct.sort_values(by = "flow", ascending = False).tail(1))
print(data_Oct.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 11
data_Nov = data3[data3["month"] == x]
print(data_Nov.sort_values(by = "flow", ascending = False).tail(1))
print(data_Nov.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 12
data_Dec = data3[data3["month"] == x]
print(data_Dec.sort_values(by = "flow", ascending = False).tail(1))
print(data_Dec.sort_values(by = "flow", ascending = False).head(1))
#%%
# Plot Max Monthly Flow
f, ax = plt.subplots()

ax.bar(flow_by_month.index,
        flow_by_month["max"],
        color="purple")

ax.set(title="Max Monthly Flow")
plt.show()

#%%
# Plot Min Monthly Flow
f, ax = plt.subplots()

ax.bar(flow_by_month.index,
        flow_by_month["min"],
        color="purple")

ax.set(title="Min Monthly Flow")
plt.show()

#%%
#6)Provide a list of historical dates with flows that are within 10% of your week 1 forecast value. If there are none than increase the %10 window until you have at least one other value and report the date and the new window you used
data2

#%%
# Get upper and lower range values
w1_value = 56.2
percent_var = 0.1

w1_value_ten_upper = w1_value + (w1_value*percent_var) 
print(w1_value_ten_upper)

w1_value_ten_lower = w1_value - (w1_value*percent_var) 
print(w1_value_ten_lower)

#%%
# NEEDS DEBUGGING - WORKS SEPARATELY, BUT NOT WITH & or and
# UPDATE - figured out the parentheses!! WORKS
data2[(data2["flow"] < w1_value_ten_upper) & (data["flow"] > w1_value_ten_lower)]
#%%
# Pieced out for an answer for now......
#upper = data2[data2["flow"]< w1_value_ten_upper]
#upper
#%%
#upper[upper["flow"] > w1_value_ten_lower]


# %%
#WEEKLY FORECAST WEEK 5
# 1week forecast
data_weekly = data.tail(7)
data_weekly

# %%
data_weekly_flow_sum = data_weekly["flow"].sum()
data_weekly_flow_sum

#%%
# Past Week Mean Flow
data_weekly_flow_mean = data_weekly_flow_sum/7
print("Average weekly flow for last 7 days was", data_weekly_flow_mean)

# or more succinct code:
#%%
data_weekly[["flow"]].describe()

# %%
flow_by_day=data_weekly.groupby(["day"])[["flow"]].head(7)
flow_by_day

#%%
# look at weekly trend
f, ax = plt.subplots()

ax.plot(data_weekly.day, data_weekly.flow)

ax.set(title="One week flow trend")
plt.show()


# 2week forecast
#AGAIN, THIS IS SOOOO CLUNKY.  HOW CAN I MAKE THIS MORE EFFICIENT - WITH CONDIDTIONALS MAYBE? CAN'T GET THEM TO WORK IN THE FILTER
# %%
#data_Oct = data[data["month"]==10]
# data_Oct

#%%
# data1_Oct_4_10 = data_Oct[data_Oct["day"]>=4]     
# data1_Oct_4_10 
# %%
# data2_Oct_4_10 = data1_Oct_4_10[data1_Oct_4_10["day"]<=10]
# data2_Oct_4_10
# %%
# Get historical stats for October 4-10
# data2_Oct_4_10[["flow"]].describe()

# %%
# TRYING TO UNCLUNK IT 
# UPDATE - SUCCESS!!
data_Oct_two_week = data[(data["month"]==10) & (data["day"] <=10) & (data["day"] >=4)]
data_Oct_two_week["flow"].describe()
# %%
