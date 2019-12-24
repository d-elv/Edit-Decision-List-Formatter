import os, csv, re, TechnicallySecondsToTimecode
from timecode import Timecode

def sixIndexSplitter(splitLine):
    splitLine = re.split(r'\s{2,}', splitter)
    dstIn = splitTimes[2]
    dstOut = splitTimes[3]
    dstOutSplit = dstOut.split("'")  # Separates timecode from '] at end
    dstOut = dstOutSplit[0]  # isolates timecode into dstOut variable
    dstIn = Timecode('25', dstIn)
    dstOut = Timecode('25', dstOut)
    srcDur = dstOut - dstIn
    del splitLine[0]
    splitLine.insert(0, num)
    del splitLine[-1]
    splitLine.append(str(srcDur))
    finalFileWriter.writerow(splitLine)

def mergeDict(a, b):
    a.update(b)
    return a


secondRow = ['Num', 'Reel', 'Tracks', 'Type', 'Src In', 'Src Out', 'Dst In', 'Dst Out', 'Src Dur']
thirdRow = ['Clip', 'Num', 'Earliest', 'Latest', 'Shortest', 'Longest', 'Total']
print('Drag in the folder containing the file(s) you want to convert. Single files will close the program.')
directoryToHack = input('Drag in the directory / file you wish to convert and hit enter: ')

acceptedFiletype = ['.edl']
ignoredFiles = []

for (root, paths, file) in os.walk(directoryToHack):
    for f in file:
        filePath = os.path.join(root + os.sep + f)
        name, ext = os.path.splitext(f)
        ext = ext.lower()
        lineElem = []
        result = []
        formattedLines = []
        outputDir = directoryToHack
        os.chdir(directoryToHack)
        dstIn = 0
        dstOut = 0
        srcDur = Timecode('25', '00:00:00:00')
        if not os.path.isfile(outputDir + name + '.csv'):
            if ext in acceptedFiletype:
                with open(root + os.sep + name + ext, 'r') as txtfile:
                    print(root + os.sep + name + ext)
                    fileLines = txtfile.readlines()
                    title = fileLines[0]
                for fileLine in fileLines: #Scrubs through the .edl file, pulling all lines that contain timecodes and writes to a list.
                    fileLine = fileLine.strip()
                    lineElems = fileLine.split(',')
                    for lineElem in lineElems:

                        pattern = re.compile(r'^(\d\d\d\d\d\d)')

                        if pattern.match(lineElem):
                            result.append(lineElem)

                finalFile = open(name + '_formatted.csv', 'w', newline='') #os.path.join for variableness
                finalFileWriter = csv.writer(finalFile)
                title = str(title)
                finalFileWriter.writerow([title])
                finalList = []
                for rowItem in secondRow:
                    finalList += [str(rowItem)]
                finalFileWriter.writerow(finalList)
                print('Writing EDL contents of new file to final formatted file... \n')

                for currentClip in result:
                    splitter = str(currentClip)
                    splitLine = splitter.split()
                    if len(splitLine) <= 6:
                        sixIndexSplitter(splitLine)
                        continue
                    splitTimes = str(splitLine[4]).split()
                    num = splitLine[0]
                    dstIn = splitLine[6]
                    dstOut = splitLine[7]

                    if ('"]') in dstOut:
                        dstOutSplit = dstOut.split('"')
                        dstOut = dstOutSplit[0]
                        dstIn = Timecode('25', dstIn)
                        dstOut = Timecode('25', dstOut)
                        srcDur = dstOut - dstIn
                        del splitLine[0]
                        splitLine.insert(0, num)
                        del splitLine[-1]
                        splitLine.append(str(srcDur))
                        finalFileWriter.writerow(splitLine)
                        continue

                    dstOutSplit = dstOut.split("'")  #Separates timecode from '] at end
                    dstOut = dstOutSplit[0] #isolates timecode into dstOut variable
                    dstIn = Timecode('25', dstIn)
                    dstOut = Timecode('25', dstOut)
                    srcDur = dstOut - dstIn
                    del splitLine[0]
                    splitLine.insert(0, num)
                    splitLine.append(srcDur)
                    formattedLines.append(splitLine)
                    finalFileWriter.writerow(splitLine)

                # This begins the shortest/longest summary at the bottom of the .edl

                print('Writing second section to formatted EDL file...')
                finalList = []
                finalFileWriter.writerow(finalList)
                numCounter = 0
                clipCount = []
                reelCount = ''
                reel = ''
                numV = 1
                blankTC = '00:00:00:00'
                blankTC = Timecode('25', blankTC)
                earliestSRC = '00:00:00:00'
                earliestSRC = Timecode('25', earliestSRC)
                latestSRC = '00:00:00:00'
                latestSRC = Timecode('25', latestSRC)
                shortestV = '00:00:00:00'
                shortestV = Timecode('25', shortestV)
                longestV = '00:00:00:00'
                longestV = Timecode('25', longestV)
                totalTC = '00:00:00:00'
                totalTC = Timecode('25', totalTC)
                srcTCSum = 0
                reels = {}
                # Defined variables to be used in the nexted Dict that will track data
                # Nested Dict that will track data. Keys and values to see what's happening.

                for line in formattedLines:
                    lineSplit = str(line).split()
                    #If a clip name is not in reels Nested Dict, adds it to clip Key value, creating new dicts for each.
                    if lineSplit[1] not in reels.keys():
                        reels[lineSplit[1]] = {'Clip' : reel, 'Num' : numV, 'Earliest' : earliestSRC, 'Latest' : latestSRC,
                                                  'Shortest' : shortestV, 'Longest' : longestV, 'Total' : totalTC}
                        reels[lineSplit[1]]['Earliest'] = lineSplit[4]
                        reels[lineSplit[1]]['Latest'] = lineSplit[5]
                        reels[lineSplit[1]]['Shortest'] = lineSplit[8]
                        reels[lineSplit[1]]['Longest'] = lineSplit[8]
                        reels[lineSplit[1]]['Total'] = blankTC

                        # srcTCPerLine = lineSplit[8]
                        # srcTCPerLine = srcTCPerLine[0:11]
                        # srcTCPerLine = FramesToTimecode.tc_to_fr(srcTCPerLine)
                        # srcTCSum = srcTCSum + srcTCPerLine
                    else:
                        reels[lineSplit[1]]['Num'] += 1

                    # Adds up of all the Source Timecode amounts for each individual clip

                    earliestSRC = reels[lineSplit[1]].get('Earliest')
                    earliestSRC = earliestSRC[1:12]
                    earliestSRCTemp = lineSplit[4] #Isolate the potential earliest Source TC from formattedLines
                    earliestSRCTemp = earliestSRCTemp[1:12] #Chop out the punctuation to allow it to be read by fr_to_tc
                    earliestSRCinfr = TechnicallySecondsToTimecode.tc_to_fr(earliestSRC) #turn potential earliest TC into no. of fr.
                    earliestSRCTempinfr = TechnicallySecondsToTimecode.tc_to_fr(earliestSRCTemp)

                    if earliestSRCTempinfr < earliestSRCinfr or earliestSRCTempinfr == earliestSRCinfr:
                        earliestSRCTemp = TechnicallySecondsToTimecode.fr_to_tc(earliestSRCTempinfr)

                        reels[lineSplit[1]]['Earliest'] = earliestSRCTemp

                    # This section pulls the latest source Timecode that appears and continually updates.
                    latestSRC = reels[lineSplit[1]].get('Latest')
                    latestSRC = latestSRC[1:12]
                    latestSRCTemp = lineSplit[5]  # Isolate the potential latest Source TC from formattedLines
                    latestSRCTemp = latestSRCTemp[1:12]
                    latestSRCinfr = TechnicallySecondsToTimecode.tc_to_fr(latestSRC)
                    latestSRCTempinfr = TechnicallySecondsToTimecode.tc_to_fr(latestSRCTemp)

                    if latestSRCTempinfr > latestSRCinfr or latestSRCTempinfr == latestSRCinfr:
                        latestSRCTemp = TechnicallySecondsToTimecode.fr_to_tc(latestSRCTempinfr)

                        reels[lineSplit[1]]['Latest'] = latestSRCTemp

                    # This section pulls the Shortest and Longest instances of a clip.

                    shortestSRC = reels[lineSplit[1]].get('Shortest')
                    shortestSRC = shortestSRC[0:11]
                    shortestSRCTemp = lineSplit[8]
                    shortestSRCTemp = shortestSRCTemp[0:11]
                    shortestSRCinfr = TechnicallySecondsToTimecode.tc_to_fr(shortestSRC)
                    shortestSRCTempinfr = TechnicallySecondsToTimecode.tc_to_fr(shortestSRCTemp)

                    if shortestSRCTempinfr < shortestSRCinfr or shortestSRCTempinfr == shortestSRCinfr:
                        shortestSRCTemp = TechnicallySecondsToTimecode.fr_to_tc(shortestSRCTempinfr)

                        reels[lineSplit[1]]['Shortest'] = shortestSRCTemp

                    if shortestSRCTempinfr > shortestSRCinfr or shortestSRCTempinfr == shortestSRCinfr:
                        shortestSRCTemp = TechnicallySecondsToTimecode.fr_to_tc(shortestSRCTempinfr)

                        reels[lineSplit[1]]['Longest'] = shortestSRCTemp

                    totalTC = reels[lineSplit[1]].get('Total')  # Takes current reel's Total source TC count
                    totalTCTemp = lineSplit[8]  # Takes current line's source duration.
                    totalTCTemp = totalTCTemp[0:11]
                    totalTCinfr = TechnicallySecondsToTimecode.tc_to_fr(totalTC) # Turns current total TC into no. of frames
                    totalTCTempinfr = TechnicallySecondsToTimecode.tc_to_fr(totalTCTemp) # Turns current line's TC into no. of frames

                    totalTCinfr = totalTCinfr + totalTCTempinfr
                    totalTCinfr = TechnicallySecondsToTimecode.fr_to_tc(totalTCinfr)
                    reels[lineSplit[1]]['Total'] = totalTCinfr

                # Write the nestedDict created in the previous for loop to the .csv file.

                w = csv.DictWriter(finalFile, thirdRow)
                w.writeheader()
                for k in sorted(reels):
                    w.writerow({field: reels[k].get(field) or k for field in thirdRow})
                finalFile.close()
            else: print(name + ext + ' ignored.')