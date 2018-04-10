import os
import sys
import datetime

#simple little function to check if string is number
def isInt(s):
    try:
		value = int(s)
		if(value != 0):
			return True
    except ValueError:
        return False

#used to determine if a given line is text or not
def isText(line):
	try:
		int(line)
		return False
	except ValueError:
		try:
			int(line[0])
		except ValueError:
			return True
		except TypeError:
			return False

#takes an .srt time stamp and puts it into DateTime
def toDateTime(uncutTime):
	cut = uncutTime.split(',')
	micro = int(cut[1])*1000
	cut = cut[0].split(':')
	time = datetime.time(int(cut[0]), int(cut[1]), int(cut[2]), micro)
	dateTime = datetime.datetime.combine(datetime.date.today(), time)
	return dateTime

def toSrtTime(dateTime):
	toSrt = dateTime.strftime('%H:%M:%S,%f')[:-3]
	return toSrt


#takes difference between two DateTimes
def getSpan(start, end):
	difference = end - start
	return difference

#takes input -- <.srt filename> <first time of speech>
def main():
	startTimes = []
	endTimes = []
	subIndex = []
	subText = []
	spans = []
	gaps = []
	filename = sys.argv[1]
	try:
		enteredStart = toDateTime(sys.argv[2])
	except IndexError:
		print "Enter the time for first dialogue instance in .srt format."
		print "i.e. 2 minutes, 23 seconds, 4 milliseconds is 00:02:23,004"
		raise KeyboardInterrupt
	with open(filename) as subs:
		lines = subs.readlines()
		subs.close()
	flag = False
	for line in lines:
		if(flag):
			span = line.split(' --> ')
			startTimes.append(span[0])
			endTimes.append(span[1])
			flag = False
		if(isInt(line)):
			subIndex.append(line)
			flag = True
	body = ""
	for line in lines:
		if(isText(line)):
			body = body + line
		else:
			if(body != ""):
				subText.append(body)
			body = ""
	if( body != ""):
		subText.append(body)
	i = 0
	sortedStart = []
	sortedEnd = []
	for time in startTimes:
		sortedStart.append(toDateTime(time))
	for time in endTimes:
		sortedEnd.append(toDateTime(time))
	i = 0
	while i < len(sortedStart):
		spans.append(getSpan(sortedStart[i], sortedEnd[i]))
		i += 1
	i = 0
	while i < (len(sortedStart) - 1):
		gaps.append(getSpan(sortedStart[i], sortedStart[i+1]))
		i += 1
	newStartTimes = []
	newStartTimes.append(enteredStart)
	i = 0
	while i < len(gaps):
		newStartTimes.append((newStartTimes[i] + gaps[i]))
		i += 1
	newEndTimes = []
	i = 0
	while i < len(newStartTimes):
		newEndTimes.append((newStartTimes[i] + spans[i]))
		i += 1
	srtStart = []
	srtEnd = []
	i = 0
	while i < len(newStartTimes):
		srtStart.append(toSrtTime(newStartTimes[i]))
		srtEnd.append(toSrtTime(newEndTimes[i]))
		i += 1
	f = open("newSrt.srt", "w+")
	i = 0
	while i < len(subIndex):
		f.write(subIndex[i])
		f.write(srtStart[i]+" --> "+srtEnd[i]+"\n")
		f.write(subText[i])
		i += 1
	print("file written")




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'Interrupted'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
