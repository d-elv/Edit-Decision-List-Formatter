import os, csv, re, sys, itertools
from csv import DictWriter
from timecode import Timecode

def sixIndexSplitter(splitLine):
    splitLine = re.split(r'\s{2,}', splitter)
    dstIn = splitTimes[2]
    dstOut = splitTimes[3]
    dstOutSplit = dstOut.split("'")  #Separates timecode from '] at end
    dstOut = dstOutSplit[0] #isolates timecode into dstOut variable
    dstIn = Timecode('25', dstIn)
    dstOut = Timecode('25', dstOut)
    srcDur = dstOut - dstIn
    del splitLine[0]
    splitLine.insert(0, num)
    del splitLine[-1]
    splitLine.append(str(srcDur))
    finalFileWriter.writerow(splitLine)


secondRow = ['Num', 'Reel', 'Tracks', 'Type', 'Src In', 'Src Out', 'Dst In', 'Dst Out', 'Src Dur']
thirdRow = ['Reel', 'Num', 'Earliest', 'Latest', 'Shortest', 'Longest', 'Total']
directoryToHack = input('Drag in the directory / file you wish to convert and hit enter: ')
print('Drag in the folder containing the file(s) you want to convert. Dragging in a single file will close the program. ')

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

                #This begins the shortest/longest summary at the bottom of the .edl
                # finalFile.close()
                print('Writing second section to formatted EDL file...')
                finalList = []
                for rowItem in thirdRow:
                    finalList += [str(rowItem)]
                finalFileWriter.writerow(finalList)
                reelCount = ''
                reel = ''
                numV = ''
                earliestSRC = ''
                latestSRC = ''
                shortestV = ''
                longestV = ''
                totalTC = ''
                # Defined variables to be used in the nexted Dict that will track data
                reels = {reelCount : {'Clip' : reel, 'Num' : numV, 'Earliest' : earliestSRC, 'Latest' : latestSRC,
                                         'Shortest' : shortestV, 'Longest' : longestV, 'Total' : totalTC}}
                # Nested Dict that will track data. Keys and values to see what's happening.
                for line in formattedLines:
                    lineSplit = str(line).split()
                    if lineSplit[1] not in reels[reelCount]['Clip']:
                        reelNew = lineSplit[1]
                        updaterDict = {reelNew : {'Clip' : lineSplit[1]}}
                        reels.update(updaterDict)



                        # reels[reelCount]['Clip'] = lineSplit[1]

                # dictWriter = csv.DictWriter(finalFile, reels)
                # for key,val in sorted(reels.items()):
                #     row = {'Clip': key}
                #     row.update(val)
                #     print(row)
                #     dictWriter.writerow(row)

                #TODO - Go through formattedLines list, create a summary starting with reel

                #Increment through formattedLines, for every new reel, add a new key to the reels dict.
                #For every same reel, update the information in its respective key value pairing.










                finalFile.close()

            else: print(name + ext + ' ignored.')

                    # splitter = str(i)
                    # splitLine = splitter.split()
                    # if len(splitLine) <= 6:
                    #     #sixIndexSplitter(splitLine)
                    #     continue
                    # splitTimes = str(splitLine[4]).split()
                    # num = splitLine[0]
                    # #num = num[2:]
                    # dstIn = splitLine[6]
                    # dstOut = splitLine[7]
                    #
                    # if ('"]') in dstOut:
                    #     dstOutSplit = dstOut.split('"')
                    #     dstOut = dstOutSplit[0]
                    #     dstIn = Timecode('25', dstIn)
                    #     dstOut = Timecode('25', dstOut)
                    #     srcDur = dstOut - dstIn
                    #     del splitLine[0]
                    #     splitLine.insert(0, num)
                    #     del splitLine[-1]
                    #     splitLine.append(str(srcDur))
                    #     #finalFileWriter.writerow(splitLine)
                    #     continue
                    #
                    # dstOutSplit = dstOut.split("'")  #Separates timecode from '] at end
                    # dstOut = dstOutSplit[0] #isolates timecode into dstOut variable
                    # dstIn = Timecode('25', dstIn)
                    # dstOut = Timecode('25', dstOut)
                    # srcDur = dstOut - dstIn
                    # del splitLine[0]
                    # splitLine.insert(0, num)
                    # splitLine.append(srcDur)
                    # del splitLine[2:4]      #From this point the new section begins formatting.
                    # result2 = []            #Deletes Tracks and Source
                    #
                    # num2 = splitLine[0]
                    # reel2 = splitLine[1]
                    # earliest2 = splitLine[2]
                    # earliest2TC = Timecode('25', earliest2)
                    # latest2 = splitLine[3]
                    # latest2TC = Timecode('25', latest2)
                    # shortest2 = str(splitLine[6])
                    # shortest2TC = Timecode('25', shortest2)
                    # longest2 = str(splitLine[6])
                    # longest2TC = Timecode('25', longest2)
                    #
                    # lineForDict = [num2, earliest2TC, latest2TC, shortest2TC, longest2TC]
                    #
                    # dictionary = {reel2: [lineForDict]}
                    #
                    # if reel2 not in dictionary:
                    #     if num2 not in lineForDict:
                    #
                    #
                    #
                    #
                    #
                    #
                    # print(splitLine)
