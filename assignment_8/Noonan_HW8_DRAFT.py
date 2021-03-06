# Gillian Noonan - Homework 8

# %%
# Import modules and define functions used in this code
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
import dataframe_image as dfi


def predictions(last_week):
    '''Function (predictions):
        This function sets a blank array with two zero values
        and then fills those values with streamflow
        predictions from the AR model for the one-week
        and two-week forecasts.

        Parameters
        ----------
        last_week: one value, int
                Input variable with one value representing
                last week's average stream flow
        Returns
        ------
        prediction : two values, int
                Outputs two values representing successive forecasts from AR
                model for one-week and two-week future time periods
        '''
    prediction = np.zeros(2)
    prediction[0] = model.intercept_ + model.coef_ * last_week
    prediction[1] = model.intercept_ + model.coef_ * prediction[0]
    return prediction


def weekly_min(month1, day_more, day_less):
    '''Function (weekly_min):
        This function pulls values out of the data_week_min dataframe which
        is aggregated by weekly minimum value.  It then pulls the
        minimum historical value from the weekly minimum values
        for the given month, day time period.

        Parameters
        ----------
        month1: int
                Input variable with one value representing
                first month of the time window
        day_more: int
                Input variable with one value representing
                first day of the time window
        day_less: int
                Input variable with one value representing
                first day of the time window
        Returns
        ------
        wk_min : dataframe
                Outputs a dataframe with only data for specified time period
                and prints the output minimum flow value
        '''
    wk_min = data_week_min[(data_week_min.index.month == month1)
                           & (data_week_min.index.day >= day_more)
                           & (data_week_min.index.day <= day_less)]

    print("")
    print("Plotted historical weekly minimum flows for ", month1, "-",
          day_more, "to", month1, "-", day_less)
    wk_min.reset_index().plot(x="datetime",
                              y="flow",
                              title="Historical Flow Weekly Minimums",
                              kind="scatter")
    plt.show()

    print("The overall historical weekly minimum flow for ",
          month1, "-", day_more, "to", month1, "-", day_less,
          " is", wk_min.flow.min(), "cfs")


print("successful import")


# Task 1 - Set data input and develop dataframe

# %%
# Set file name and path
filename = 'streamflow_week8.txt'
filepath = os.path.join('data', filename)

print("File path is:", os.getcwd())
print("File name is:", filepath)

# %%
# Read the data into a pandas dataframe
# Expand the dates to year, month, day.
# View format of dataframe data (print first 15 rows)
data = pd.read_table(filepath, sep='\t', skiprows=30,
                     names=['agency_cd', 'site_no',
                            'datetime', 'flow', 'code'],
                     parse_dates=['datetime']
                     )
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

print(data.head(15))

# %%
# Aggregate flow values to weekly
# View new flow_weekly dataframe format (print first 15 rows)
flow_weekly = data.resample("W", on='datetime').mean()

print(flow_weekly.head(15))


# Task 2 - Build the Autoregressive (AR) model

# %%
# Set up arrays for lagged timeseries (one shift)
# [adds columns to flow_weekly dataframe with shifted flow values]
# View new flow_weekly dataframe format (print first 15 rows)
flow_weekly['flow_tm1'] = flow_weekly['flow'].shift(1)


print(flow_weekly.head(15))

# %%
# Set training and test data periods
# [train period is September data only for 2017 - 2019]
# [test [period is using last 10 weeks data]
month1 = 9
year_trainmin = 2017
year_trainmax = 2019
train = flow_weekly[(flow_weekly["month"] == month1)
                    & (flow_weekly["year"] >= year_trainmin) &
                      (flow_weekly["year"] <= year_trainmax)][['month',
                                                               'flow',
                                                               'flow_tm1'
                                                               ]]
test = flow_weekly[1648:][['flow', 'flow_tm1']]

print("Training data")
print(train)
print("Testing data")
print(test)
print("Good luck with your model!")

# %%
# Fit a linear regression model using sklearn (using one shift)
# Print coefficient of determination, intercept and slope for model
x = train['flow_tm1'].values.reshape(-1, 1)
y = train['flow'].values
model = LinearRegression().fit(x, y)

print('coefficient of determination:', np.round(model.score(x, y), 2))
print('intercept:', np.round(model.intercept_, 2))
print('slope:', np.round(model.coef_, 2))

# %%
# Plot of training and testing data periods
# Save figure to working folder as PNG file
plt.style.use('ggplot')
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
fig, ax = plt.subplots()
ax.plot(train['flow'], '--k', label='training', linewidth=3)
ax.plot(test['flow'], '-r', label='testing')
ax.set(title="AR Model: Training and Testing Data", xlabel="Date (yyyy-mm)",
       ylabel="Weekly Avg Flow [cfs]",
       xlim=[datetime.date(2017, 1, 1),
             datetime.date(2021, 1, 1)])
ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True, ncol=2)

fig.savefig('Train-and-Test.png')


# Task 3 - Predict Model Response for Autoregressive (AR) model

# %%
# Predict the model response for a given flow value
# [passes the regressor as the argument and get the
# corresponding predicted response]
# Plot comparison of simulated and observed flows
# Save figure to working folder as PNG file
q_pred_train = model.predict(train['flow_tm1'].values.reshape(-1, 1))
q_pred_test = model.predict(test['flow_tm1'].values.reshape(-1, 1))

fig, ax = plt.subplots()
ax.plot(train['flow'], '-k', linewidth=2, label='observed')
ax.plot(train.index, q_pred_train, ':r', linewidth=3,
        label='simulated')
ax.set(title="Observed Flow vs. Simulated Flow",
       xlabel="Model Duration Period (yyyy-mm)",
       ylabel="Weekly Avg Flow [cfs]")
ax.legend(frameon=True, fancybox=True, shadow=True)

fig.savefig('Predict-vs-observed.png')

# %%
# Plot model fit for t vs t-1 flow
# Save figure to working folder as PNG file
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='o',
           color='mediumvioletred', label='observations')
ax.set(xlabel='flow t-1', ylabel='flow t', title="AR Model Fit")
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train),
        label='AR model', linewidth=3, color='black')
ax.text(50, 175, "x(t) = 0.7 * x(t-1) + 31.95", fontsize=10)
ax.text(50, 155, "r^2 = 0.76", fontsize=10)
ax.legend(frameon=True, fancybox=True, shadow=True)

fig.savefig('t-vs-(t-1).png')

# Task 4 - Predict Flow with Autoregressive (AR) model

# WEEKLY FORECAST
# ---------------------------

# AR Model
# %%
# Predict one-week and two-week flow values (AR model)
#  using last week's average flow value and the AR model
last_week_flow = np.mean(data.tail(7))['flow']
one_two_flow = np.round(predictions(last_week_flow), 1)

print("Using last week's average flow of", last_week_flow,
      "the one-week and two-week predicted flow values from\
      the AR model are [AR-1WK, AR-2WK]:", one_two_flow)

# Jill's Code forecast
# %%
# Look at historical minumums for one-week and two-week forecast periods
# Input dates to grab and print historical min for one-week forecast period
month = 10
day_more = 18
day_less = 24

hist_min = data[(data["month"] == month)
                & (data["day"] >= day_more) & (data["day"] <= day_less)]
print("The historical minimum flow for the week of", month, "-", day_more,
      "to", month, "-", day_less, " is",
      hist_min["flow"].min(), "cfs")

month = 10
day_more = 25
day_less = 31

hist_min = data[(data["month"] == month)
                & (data["day"] >= day_more) & (data["day"] <= day_less)]
print("The historical minimum flow for the week of", month, "-", day_more,
      "to", month, "-", day_less, " is",
      hist_min["flow"].min(), "cfs")

# %%
# # Look at tables of statistics for last 7 and 14 days
# Save tables of statistics as PNG files for markdown
data_weekly = data.tail(7)
data_two_wks = data.tail(14)

df1 = data_weekly[["flow"]].describe()
print("Last week's flow statistics")
print(df1)
dfi.export(df1, "Last7days-stats.png")

df2 = data_two_wks[["flow"]].describe()
print("Last two week's flow statistics")
print(df2)
dfi.export(df2, "Last14days-stats.png")

# %%
# Look at visual trend over last two weeks
# Save plot for markdown
fig, ax = plt.subplots()
ax.plot(data_two_wks.datetime, data_two_wks.flow)
ax.set(title="Two-week flow trend")
ax.set(xlabel='Date', ylabel='Daily Flow (cfs)')
plt.show()

fig.savefig('Two-week-Trend.png')

# %%
# Get one-week and two-week mean values

mean_1wk = round(np.mean(data_weekly)["flow"], 2)
print("The mean flow for the last 7 days is:", mean_1wk)

mean_2wk = round(np.mean(data_two_wks)["flow"], 2)
print("The mean flow for the last 14 days is:", mean_2wk)

# %%
# Get beginning and end flow values for one-week and two-week periods
print("One-week Beginning and End Flow Values")
first_val1 = data_weekly.flow.iloc[0]
last_val1 = data_weekly.flow.iloc[-1]
print(first_val1)
print(last_val1)

print("Two-week Beginning and End Flow Values")
first_val2 = data_two_wks.flow.iloc[0]
last_val2 = data_two_wks.flow.iloc[-1]
print(first_val2)
print(last_val2)

# %%
# Overall flow flucuation for last 7 and 14 days
# Calculate flucuation from start to end of last 7 days
perc_chng_total_1wk = ((last_val1 - first_val1)/first_val1)*100
print("Overall flow fluctuation in past 7 days was",
      round(perc_chng_total_1wk, 2), "percent.")

# Calculate flucuation from start to end of last 14 days
perc_chng_total_2wk = ((last_val2 - first_val2)/first_val2)*100
print("Overall flow fluctuation in past 14 days was",
      round(perc_chng_total_2wk, 2), "percent.")

# %%
# Trend-based prediction for one-week and two-week/
# forecast values (Jill's Code)
# Based on percent change total from above code block.  If trend is upward,
# forecast a percentage higher, if trend is downward, forecast a
# percentage lower
if perc_chng_total_1wk > 0:
    Jill_1wk = mean_1wk + (mean_1wk * (perc_chng_total_1wk/100))
    print("The one-week flow prediction using Jill's code"
          " [JILL-1WK] is", round(Jill_1wk, 1), "cfs")
else:
    Jill_1wk = mean_1wk - (mean_1wk * (perc_chng_total_1wk/100))
    print("The one-week flow prediction using Jill's code"
          " [JILL-1WK] is", round(Jill_1wk, 1), "cfs")

if perc_chng_total_2wk > 0:
    Jill_2wk = mean_2wk + (mean_2wk * (perc_chng_total_2wk/100))
    print("The two-week flow prediction using Jill's code"
          " [JILL-2WK] is", round(Jill_2wk, 1), "cfs")
else:
    Jill_2wk = mean_2wk - (mean_2wk * (perc_chng_total_2wk/100))
    print("The two-week flow prediction using Jill's code"
          " [JILL-2WK] is", round(Jill_2wk, 1), "cfs")

# LONGTERM FORECAST [Week 11-15] (historical minimums)
# ---------------------------
# %%
# Aggregate flow values to weekly MINIMUM
data_week_min = data.resample("W", on='datetime').min()
data_week_min = data_week_min.set_index("datetime")
data_week_min

# %%
# Plot historical weekly flows for each forecast week
# Use function 'weekly_min' to grab historical minimum flow
# Get overall minumum of these flows for all time
# Wk11 historical min
month1 = 11
day_more = 1
day_less = 7

weekly_min(month1, day_more, day_less)

# Wk12 historical min
month1 = 11
day_more = 8
day_less = 14

weekly_min(month1, day_more, day_less)

# Wk13 historical min
month1 = 11
day_more = 15
day_less = 21

weekly_min(month1, day_more, day_less)

# Wk14 historical min
month1 = 11
day_more = 22
day_less = 28

weekly_min(month1, day_more, day_less)

# Wk15 historical min (spans two months so does not use function)
month1 = 11
day1 = 29
month2 = 12
day2 = 5

week15_min = data_week_min[(data_week_min.index.month == month1)
                           & (data_week_min.index.day >= day1)
                           | (data_week_min.index.month == month2)
                           & (data_week_min.index.day <= day2)]

print("")
print("Plotted historical weekly minimum flows for ", month1, "-", day1,
      "to", month2, "-", day2)
week15_min.reset_index().plot(x="datetime",
                              y="flow",
                              title="Historical Flow Weekly Minimums",
                              kind="scatter")
plt.show()

print("The overall historical weekly minimum flow for ", month1, "-", day1,
      "to", month2, "-", day2, " is",
      week15_min.flow.min(), "cfs")

# Wk16 historical min
month1 = 12
day_more = 6
day_less = 12

weekly_min(month1, day_more, day_less)

# %%
