#!/usr/bin/env python
# coding: utf-8

# Note that the script runs only on python3!
# It works best when running from Anaconda Prompt as Anaconda has the pandas module installed 

# The folder structure used was: .../RandomPoints/#ofPoints/.csvFiles, e.g:
# .../RandomPoints/20/.csvFiles where .csvFiles represents the location where all the .csv files where stored
# Please note that two output folder are required in the parent folder of the datasets: "stats" and "mean_det", e.g.:
# .../RandomPoints/stats and .../RandomPoints/mean_det

import pandas as pd
import os


path = input('Where are the files located? (e.g. RandomPoints/20): ')
print('Computing...')
#os.fsencode() may produce problems, could possibly be resolved with os.path.fsencode()
directory = os.fsencode(path)
col_names =  ['1', '4', '7', '8', '9', '10', '11', '12', '13', '14', '17', '21']
g = []
number = []
count = 0

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"):
        filenameext = os.path.splitext(filename)[0]
        filepath = os.fsdecode(directory) + "/" + filename
        a = "df_" + filenameext 
        g.append(str(a))
        number.append(str(count))
        g[count] =pd.read_csv(filepath, sep=',')
        number[count] = pd.DataFrame(index=g[count].index, columns = col_names)
        count = count + 1

for n in range(len(g)):
    for i in range(len(g[n].values)):
            if g[n].values[i,2] == 1:
                number[n].at[i, '1'] = g[n].values[i,1]
            elif g[n].values[i,2] == 4:
                number[n].at[i, '4'] = g[n].values[i,1]    
            elif g[n].values[i,2] == 7:
                number[n].at[i, '7'] = g[n].values[i,1]
            elif g[n].values[i,2] == 8:
                number[n].at[i, '8'] = g[n].values[i,1]
            elif g[n].values[i,2] == 9:
                number[n].at[i, '9'] = g[n].values[i,1]
            elif g[n].values[i,2] == 10:
                number[n].at[i, '10'] = g[n].values[i,1]
            elif g[n].values[i,2] == 11:
                number[n].at[i, '11'] = g[n].values[i,1]
            elif g[n].values[i,2] == 12:
                number[n].at[i, '12'] = g[n].values[i,1]
            elif g[n].values[i,2] == 13:
                number[n].at[i, '13'] = g[n].values[i,1]
            elif g[n].values[i,2] == 14:
                number[n].at[i, '14'] = g[n].values[i,1]
            elif g[n].values[i,2] == 17:
                number[n].at[i, '17'] = g[n].values[i,1]
            elif g[n].values[i,2] == 21:
                number[n].at[i, '21'] = g[n].values[i,1]


mean = pd.DataFrame(columns = col_names)
for i in range(len(number)):
    mean.at[i, '1'] = number[i].loc[:,'1'].mean()
    mean.at[i, '4'] = number[i].loc[:,'4'].mean()
    mean.at[i, '7'] = number[i].loc[:,'7'].mean()
    mean.at[i, '8'] = number[i].loc[:,'8'].mean()
    mean.at[i, '9'] = number[i].loc[:,'9'].mean()
    mean.at[i, '10'] = number[i].loc[:,'10'].mean()
    mean.at[i, '11'] = number[i].loc[:,'11'].mean()
    mean.at[i, '12'] = number[i].loc[:,'12'].mean()
    mean.at[i, '13'] = number[i].loc[:,'13'].mean()
    mean.at[i, '14'] = number[i].loc[:,'14'].mean()
    mean.at[i, '17'] = number[i].loc[:,'17'].mean()
    mean.at[i, '21'] = number[i].loc[:,'21'].mean()
    mean.at[i,'MEAN'] = mean.fillna(0).iloc[i]['1'] * 0.034298702 + mean.fillna(0).iloc[i]['4'] * 0.046317022 +     mean.fillna(0).iloc[i]['7'] * 0.048348772 + mean.fillna(0).iloc[i]['8'] * 0.025861772 + mean.fillna(0).iloc[i]['9'] * 0.012190502 +     mean.fillna(0).iloc[i]['10'] * 0.190605737 + mean.fillna(0).iloc[i]['11'] * 0.058851889 + mean.fillna(0).iloc[i]['12'] * 0.346912772 +     mean.fillna(0).iloc[i]['13'] * 0.051895726 + mean.fillna(0).iloc[i]['14'] * 0.134508764 + mean.fillna(0).iloc[i]['17'] * 0.050208341
    mean.at[i,'MEAN_PERCENT'] =  (mean.fillna(0).iloc[i]['MEAN'] / 29.5) * 100


std = pd.DataFrame(columns = col_names)
for i in range(len(number)):
    std.at[i, '1'] = number[i].loc[:,'1'].std()
    std.at[i, '4'] = number[i].loc[:,'4'].std()
    std.at[i, '7'] = number[i].loc[:,'7'].std()
    std.at[i, '8'] = number[i].loc[:,'8'].std()
    std.at[i, '9'] = number[i].loc[:,'9'].std()
    std.at[i, '10'] = number[i].loc[:,'10'].std()
    std.at[i, '11'] = number[i].loc[:,'11'].std()
    std.at[i, '12'] = number[i].loc[:,'12'].std()
    std.at[i, '13'] = number[i].loc[:,'13'].std()
    std.at[i, '14'] = number[i].loc[:,'14'].std()
    std.at[i, '17'] = number[i].loc[:,'17'].std()
    std.at[i, '21'] = number[i].loc[:,'21'].std()

maxi = pd.DataFrame(columns = col_names)
for i in range(len(number)):
    maxi.at[i, '1'] = number[i].loc[:,'1'].max()
    maxi.at[i, '4'] = number[i].loc[:,'4'].max()
    maxi.at[i, '7'] = number[i].loc[:,'7'].max()
    maxi.at[i, '8'] = number[i].loc[:,'8'].max()
    maxi.at[i, '9'] = number[i].loc[:,'9'].max()
    maxi.at[i, '10'] = number[i].loc[:,'10'].max()
    maxi.at[i, '11'] = number[i].loc[:,'11'].max()
    maxi.at[i, '12'] = number[i].loc[:,'12'].max()
    maxi.at[i, '13'] = number[i].loc[:,'13'].max()
    maxi.at[i, '14'] = number[i].loc[:,'14'].max()
    maxi.at[i, '17'] = number[i].loc[:,'17'].max()
    maxi.at[i, '21'] = number[i].loc[:,'21'].max()

mini = pd.DataFrame(columns = col_names)
for i in range(len(number)):
    mini.at[i, '1'] = number[i].loc[:,'1'].min()
    mini.at[i, '4'] = number[i].loc[:,'4'].min()
    mini.at[i, '7'] = number[i].loc[:,'7'].min()
    mini.at[i, '8'] = number[i].loc[:,'8'].min()
    mini.at[i, '9'] = number[i].loc[:,'9'].min()
    mini.at[i, '10'] = number[i].loc[:,'10'].min()
    mini.at[i, '11'] = number[i].loc[:,'11'].min()
    mini.at[i, '12'] = number[i].loc[:,'12'].min()
    mini.at[i, '13'] = number[i].loc[:,'13'].min()
    mini.at[i, '14'] = number[i].loc[:,'14'].min()
    mini.at[i, '17'] = number[i].loc[:,'17'].min()
    mini.at[i, '21'] = number[i].loc[:,'21'].min()


col_names =  ['1', '4', '7', '8', '9', '10', '11', '12', '13', '14', '17', '21']
stats = pd.DataFrame(columns = col_names)
stats.at['Mean'] = 'NaN'
stats.at['Std'] = 'NaN'
stats.at['Min'] = 'NaN'
stats.at['Max'] = 'NaN'
stats.at['Fraction'] = 0
for i in range(len(number)):
    stats.at['Mean', '1'] = mean.loc[:,'1'].mean()
    stats.at['Mean', '4'] = mean.loc[:,'4'].mean()
    stats.at['Mean', '7'] = mean.loc[:,'7'].mean()
    stats.at['Mean', '8'] = mean.loc[:,'8'].mean()
    stats.at['Mean', '9'] = mean.loc[:,'9'].mean()
    stats.at['Mean', '10'] = mean.loc[:,'10'].mean()
    stats.at['Mean', '11'] = mean.loc[:,'11'].mean()
    stats.at['Mean', '12'] = mean.loc[:,'12'].mean()
    stats.at['Mean', '13'] = mean.loc[:,'13'].mean()
    stats.at['Mean', '14'] = mean.loc[:,'14'].mean()
    stats.at['Mean', '17'] = mean.loc[:,'17'].mean()
    stats.at['Mean', '21'] = mean.loc[:,'21'].mean()
    stats.at['Std', '1'] = std.loc[:,'1'].mean()
    stats.at['Std', '4'] = std.loc[:,'4'].mean()
    stats.at['Std', '7'] = std.loc[:,'7'].mean()
    stats.at['Std', '8'] = std.loc[:,'8'].mean()
    stats.at['Std', '9'] = std.loc[:,'9'].mean()
    stats.at['Std', '10'] = std.loc[:,'10'].mean()
    stats.at['Std', '11'] = std.loc[:,'11'].mean()
    stats.at['Std', '12'] = std.loc[:,'12'].mean()
    stats.at['Std', '13'] = std.loc[:,'13'].mean()
    stats.at['Std', '14'] = std.loc[:,'14'].mean()
    stats.at['Std', '17'] = std.loc[:,'17'].mean()
    stats.at['Std', '21'] = std.loc[:,'21'].mean()
    stats.at['Fraction', '1'] = 0.034298702 * stats.loc['Mean','1']
    stats.at['Fraction', '4'] = 0.046317022 * stats.loc['Mean','4']
    stats.at['Fraction', '7'] = 0.048348772 * stats.loc['Mean','7']
    stats.at['Fraction', '8'] = 0.025861772 * stats.loc['Mean','8']
    stats.at['Fraction', '9'] = 0.012190502 * stats.loc['Mean','9']
    stats.at['Fraction', '10'] = 0.190605737 * stats.loc['Mean','10']
    stats.at['Fraction', '11'] = 0.058851889 * stats.loc['Mean','11']
    stats.at['Fraction', '12'] = 0.346912772 * stats.loc['Mean','12']
    stats.at['Fraction', '13'] = 0.051895726 * stats.loc['Mean','13']
    stats.at['Fraction', '14'] = 0.134508764 * stats.loc['Mean','14']
    stats.at['Fraction', '17'] = 0.050208341 * stats.loc['Mean','17']
stats.at['Max', '1'] = maxi.loc[:,'1'].mean()
stats.at['Max', '4'] = maxi.loc[:,'4'].mean()
stats.at['Max', '7'] = maxi.loc[:,'7'].mean()
stats.at['Max', '8'] = maxi.loc[:,'8'].mean()
stats.at['Max', '9'] = maxi.loc[:,'9'].mean()
stats.at['Max', '10'] = maxi.loc[:,'10'].mean()
stats.at['Max', '11'] = maxi.loc[:,'11'].mean()
stats.at['Max', '12'] = maxi.loc[:,'12'].mean()
stats.at['Max', '13'] = maxi.loc[:,'13'].mean()
stats.at['Max', '14'] = maxi.loc[:,'14'].mean()
stats.at['Max', '17'] = maxi.loc[:,'17'].mean()
stats.at['Max', '21'] = maxi.loc[:,'21'].mean()
stats.at['Min', '1'] = mini.loc[:,'1'].mean()
stats.at['Min', '4'] = mini.loc[:,'4'].mean()
stats.at['Min', '7'] = mini.loc[:,'7'].mean()
stats.at['Min', '8'] = mini.loc[:,'8'].mean()
stats.at['Min', '9'] = mini.loc[:,'9'].mean()
stats.at['Min', '10'] = mini.loc[:,'10'].mean()
stats.at['Min', '11'] = mini.loc[:,'11'].mean()
stats.at['Min', '12'] = mini.loc[:,'12'].mean()
stats.at['Min', '13'] = mini.loc[:,'13'].mean()
stats.at['Min', '14'] = mini.loc[:,'14'].mean()
stats.at['Min', '17'] = mini.loc[:,'17'].mean()
stats.at['Min', '21'] = mini.loc[:,'21'].mean()


xsum = stats.sum(axis=1)
msum = xsum[4]
stddevmean =  mean.loc[:,'MEAN'].std()
meanmax = mean.loc[:,'MEAN'].max() 
meanmin = mean.loc[:,'MEAN'].min()
meanminperc = (meanmin/29.5)*100
meanmaxperc = (meanmax/29.5)*100


indexover = 0
indexunder = 0
for index, row in mean.iterrows():
    if mean.at[index,'MEAN_PERCENT'] > 110:
        indexover = indexover + 1
    elif mean.at[index,'MEAN_PERCENT'] < 90:
        indexunder = indexunder + 1

trueitems = ((len(g) - indexover - indexunder)/len(g))*100


print('Finished!')
#	pathstats = input('Where do you want to save the statistics file? (e.g. RandomPoints/20/): ')
filestats1 = input('Wheres the parent folder?')
numperp = input('How many points?')
filestats = 'stats_'
filemean = 'mean_d_'
stats.to_csv(str(filestats1) + '\\stats\\' +  str(filestats) + '_' + str(numperp) + '.csv')
with open(str(filestats1) + '\\stats\\' +  str(filestats) + '_' + str(numperp)  + '.txt', 'w') as f:
    f.write('The average landscape mean is: {namem}\nThe average standard deviation of the means is: {namest}\nThe maximum of the means is: {namemaxm}\nThe maximum of the means in percent is: {namemaxp}\nThe minimum of the means is: {namemmin}\nThe minimum of the means in percent is: {namemminp}\n{valueover} values are over 110%\n{valueunder} values are under 90%\n{valueright} values fall within +-10%'.format(namem=msum, namest=stddevmean, namemaxm=meanmax, namemaxp=meanmaxperc, namemmin=meanmin, namemminp=meanminperc, valueover=indexover, valueunder=indexunder, valueright=trueitems))
    f.close
mean.to_csv(str(filestats1) + '\\mean_det\\' +  str(filestats) + '_' + str(numperp)  + '.csv')

#The following section would ask for a little more user input
#It's currently disabled to allow for streamlined processing 

#statsyes = input('Do you want the summarized statistics? (Y/N): ')
#if statsyes == "Y" or statsyes == "y":
#	pathstats = input('Where do you want to save the statistics file? (e.g. RandomPoints/20/): ')
#	filestats = input('What would you like to call the file? (e.g. stats.csv): ')
#	stats.to_csv(str(pathstats) + '/' +  str(filestats) + '.csv')
#
#	with open(str(pathstats) + '/' +  str(filestats) + '.txt', 'w') as f:
#            f.write('The average landscape mean is: {namem}\nThe average standard deviation of the means is: {namest}\nThe maximum of the means is: {namemaxm}\nThe maximum of the means in percent is: {namemaxp}\nThe minimum of the means is: {namemmin}\nThe minimum of the means in percent is: {namemminp}\n{valueover} values are over 110%\n{valueunder} values are under 90%\n{valueright} values fall within +-10%'.format(namem=msum, namest=stddevmean, namemaxm=meanmax, namemaxp=meanmaxperc, namemmin=meanmin, namemminp=meanminperc, valueover=indexover, valueunder=indexunder, valueright=trueitems))
#            f.close
#elif statsyes != "N" or statsyes != "n":
#	statsyes2 = input('Please use Y or N, NOT yes or no): ')
#	if statsyes2 == "Y" or statsyes2 == "y":
#		pathstats2 = input('Where do you want to save the statistics file? (e.g. RandomPoints/20/): ')
#		filestats2 = input('What would you like to call the file? (e.g. stats.csv): ')
#		stats.to_csv(str(pathstats2) + '/' + str(filestats2)  + '.csv')
#		
#meanyes = input('Do you want the detailed information of the mean for all tries? (Y/N): ')
#if meanyes == "Y" or meanyes == "y":
#	pathmean = input('Where do you want to save the statistics file? (e.g. RandomPoints/20/): ')
#	filemean = input('What would you like to call the file? (e.g. mean.csv): ')
#	mean.to_csv(str(pathmean) + '/' + str(filemean)  + '.csv' )
#elif meanyes != "N" or meanyes != "n":
#	meanyes2 = input('Please use Y or N, NOT yes or no): ')
#	if meanyes2 == "Y" or meanyes2 == "y":
#		pathmean2 = input('Where do you want to save the statistics file? (e.g. RandomPoints/20/): ')
#		filemean2 = input('What would you like to call the file? (e.g. mean.csv): ')
#		mean.to_csv(str(pathmean2) + '/' + str(filemean2)  + '.csv')


