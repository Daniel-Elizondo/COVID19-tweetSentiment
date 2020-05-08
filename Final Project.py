import COVID19Py
import csv
from datetime import datetime
import matplotlib.dates as mdates
from textblob import TextBlob
import matplotlib.pyplot as plt

tweetBody = []
tweetDateTime = []
tweetDate = []
tweetSentiment = []

# get tweet's body and datetime from CSV file
with open('TrumpTweets.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            tweetBody.append(row[1])
            tweetDateTime.append(row[2])
            line_count += 1

# take out the time and just keep the date
for i in tweetDateTime:
    temp = i.split(" ")
    tweetDate.append(temp[0])

# calculate the sentiment of each tweet
for i in tweetBody:
    blob = TextBlob(i)
    sentiment = blob.sentiment.polarity
    tweetSentiment.append(sentiment)

# big chunk of code to get the average sentiment of the the tweets posted that day
dateSentimentCount = {}
dateSentimentTotal = {}
count = 0
for i in tweetDate:
    if i not in dateSentimentCount:
        dateSentimentCount[i] = tweetDate.count(i)
    if i not in dateSentimentTotal:
        dateSentimentTotal[i] = 0
    dateSentimentTotal[i] = dateSentimentTotal[i] + tweetSentiment[count]
    count += 1

uniqueDates = []
for i in tweetDate:
    if i not in uniqueDates:
        uniqueDates.append(i)

avgSentiment = []
for i in range(len(dateSentimentCount)):
    avgSentiment.append(dateSentimentTotal[uniqueDates[i]]/dateSentimentCount[uniqueDates[i]])

avgdic = {}
count = 0
for i in uniqueDates:
    avgdic[i] = avgSentiment[count]
    count += 1
# big chunk ends

# getting and formatting COVID-19 infaction data in the US
covid19 = COVID19Py.COVID19(data_source="jhu")
usData = covid19.getLocationByCountryCode("US",1)
rawTimeline = str(usData)[str(usData).index("timeline",str(usData).index("timeline") + 1) + 12:str(usData).index("deaths", str(usData).index("deaths") + 1) - 5]
spliTimeline = rawTimeline.split(", ")

# even more formatting for COVID-19 data
coronaDates = []
coronaInfections = []
for i in spliTimeline:
    coronaDates.append(i[6:11] + "-" + i[1:5])
    coronaInfections.append(int(i[24:]))

# sync the dates between the tweets and the COVID-19 data
syncedSentiment = []
count = 0
for i in coronaDates:
    if i not in uniqueDates:
        syncedSentiment.append(None)
    else:
        syncedSentiment.append(avgSentiment[count])
        count += 1

# plot the data
xVals = [datetime.strptime(d,"%m-%d-%Y").date() for d in coronaDates]
yVals1 = syncedSentiment

ax = plt.gca()

locator = mdates.DayLocator()
ax.xaxis.set_major_locator(locator)
plt.scatter(xVals, yVals1)

plt2 = plt.twinx()

plt2.plot(xVals, coronaInfections)
plt.gcf().autofmt_xdate()
plt.show()