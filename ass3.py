#! /usr/bin/python3
#Brent Barrese - Assignment 3

import re   #reg expression operations
import sys  #sys module for list, argv

def printDict(dict):
    i = 0
    #sort keys in dict
    for key in sorted(dict.keys()):
        #sort values in dict
        dict[key] = sorted(dict[key])
        print(i, '\t', key, '\t', len(list(filter(None, dict[key]))), '\t', dict[key])
        i += 1

def buildDicts(file):
    #define regex patterns
    pattern = re.compile(".*evaluated: ([0-9a-fA-F]+).*\\[(.*)\\]")
    cookieKeyDict = {}
    segmentKeyDict = {}
    with open(file) as f:
        for line in f:
           match = pattern.match(line)
           if match:
               foundCookie = match.group(1)
               segments = match.group(2).split(", ")
               cookieKeyDict[foundCookie] = set()
               for segment in segments:
                   cookieKeyDict[foundCookie].add(segment)
               for segment in segments:
                   if segment:
                        if segment not in segmentKeyDict:
                            segmentKeyDict[segment] = set()
                        segmentKeyDict[segment].add(foundCookie)

    return cookieKeyDict, segmentKeyDict

def numEmptyCookies(dict):
    total = 0
    for key in dict.keys():
        if (len(list(filter(None, dict[key]))) == 0):
            total += 1
    return total

def numNonEmptyCookies(dict):
    return sum(value != '' for value in dict.values())

def numNonEmptyCookiesLogExclusive(dict1, dict2):
    total = 0
    for key in dict1:
        if key not in dict2:
            #Confirmed if only in 1 dict, now check if non-empty
            if (value != [] for value in dict1.values()):
                total += 1
    return total

def numNonEmptyCookiesBoth(dict1, dict2):
    total = 0
    for key in dict1:
        if (value != [] for value in dict1.values()):
            if key in dict2:
                if (value != [] for value in dict2.values()):
                    total += 1
    return total

def gainedExtraCookies(baselineDict, testRunDict):
    numMismatches = 0
    population = len(testRunDict)    
    extraCookiesDict = {}
    for key in testRunDict:
        if key in baselineDict:
            baselineSet = set(baselineDict.get(key))
            testrunSet = set(testRunDict.get(key))
            difference = set()
            difference = testrunSet - baselineSet
            isEmpty = (len(difference) == 0)
            if isEmpty == False:
                extraCookiesDict[key] = (difference)
        else:
            #not in baseline, so extra
            extraCookiesDict[key] = testRunDict[key]
    
    numMismatches = len(extraCookiesDict)
    print("\nSegments that gained extra cookies: " , numMismatches,'/',population)
    printDict(extraCookiesDict)

def lostCookies(baselineDict, testRunDict):
    numMismatches = 0
    population = len(testRunDict)
    lostCookiesDict = {}
    for key in baselineDict:
        if key in testRunDict:
            baselineSet = set(baselineDict.get(key))
            testrunSet = set(testRunDict.get(key))
            difference = set()
            difference = baselineSet - testrunSet
            isEmpty = (len(difference) == 0)
            if isEmpty == False:
                lostCookiesDict[key] = difference
        #else segment is not in test run dict, which means it lost a cookie
        else:
            lostCookiesDict[key] = baselineDict[key]
    
    numMismatches = len(lostCookiesDict)
    print("\nSegments that lost cookies: ", numMismatches, '/', population)
    printDict(lostCookiesDict)

def extraSegments(baselineDict, testRunDict):
    numMismatches = 0
    population = len(testRunDict)
    extraSegmentsDict = {}
    for key in testRunDict:
        if key in baselineDict:
            #form a set to find the difference
            baselineSet = set(baselineDict.get(key))
            testRunSet = set(testRunDict.get(key))
            difference = set()
            difference = testRunSet - baselineSet
            isEmpty = (len(difference) == 0)
            if isEmpty == False:
                if (len(list(filter(None, testRunDict[key])))):
                    extraSegmentsDict[key] = difference
        else:
            #key was not in baseline, so it is extra in test
            extraSegmentsDict[key] = testRunDict[key]
    
    numMismatches = len(extraSegmentsDict)
    print("\nCookies assigned to extra segments: ", numMismatches, '/',population)
    printDict(extraSegmentsDict)

def omittedSegments(baselineDict, testRunDict):
    numMismatches = 0
    population = len(testRunDict)
    omittedSegmentsDict = {}
    for key in baselineDict:
        if key in testRunDict:
            #form a set to find the difference
            baselineSet = set(baselineDict.get(key))
            testRunSet = set(testRunDict.get(key))
            difference = set()
            difference = baselineSet - testRunSet
            isEmpty = (len(difference) == 0)
            if isEmpty == False:
                if difference != 0:
                    omittedSegmentsDict[key] = difference
        #else segment is not in the test run dict, which means it was lost
        else:
            omittedSegmentsDict[key] = baselineDict[key]

    numMismatches = len(omittedSegmentsDict)
    print("\nCookies omitted from segments: ", numMismatches, '/', population)
    printDict(omittedSegmentsDict)

def main():
    baselineCookieDict, baselineSegmentDict = buildDicts(sys.argv[1])
    testRunCookieDict, testRunSegmentDict = buildDicts(sys.argv[2])

    #Print summary statements
    print ("Summary:")
    print ("Total Cookies in Baseline =  " , len(baselineCookieDict))
    print ("Empty cookies in baseline  = " , numEmptyCookies(baselineCookieDict))
    nonEmptyBaseline = numNonEmptyCookies(baselineCookieDict)
    print ("Non-empty cookies in baseline =" , nonEmptyBaseline)
    print ("total cookies in test =" , len(testRunCookieDict))
    print ("empty cookies in test =" , numEmptyCookies(testRunCookieDict))
    print ("non-empty cookies in test =" , numNonEmptyCookies(testRunCookieDict))
    print ("non-empty cookies in baseline only = ", numNonEmptyCookiesLogExclusive(baselineCookieDict, testRunCookieDict))
    nonEmptyTestOnly = numNonEmptyCookiesLogExclusive(testRunCookieDict, baselineCookieDict)
    print ("non-empty cookies in test only = ", nonEmptyTestOnly)
    print ("non-empty cookies in both =" , numNonEmptyCookiesBoth(baselineCookieDict, testRunCookieDict))
    print ("non-empty cookies in either =", nonEmptyBaseline + nonEmptyTestOnly)

    gainedExtraCookies(baselineSegmentDict, testRunSegmentDict)
    lostCookies(baselineSegmentDict, testRunSegmentDict)
    extraSegments(baselineCookieDict, testRunCookieDict)
    omittedSegments(baselineCookieDict, testRunCookieDict)

if __name__ == "__main__":
    main()