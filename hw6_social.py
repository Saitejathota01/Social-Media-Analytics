"""
Social Media Analytics Project
Name:
Roll Number:
"""

from ipaddress import collapse_addresses
import numbers
from tabnanny import check
from urllib.parse import _SplitResultBase
from xml.sax.handler import feature_external_ges
import hw6_social_tests as test

project = "Social" # don't edit this

### PART 1 ###

import pandas as pd
import nltk
nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
endChars = [ " ", "\n", "#", ".", ",", "?", "!", ":", ";", ")" ]

'''
makeDataFrame(filename)
#3 [Check6-1]
Parameters: str
Returns: dataframe
'''
def makeDataFrame(filename):
    dataframe=pd.read_csv(filename)
    return dataframe


'''
parseName(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseName(fromString):
    for line in fromString.split("\n"):
        a=line.find(":") 
        line=line[a+1:] 
        b=line.find("(") 
        line=line[:b]
        line=line.strip()
    return line


'''
parsePosition(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parsePosition(fromString):
    for line in fromString.split("\n"):
        a=line.find("(") 
        line=line[a+1:] 
        b=line.find("from") 
        line=line[:b]
        line=line.strip()
    return line
    


'''
parseState(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseState(fromString):
    for line in fromString.split("\n"):
        a=line.find("from ") + len("from")
        line=line[a:]
        b=line.find(")")
        line=line[:b]
        line=line.strip()
    return line


'''
findHashtags(message)
#5 [Check6-1]
Parameters: str
Returns: list of strs
'''
def findHashtags(message):
    new=message.split("#")
    r=""
    list=[]
    for i in new[1:]:
        for j in i:
            # print(j)
            if j not in endChars:
                r+=j
            else:
                break
        list.append('#'+r)
        r=""
    return list   


'''
getRegionFromState(stateDf, state)
#6 [Check6-1]
Parameters: dataframe ; str
Returns: str
'''
def getRegionFromState(stateDf, state):
    a=stateDf.loc[stateDf['state']==state,'region']
    return a.values[0]


'''
addColumns(data, stateDf)
#7 [Check6-1]
Parameters: dataframe ; dataframe
Returns: None
'''
def addColumns(data, stateDf):
    names=[]
    position=[]
    hashtags=[]
    state=[]
    region=[]
    for i,j in data.iterrows():
        names.append(parseName(j["label"]))
        position.append(parsePosition(j["label"]))
        state.append(parseState(j["label"]))
        region.append(getRegionFromState(stateDf,parseState(j["label"])))
        hashtags.append(findHashtags(j["text"]))
    data['name']=names
    data['position']=position
    data['hashtags']=hashtags
    data['state']=state    
    data['region']=region
    return None


### PART 2 ###

'''
findSentiment(classifier, message)
#1 [Check6-2]
Parameters: SentimentIntensityAnalyzer ; str
Returns: str
'''
def findSentiment(classifier, message):
    score = classifier.polarity_scores(message)['compound']
    if score<-0.1:
        return "negative"
    if score>0.1:
        return "positive" 
    return "neutral"


'''
addSentimentColumn(data)
#2 [Check6-2]
Parameters: dataframe
Returns: None
'''
def addSentimentColumn(data):
    classifier = SentimentIntensityAnalyzer()
    list=[]
    for i,j in data.iterrows():
        list.append(findSentiment(classifier,j['text']))
    data['sentiment']=list
    return None


'''
getDataCountByState(data, colName, dataToCount)
#3 [Check6-2]
Parameters: dataframe ; str ; str
Returns: dict mapping strs to ints
'''
def getDataCountByState(data, colName, dataToCount):
    dict1={}
    if len(colName)!=0 and len(dataToCount)!=0:
        for i,j in data.iterrows():
            if j[colName]==dataToCount:
                if j["state"]not in dict1:
                    dict1[j["state"]]=0
                dict1[j["state"]]+=1
    if len(colName)==0 or len(dataToCount)==0:
        for i,j in data.iterrows():
            if j["state"] not in dict1:
                dict1[j["state"]]=0
            dict1[j["state"]]+=1             
    return dict1


'''
getDataForRegion(data, colName)
#4 [Check6-2]
Parameters: dataframe ; str
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def getDataForRegion(data, colName):
    dictionary={}
    for i,j in data.iterrows():
        key=j["region"]
        if key not in dictionary:
            dictionary[key]={}
        if j[colName] not in dictionary[key]:
            dictionary[key][j[colName]]=1
        else:
            dictionary[key][j[colName]]+=1
    return dictionary


'''
getHashtagRates(data)
#5 [Check6-2]
Parameters: dataframe
Returns: dict mapping strs to ints
'''
def getHashtagRates(data):
    dictionary={}
    for a in data["hashtags"]:
        for i in a:
            if len(i)!=0 and i not in dictionary:
                dictionary[i]=1
            else:
                dictionary[i]+=1
    return dictionary
    


'''
mostCommonHashtags(hashtags, count)
#6 [Check6-2]
Parameters: dict mapping strs to ints ; int
Returns: dict mapping strs to ints
'''
def mostCommonHashtags(hashtags, count):
    res=dict(sorted(hashtags.items(), key=lambda x: x[1], reverse=True))
    out=dict([(a,b) for (a,b) in res.items()] [:count])
    return out
    


'''
getHashtagSentiment(data, hashtag)
#7 [Check6-2]
Parameters: dataframe ; str
Returns: float
'''
def getHashtagSentiment(data, hashtag):
    check=0
    count=0
    for a,b in data.iterrows():
        if hashtag in findHashtags(b["text"]):
            if b["sentiment"] =="positive":
                count+=1
            elif b["sentiment"] =="negative":
                count-=1
            elif b["sentiment"] =="neutral":
                count+=0
            check+=1
    return count/check
    


### PART 3 ###

'''
graphStateCounts(stateCounts, title)
#2 [Hw6]
Parameters: dict mapping strs to ints ; str
Returns: None
'''
def graphStateCounts(stateCounts, title):
    #print(stateCounts)
    import matplotlib.pyplot as plt
    state=[a for a in stateCounts.keys()]
    number=[b for b in stateCounts.values()]
    plt.bar(state, number, width=0.6)
    plt.xticks(ticks=list(range(len(state))), labels=state, rotation="vertical")
    plt.xlabel("States")
    plt.ylabel("Values of states")
    plt.title(title)
    plt.show()
    return


'''
graphTopNStates(stateCounts, stateFeatureCounts, n, title)
#3 [Hw6]
Parameters: dict mapping strs to ints ; dict mapping strs to ints ; int ; str
Returns: None
'''
def graphTopNStates(stateCounts, stateFeatureCounts, n, title):
    dictionary={}
    for a,b in stateFeatureCounts.items():
        for i,j in stateCounts.items():
            if i==a:
                dictionary[i]=b/j
    new=mostCommonHashtags(dictionary, n)
    graphStateCounts(new,title)
    return


'''
graphRegionComparison(regionDicts, title)
#4 [Hw6]
Parameters: dict mapping strs to (dicts mapping strs to ints) ; str
Returns: None
'''
def graphRegionComparison(regionDicts, title):
    feature=[]
    region=[]
    regionfeatures=[]
    for a in regionDicts:
        for b in regionDicts[a]:
            if b not in feature:
                feature.append(b)
        region.append(a)
    for a in regionDicts:
        temp=[]
        for b in feature:
            if b not in regionDicts[a]:
                temp.append(0)
            else:
                temp.append(regionDicts[a][b])
        regionfeatures.append(temp)
    sideBySideBarPlots(feature, region, regionfeatures, title)
    return


'''
graphHashtagSentimentByFrequency(data)
#4 [Hw6]
Parameters: dataframe
Returns: None
'''
def graphHashtagSentimentByFrequency(data):
    
    return


#### PART 3 PROVIDED CODE ####
"""
Expects 3 lists - one of x labels, one of data labels, and one of data values - and a title.
You can use it to graph any number of datasets side-by-side to compare and contrast.
"""
def sideBySideBarPlots(xLabels, labelList, valueLists, title):
    import matplotlib.pyplot as plt

    w = 0.8 / len(labelList)  # the width of the bars
    xPositions = []
    for dataset in range(len(labelList)):
        xValues = []
        for i in range(len(xLabels)):
            xValues.append(i - 0.4 + w * (dataset + 0.5))
        xPositions.append(xValues)

    for index in range(len(valueLists)):
        plt.bar(xPositions[index], valueLists[index], width=w, label=labelList[index])

    plt.xticks(ticks=list(range(len(xLabels))), labels=xLabels, rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Expects that the y axis will be from -1 to 1. If you want a different y axis, change plt.ylim
"""
def scatterPlot(xValues, yValues, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xValues, yValues)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xValues[i], yValues[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.ylim(-1, 1)

    # a bit of advanced code to draw a line on y=0
    ax.plot([0, 1], [0.5, 0.5], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    #print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    #test.week1Tests()
    #print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    #test.runWeek1()
    # test.testMakeDataFrame()
    # test.testParseName()
    # test.testParsePosition()
    # test.testParseState()
    # test.testFindHashtags()
    # test.testGetRegionFromState()
    # test.testAddColumns()
    # test.testFindSentiment()
    # test.testAddSentimentColumn()
   



    ## Uncomment these for Week 2 ##
    """print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()
    print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    test.runWeek2()"""
    df = makeDataFrame("data/politicaldata.csv")
    stateDf = makeDataFrame("data/statemappings.csv")
    addColumns(df, stateDf)
    addSentimentColumn(df)
    # test.testGetDataCountByState(df)
    # test.testGetDataForRegion(df)
    # test.testGetDataForRegion(df)
    # test.testGetHashtagRates(df)
    # test.testMostCommonHashtags(df)
    # test.testGetHashtagSentiment(df)

    

    ## Uncomment these for Week 3 ##
    """print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()"""
    test.runWeek3()
