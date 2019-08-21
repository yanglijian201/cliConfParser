# import bs4
import re
from collections import OrderedDict

class CommonMappingFunc:

    def cliOutToList(self, inputStr):
      # Store each line and its space number
      self.lineNumDic ={ }
      lineNum = 0
      outPutLines = inputStr.split('\n')
      # Format and Store output line, remove the space lines and remove the spaces in each lines.
      self.ftOutPutLines = []
      self.ftOutPutLinesNoStrip = []
      for line in outPutLines:
          if not len(line.strip(' ')):
             continue
          spcNum = len(line)-len(line.lstrip(' '))
          self.lineNumDic[lineNum] = spcNum
          lineNum+=1
          #ftOutPutLines.append('<val>' + line.strip() + '</val>')
          self.ftOutPutLinesNoStrip.append(line)
          self.ftOutPutLines.append(line.strip())
      
      # Reverse Store the hierachy information
      self.cmdHierLv=sorted(set(self.lineNumDic.values()), reverse=True)

    def hasChildHierOrNot(self, currentLine, currentLineNum, currentList = None):
      if currentList is None:
        currentList = self.ftOutPutLinesNoStrip
      listLen = len(currentList)
      if currentLineNum < listLen - 1:
        nextLineSpaceNum = self.getLineSpaceNum(currentList[currentLineNum + 1])
        if nextLineSpaceNum <= self.getLineSpaceNum(currentLine):
          return False
        else:
          return True
      else:
        return False      
    '''
    ## Remove BS4 dependency
    def covertSpaceToXML(self):
      ####
      lineLev = len(self.cmdHierLv) + 1
      for hierLv in self.cmdHierLv:
          lineLev-=1
          addCloseTagFlag = 0
          for lnUm in range(len(self.lineNumDic)):
              lastLineNum = len(self.lineNumDic) -1
              # if the line has the same number of zero in the cmdHierLv then add XML tags to the line.
              if self.lineNumDic[lnUm] == hierLv:
                  self.ftOutPutLines[lnUm] = "<sec" + str(lineLev) + ">" + self.ftOutPutLines[lnUm]
                  if addCloseTagFlag:
                      self.ftOutPutLines[lnUm-1] = self.ftOutPutLines[lnUm-1] + "</sec" + str(lineLev) + ">"
                  addCloseTagFlag = 1
                  if lnUm == lastLineNum:
                      self.ftOutPutLines[lnUm] = self.ftOutPutLines[lnUm] + "</sec" + str(lineLev)+ ">"
                      addCloseTagFlag = 0
      
              # if the line number of the line is bigger than the hierachy level(hierLv) and addCloseTagFlag is 1
              # then add close tag to the above line, and mark addCloseTagFlag to 0
              if self.lineNumDic[lnUm] < hierLv:
                  if addCloseTagFlag:
                      self.ftOutPutLines[lnUm-1] = self.ftOutPutLines[lnUm-1] + "</sec" + str(lineLev) + ">"
                      addCloseTagFlag = 0
      
              # if the line the last line and addCloseTagFlag is 1, add close tag to the last line.
              if lnUm == lastLineNum and addCloseTagFlag:
                  self.ftOutPutLines[lnUm] = self.ftOutPutLines[lnUm] + "</sec" + str(lineLev)+ ">" 
      self.structedFtoutputLines = ''.join(self.ftOutPutLines)

    def reCreateDic(self, entry = 'output'):
      
      soup = bs4.BeautifulSoup(self.structedFtoutputLines, 'html.parser')
      self.reDic = {}
      def restructDic(soupTagInst, reDic, dicKey):
          try :
              self.reDic[dicKey]
          except KeyError:
              self.reDic[dicKey] = []
          if type(soupTagInst.next_element) == bs4.element.NavigableString:
              self.reDic[dicKey].append(unicode(soupTagInst.next_element))
              for eachElement in soupTagInst.next_element.fetchNextSiblings():
                  if type(eachElement) == bs4.element.NavigableString:
                      self.reDic[dicKey].append(unicode(eachElement))
                  if type(eachElement) == bs4.element.Tag:
                      # if not type(eachElement.next_element) == bs4.element.NavigableString:
                      #     raise Exception('each Tag should start with NavigableString!')  
                      newDicKey = dicKey + '.' + unicode(unicode(soupTagInst.next_element))
                      restructDic(eachElement, self.reDic, newDicKey)  
      restructDic(soup.sec1, self.reDic, entry)
      '''
    def reCreateDic(self, entry = 'output'):
      intial = -1
      lineHivInfo = self.lineNumDic
      lineList = self.ftOutPutLines
      self.reDic = OrderedDict()
      totalLineNum =  len(lineHivInfo)
      keyLocationDict = OrderedDict()
      
      dicKey = 'output'
      dicKeyLineNum = -1
      currentSPnum = -1
      

      def getCurrentLineKeyValue(dicKey, currentSPnum, dicKeyLineNum):
          keyList = []
          self.reDic[dicKey] = keyList
          if dicKeyLineNum < totalLineNum - 1:
              nextLineSPnum = lineHivInfo[dicKeyLineNum + 1]
              childLineSP = nextLineSPnum
              if childLineSP <= currentSPnum:
                  del self.reDic[dicKey]
              else:
                  keyList.append(lineList[dicKeyLineNum + 1])
                  newKey = dicKey + '.' + lineList[dicKeyLineNum + 1]
                  keyLocationDict[newKey] = dicKeyLineNum + 1
      
                  if dicKeyLineNum + 2 >= totalLineNum - 1:
                      self.reDic[dicKey] = keyList[:]
                  else:
      
                      for lineNum in range(dicKeyLineNum + 2, totalLineNum):
                          if childLineSP == lineHivInfo[lineNum]:
                              keyList.append(lineList[lineNum])
                              newKey = dicKey + '.' + lineList[lineNum]
                              keyLocationDict[newKey] = lineNum
                              continue
                          if childLineSP > lineHivInfo[lineNum] and lineHivInfo[lineNum] > currentSPnum:
                              keyList.append(lineList[lineNum])
                              newKey = dicKey + '.' + lineList[lineNum]
                              keyLocationDict[newKey] = lineNum
                              childLineSP = lineHivInfo[lineNum]
                              continue
                          if lineHivInfo[lineNum] <= currentSPnum:
                              break
                      self.reDic[dicKey] = keyList[:]
      
          else:
              del self.reDic[dicKey]
          if dicKey not in self.reDic.keys():
              return
          for eachKey in self.reDic[dicKey]:
              newDicKey = dicKey + '.' + eachKey
              newDicKeyLineNum = keyLocationDict[newDicKey]
              newCurrentSPnum = lineHivInfo[newDicKeyLineNum]
              getCurrentLineKeyValue(newDicKey, newCurrentSPnum, newDicKeyLineNum)

      getCurrentLineKeyValue(entry, currentSPnum, dicKeyLineNum)

    def tabToSpace(self, inputStr, spaceNum = 4):
      inputStr = inputStr.replace('\r', '')
      return inputStr.replace('\t', " "*spaceNum)
    def getLineSpaceNum(self, line):
      return len(line) - len(line.lstrip(' '))

    def changeKeyValToCurrentHier(self, currentLine, value, customVal = 0):
      lineSpaceNum = self.getLineSpaceNum(currentLine)
      valList = [' '*(lineSpaceNum + customVal) + value]
      return valList
    def addKeyValToCurrentHier(self, currentLine, key, value, childSpacNum = 2 ):
      lineSpaceNum = self.getLineSpaceNum(currentLine)
      keList = [' '*lineSpaceNum + key]
      valList = [' '*(lineSpaceNum + childSpacNum) + value]
      return keList + valList
    def addKeyValToCustCurrentHier(self, currentLine, key, value, customVal, childSpacNum = 2 ):
      lineSpaceNum = self.getLineSpaceNum(currentLine)
      keList = [' '*(lineSpaceNum + customVal ) + key]
      valList = [' '*(lineSpaceNum + customVal + childSpacNum) + value]
      return keList + valList
    def addKeyValToNextChildHier(self, currentLine, currentLineNum, key, value, currentList = None, childSpacNum = 2):
      if currentList is None:
        currentList = self.ftOutPutLinesNoStrip
      if self.hasChildHierOrNot(currentLine, currentLineNum, currentList):
        return self.addKeyValToCurrentHier(currentList[currentLineNum + 1], key, value, childSpacNum)
      else:
        return self.addKeyValToCurrentHier(currentLine, key, value, childSpacNum)
    def processMultLine(self, lineNum, processLineNum = 2, currentList = None):
      if currentList is None:
        currentList = self.ftOutPutLinesNoStrip
      newProcessString = currentList[lineNum]
      for addLineNum in range(1, processLineNum):
        newProcessString = newProcessString + currentList[lineNum + addLineNum]
      return [newProcessString]

class Show_policymap_interface(CommonMappingFunc):
    def __init__(self, cliQosSerPolicyOut):
      self.cliQosSerPolicyOut = cliQosSerPolicyOut
      strTabToSpace = self.tabToSpace(cliQosSerPolicyOut)
      self.cliOutToList(strTabToSpace)
    def matchClassMap(self, inputLine):
      matchResult = re.search('Class-map: +(.*) +\(match-(.*)\)',inputLine)
      if matchResult:
        return [True, matchResult.group(1), matchResult.group(2)]
      else:
        return [False, None, None, None]
    def matchSerPolicy(self, inputLine):
      matchResult = re.search('Service-policy +.*: +(.*)',inputLine)
      if matchResult:
        return [True, matchResult.group(1)]
      else:
        return [False, None]      
    def matchPacketByte(self, inputLine):
      matchResult = re.search('^ *(\d+) +packets, +(\d+) bytes *$',inputLine)
      if matchResult:
        return [True, matchResult.group(1), matchResult.group(2)]
      else:
        return [False, None, None]
    def matchOfferedDropRate(self, inputLine):
      matchResult = re.search('(\d+) minute offered rate (\d+) bps, drop rate (\d+) bps',inputLine)
      if matchResult:
        return [True, matchResult.group(2), matchResult.group(3)]
      else:
        return [False, None, None] 
    def matchCondition(self, inputLine):
      matchResult = re.search('Match: +(.+)',inputLine)
      if matchResult:
        return [True, matchResult.group(1)]
      else:
        return [False, None] 
    def matchQueLimit(self, inputLine):
      matchResult = re.search('queue limit (\d+) (.+)',inputLine)
      if matchResult:
        return [True, matchResult.group(1)]
      else:
        return [False, None] 
    def matchQueDepthDropsNobuffer(self, inputLine):
      matchResult = re.search('\(queue depth/total drops/no-buffer drops\) (\d+)/(\d+)/(\d+)',inputLine)
      if matchResult:
        return [True, matchResult.group(1), matchResult.group(2), matchResult.group(3)]
      else:
        return [False, None, None, None] 
    def matchPktOutByteOut(self, inputLine):
      matchResult = re.search('\(pkts output/bytes output\) (\d+)/(\d+)',inputLine)
      if matchResult:
        return [True, matchResult.group(1), matchResult.group(2)]
      else:
        return [False, None, None] 
    def matchShapeCirBcBe(self, inputLine):
      matchResult = re.search('shape \(average\) cir (\d+), bc (\d+), be (\d+)',inputLine)
      if matchResult:
        return [True, matchResult.group(1), matchResult.group(2), matchResult.group(3)]
      else:
        return [False, None, None, None]  
    def matchTargetShapRate(self, inputLine):
      matchResult = re.search('target shape rate (\d+)',inputLine)
      if matchResult:
        return [True, matchResult.group(1)]
      else:
        return [False, None] 
    def matchQueStats(self, inputLine):
      matchResult = re.search('queue stats for (.+) classes:',inputLine)
      if matchResult:
        return [True]
      else:
        return [False] 
    def matchPriLevel(self, inputLine):
      matchResult = re.search('[pP]riority +[lL]evel.* +(\d+)',inputLine)
      if matchResult:
        return [True, matchResult.group(1)]
      else:
        return [False, None]     
    def matchBandWidth(self, inputLine):
      matchResult = re.search('bandwidth (\d+\%) \((\d+ kbps)\)',inputLine)
      if matchResult:
        return [True, matchResult.group(1), matchResult.group(2)]
      else:
        return [False, None, None]
    def matchWREDExpWeight(self, inputLine):
      matchResult = re.search('Exp-weight-constant: (\d+) \((\d+/\d+)\)',inputLine)
      if matchResult:
        return [True, matchResult.group(1), matchResult.group(2)]
      else:
        return [False, None, None]
    def matchWREDMeanQueDep(self, inputLine):
      matchResult = re.search('Mean queue depth: (\d+) packets',inputLine)
      if matchResult:
        return [True, matchResult.group(1)]
      else:
        return [False, None]
    def matchWREDPre(self, inputLine):
      matchResult = re.search('(\d+) +(\d+)/(\d+) +(\d+)/(\d+) +(\d+)/(\d+) +(\d+) +(\d+) +(\d+/\d+)',inputLine)
      if matchResult:
        returnResult = [True]
        for gnum in range(1,11):
          returnResult.append(matchResult.group(gnum))
        return returnResult
      else:
        return [False, None, None, None, None, None, None, None, None, None, None]
    def matchWREDstart(self, inputLine):
      matchResult = re.search('class +Transmitted +Random drop +Tail drop +Minimum +Maximum +Mark',inputLine)
      if matchResult:
        return [True]
      else:
        return [False]
    def matchPolice(self, inputLine):
      matchResult = re.search(' +police:',inputLine)
      if matchResult:
        return [True]
      else:
        return [False]

    def matchPoliceCirSpeedLimit(self, inputLine):
      matchResult = re.search('cir +(\d+) +bps.* +bc +(\d+) +bytes',inputLine)
      if matchResult:
        return [True, matchResult.group(1), matchResult.group(2)]
      else:
        return [False, None, None]

    def matchPoliceCir(self, inputLine):
      matchResult = re.search('cir +(\d+) +\%',inputLine)
      if matchResult:
        return [True, matchResult.group(1)]
      else:
        return [False, None]

    def matchPoliceConform(self, inputLine):
      matchResult = re.search('conformed (\d+) packets, (\d+) bytes; actions:',inputLine)
      if matchResult:
        return [True, matchResult.group(1), matchResult.group(2)]
      else:
        return [False, None, None]

    def matchMulPoliceConformAction(self, inputLine):
      matchResult = re.search('conformed (\d+) packets, (\d+) bytes; actions: +(.*) *',inputLine,re.DOTALL)
      if matchResult:
        return [True, matchResult.group(1), matchResult.group(2), matchResult.group(3)]
      else:
        return [False, None, None, None]

    def matchPoliceExceed(self, inputLine):
      matchResult = re.search('exceeded (\d+) packets, (\d+) bytes; actions:',inputLine)
      if matchResult:
        return [True, matchResult.group(1), matchResult.group(2)]
      else:
        return [False, None, None]

    def matchMulPoliceExceedAction(self, inputLine):
      matchResult = re.search('exceeded (\d+) packets, (\d+) bytes; actions: +(.*) *',inputLine,re.DOTALL)
      if matchResult:
        return [True, matchResult.group(1), matchResult.group(2), matchResult.group(3)]
      else:
        return [False, None, None, None]

    def matchPoliceConformSpeed(self, inputLine):
      matchResult = re.search('conformed (\d+) bps, exceeded (\d+) bps',inputLine)
      if matchResult:
        return [True, matchResult.group(1), matchResult.group(2)]
      else:
        return [False, None, None]

    def formatOutput(self, notMatchInclude = True):
      listLength = len(self.ftOutPutLinesNoStrip)
      self.matchSingleFunList = [self.matchClassMap, self.matchSerPolicy, self.matchPacketByte, self.matchOfferedDropRate, \
        self.matchCondition, self.matchQueLimit, self.matchQueDepthDropsNobuffer, self.matchPktOutByteOut, \
        self.matchShapeCirBcBe, self.matchTargetShapRate, self.matchQueStats, self.matchPriLevel, self.matchBandWidth, self.matchWREDExpWeight, \
        self.matchWREDMeanQueDep, self.matchWREDstart, self.matchWREDPre, self.matchPolice, self.matchPoliceCir, self.matchPoliceCirSpeedLimit, self.matchPoliceConformSpeed]
      self.formatedOutput = []
      skipLine = 0
      for lineNum in range(listLength):
        if skipLine > lineNum:
          continue
        skipLine += 1
        for eachFun in self.matchSingleFunList:
          funReturnVal = eachFun(self.ftOutPutLinesNoStrip[lineNum])
          if funReturnVal[0]:
            if eachFun.__name__ == 'matchSerPolicy':
              # pdb.set_trace()
              servicePolicyName = funReturnVal[1]
              self.formatedOutput.append(self.changeKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], servicePolicyName))
            elif eachFun.__name__ == 'matchClassMap':
              classMapName = funReturnVal[1]
              match_method = funReturnVal[2]
              self.formatedOutput.append(self.changeKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], classMapName))
              self.formatedOutput.append(self.addKeyValToNextChildHier(self.ftOutPutLinesNoStrip[lineNum], lineNum, "match_method", match_method))
            elif eachFun.__name__ == 'matchPacketByte':
              packets = funReturnVal[1]
              bytes = funReturnVal[2]
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "packets", packets))
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "bytes", bytes))
            elif eachFun.__name__ == 'matchOfferedDropRate':
              offered_rate = funReturnVal[1]
              drop_rate = funReturnVal[2]
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "offered_rate", offered_rate))
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "drop_rate", drop_rate))
            elif eachFun.__name__ == 'matchCondition':
              match_types = funReturnVal[1]
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "match_types", match_types))
            elif eachFun.__name__ == 'matchQueLimit':
              queue_limit = funReturnVal[1]
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "queue_limit", queue_limit))
            elif eachFun.__name__ == 'matchQueDepthDropsNobuffer':
              queue_depth = funReturnVal[1]
              total_drops = funReturnVal[2]
              nobuffer_drops = funReturnVal[3]
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "queue_depth", queue_depth))
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "total_drops", total_drops))
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "nobuffer_drops", nobuffer_drops))
            elif eachFun.__name__ == 'matchPktOutByteOut':
              pkts_output = funReturnVal[1]
              bytes_output = funReturnVal[2]
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "pkts_output", pkts_output))
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "bytes_output", bytes_output))
            elif eachFun.__name__ == 'matchShapeCirBcBe':
              shape_avg_cir = funReturnVal[1]
              shape_avg_bc = funReturnVal[2]
              shape_avg_be = funReturnVal[3]
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "shape_avg_cir", shape_avg_cir))
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "shape_avg_bc", shape_avg_bc))
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "shape_avg_be", shape_avg_be))
            elif eachFun.__name__ == 'matchTargetShapRate':
              shape_rate = funReturnVal[1]
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "shape_rate", shape_rate))
            elif eachFun.__name__ == 'matchQueStats':
              self.formatedOutput.append(self.changeKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "queue_stats"))
            elif eachFun.__name__ == 'matchPriLevel':
              priority_level = funReturnVal[1]
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "priority_level", priority_level))
            elif eachFun.__name__ == 'matchBandWidth':
              bandwidth_percent = funReturnVal[1]
              bandwidth_speed = funReturnVal[2]
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "bandwidth_percent", bandwidth_percent))
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "bandwidth_speed", bandwidth_speed))
            elif eachFun.__name__ == 'matchWREDExpWeight':
              exp_weight_constant = funReturnVal[1]
              decay_constant = funReturnVal[2]
              self.formatedOutput.append(self.addKeyValToCustCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "exp_weight_constant", exp_weight_constant, -2))
              self.formatedOutput.append(self.addKeyValToCustCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "decay_constant", decay_constant, -2))
            elif eachFun.__name__ == 'matchWREDMeanQueDep':
              mean_queue_depth = funReturnVal[1]
              self.formatedOutput.append(self.addKeyValToCustCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "mean_queue_depth", mean_queue_depth, -2))
            elif eachFun.__name__ == 'matchWREDstart':
              self.formatedOutput.append(self.changeKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "precedence", -2))
            elif eachFun.__name__ == 'matchWREDPre':
              precedence = funReturnVal[1]
              wred_tx_pkts = funReturnVal[2]
              wred_tx_bytes = funReturnVal[3]
              rand_drops_pkts = funReturnVal[4]
              rand_drops_bytes = funReturnVal[5]
              tail_drops_pkts = funReturnVal[6]
              tail_drops_bytes = funReturnVal[7]
              min_thresh = funReturnVal[8]
              max_thresh = funReturnVal[9]
              mark_prob = funReturnVal[10]
              self.formatedOutput.append(self.changeKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], precedence))
              self.formatedOutput.append(self.addKeyValToCustCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "wred_tx_pkts", wred_tx_pkts, 2))
              self.formatedOutput.append(self.addKeyValToCustCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "wred_tx_bytes", wred_tx_bytes, 2))
              self.formatedOutput.append(self.addKeyValToCustCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "rand_drops_pkts", rand_drops_pkts, 2))
              self.formatedOutput.append(self.addKeyValToCustCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "rand_drops_bytes", rand_drops_bytes, 2))
              self.formatedOutput.append(self.addKeyValToCustCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "tail_drops_pkts", tail_drops_pkts, 2))
              self.formatedOutput.append(self.addKeyValToCustCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "tail_drops_bytes", tail_drops_bytes, 2))
              self.formatedOutput.append(self.addKeyValToCustCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "min_thresh", min_thresh, 2))
              self.formatedOutput.append(self.addKeyValToCustCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "max_thresh", max_thresh, 2))
              self.formatedOutput.append(self.addKeyValToCustCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "mark_prob", mark_prob, 2))
            elif eachFun.__name__ == 'matchPolice':
              self.formatedOutput.append(self.changeKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "police"))
            elif eachFun.__name__ == 'matchPoliceCir':
              cir_percent = funReturnVal[1]
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "cir_percent", cir_percent))
            elif eachFun.__name__ == 'matchPoliceCirSpeedLimit':
              cir_bps = funReturnVal[1]
              cir_limit = funReturnVal[2]
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "cir_bps", cir_bps))
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "cir_limit", cir_limit))
            elif eachFun.__name__ == 'matchPoliceConformSpeed':
              conform_bps = funReturnVal[1]
              exceed_bps = funReturnVal[2]
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "conform_bps", conform_bps))
              self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "exceed_bps", exceed_bps))
            break
        else:
          self.matchMultiFunList = [self.matchPoliceConform, self.matchPoliceExceed]
          for eachFun in self.matchMultiFunList:
            funReturnVal = eachFun(self.ftOutPutLinesNoStrip[lineNum])
            if funReturnVal[0]:
              if eachFun.__name__ == 'matchPoliceConform':
                multifunReMatch = self.processMultLine(lineNum)
                skipLine += 1
                multifunReVal = self.matchMulPoliceConformAction(multifunReMatch[0])
                if not multifunReVal[0]:
                  print('ERROR: multifunReVal')
                  continue
                conformed_pkt = multifunReVal[1]
                conformed_bytes = multifunReVal[2]
                conformed_action = multifunReVal[3]
                self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "conformed_pkt", conformed_pkt))
                self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "conformed_bytes", conformed_bytes))
                self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "conformed_action", conformed_action))
              elif eachFun.__name__ == 'matchPoliceExceed':
                multifunReMatch = self.processMultLine(lineNum)
                skipLine += 1
                multifunReVal = self.matchMulPoliceExceedAction(multifunReMatch[0])
                if not multifunReVal[0]:
                  print('ERROR: multifunReVal')
                  continue                
                exceeded_pkt = multifunReVal[1]
                exceeded_bytes = multifunReVal[2]
                exceeded_action = multifunReVal[3]
                self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "exceeded_pkt", exceeded_pkt))
                self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "exceeded_bytes", exceeded_bytes))
                self.formatedOutput.append(self.addKeyValToCurrentHier(self.ftOutPutLinesNoStrip[lineNum], "exceeded_action", exceeded_action))

class show_cmd_output_analyze():
  def __init__(self, inputStr, className = Show_policymap_interface):
    inst = className(inputStr)
    inst.formatOutput() 
    tmpList = []
    self.internalreCreatedOutputList = inst.formatedOutput
    for eachList in self.internalreCreatedOutputList:
      tmpList = tmpList + eachList
    recreatedOutput = '\n'.join(tmpList)
    inst = className(recreatedOutput) 
    # inst.covertSpaceToXML()
    inst.reCreateDic()
    self.outputDict = inst.reDic
  def entryIsKeyOrNot(self, dictEnty = 'output', dictName = None):
    if dictName is None:
      dictName = self.outputDict
    try:
      dictName[dictEnty]
    except KeyError:
      return False
    return True
  def exportDict(self, inputEntry = None):
    if inputEntry is None:
      inputEntry = 'output'
      return self.outputDict
    returnDic = {}
    for eachKey in self.outputDict.keys():
      if re.search('^' + inputEntry, eachKey):
        newEntry = inputEntry.split('.')[-1]
        if not eachKey[len(inputEntry) + 1:]:
          exportKey = newEntry
        else:
          exportKey = newEntry + '.' + eachKey[len(inputEntry) + 1:]
        returnDic[exportKey] = self.outputDict[eachKey]
    return returnDic
  def remvDupList(self, list):
    returnList = []
    remvDict = {}
    for eachItem in list:
      remvDict[eachItem] = 0
    for eachItem in list:
      if remvDict[eachItem] == 0:
        returnList.append(eachItem)
        remvDict[eachItem] += 1
    return returnList
  def printDict(self, dictEnty = 'output', dictName = None, hierSpaceNum = 2, hierLev = None):
    # pdb.set_trace()
    try:
      rePrint
    except NameError:
      rePrint = {}
    try:
      rePrint[dictEnty]
    except KeyError:
      rePrint[dictEnty] = 0
    if hierLev is None:
      headSpaceNum = 0
      hierLev = 0
    else:
      headSpaceNum = hierSpaceNum * hierLev
    if dictName is None:
      dictName = self.outputDict
    if not self.entryIsKeyOrNot(dictEnty):
      print(' ' * headSpaceNum + dictEnty)
      print('It seems that you input incorrect Entry')
      return False
    valueList = self.remvDupList(dictName[dictEnty])
    if len(valueList) == 1:
      if not self.entryIsKeyOrNot(dictEnty + '.' + valueList[0]):
        print(' ' * headSpaceNum + dictEnty.split('.')[-1] + ' ' +'=' + ' ' + valueList[0])
      else:
        if not rePrint[dictEnty]:
          print(' ' * headSpaceNum + dictEnty.split('.')[-1])
          rePrint[dictEnty] += 1
        self.printDict(dictEnty + '.' + valueList[0], hierLev = hierLev + 1)
    else:
      for eachVal in valueList:
        if not rePrint[dictEnty]:
          print(' ' * headSpaceNum + dictEnty.split('.')[-1])
          rePrint[dictEnty] += 1
        self.printDict(dictEnty + '.' + eachVal, hierLev = hierLev + 1)
