# HOMAcalc v2.0
# HOMA calculator, powered by Python 3.9
# Last Update: 2021-06-03
# Author: Zhe Wang
# Homepage: https://www.wangzhe95.net/program-homacalc

print("*******************************************************************************")
print("*                                                                             *")
print("*                                                                             *")
print("*                               H O M A c a l c                               *")
print("*                                                                             *")
print("*                                                                             *")
#print("*     ====================== Version 2.0 for macOS ======================     *")
#print("*     ====================== Version 2.0 for Linux ======================     *")
#print("*     ================ Version 2.0 for Microsoft Windows ================     *")
print("*     =================== Version 2.0 for Source Code ===================     *")
print("*                           Last update: 2021-06-03                           *")
print("*                                                                             *")
print("*         A HOMA calculator, developed by Zhe Wang. Online document is        *")
print("*        available from https://www.wangzhe95.net/program-homacalc .          *")
print("*                                                                             *")
print("*                             -- Catch me with --                             *")
print("*                         E-mail  wongzit@yahoo.co.jp                         *")
print("*                       Homepage  https://www.wangzhe95.net                   *")
print("*                         GitHub  https://github.com/wongzit                  *")
print("*                                                                             *")
print("*******************************************************************************")
print("\nPRESS Ctrl+c to exit the program.\n")

def elementDetermin (userInputted2):
	calcAtom2 = userInputted2[:]
	calcAtom2.append(userInputted2[0])
	userElements =[]
	for j in range(len(calcAtom2)):
		userElements.append(element[int(calcAtom2[j]) - 1])
	return userElements

def calcHOMA (userInputted, elementList):
	calcAtom = userInputted[:]
	calcAtom.append(userInputted[0])
	disMatrix = []
	for i in range(len(userInputted)):
		disABx = float(xCoors[int(calcAtom[i]) - 1]) - float(xCoors[int(calcAtom[i + 1]) - 1])
		disABy = float(yCoors[int(calcAtom[i]) - 1]) - float(yCoors[int(calcAtom[i + 1]) - 1])
		disABz = float(zCoors[int(calcAtom[i]) - 1]) - float(zCoors[int(calcAtom[i + 1]) - 1])
		disAB = pow(disABx * disABx + disABy * disABy + disABz * disABz, 0.5)
		disMatrix.append(format(disAB, '.3f'))
	sumDiff = 0.0000
	for j in range(len(disMatrix)):
		if elementList[j] == 'C' and elementList[j + 1] == 'C':
			Ropt = 1.397
			alpha = 98.89
		elif elementList[j] == 'C' and elementList[j + 1] == 'N':
			Ropt = 1.334
			alpha = 93.52
		elif elementList[j] == 'N' and elementList[j + 1] == 'C':
			Ropt = 1.334
			alpha = 93.52
		elif elementList[j] == 'C' and elementList[j + 1] == 'O':
			Ropt = 1.265
			alpha = 157.38
		elif elementList[j] == 'O' and elementList[j + 1] == 'C':
			Ropt = 1.265
			alpha = 157.38
		elif elementList[j] == 'C' and elementList[j + 1] == 'P':
			Ropt = 1.698
			alpha = 118.91
		elif elementList[j] == 'P' and elementList[j + 1] == 'C':
			Ropt = 1.698
			alpha = 118.91
		elif elementList[j] == 'C' and elementList[j + 1] == 'S':
			Ropt = 1.677
			alpha = 94.09
		elif elementList[j] == 'S' and elementList[j + 1] == 'C':
			Ropt = 1.677
			alpha = 94.09
		elif elementList[j] == 'N' and elementList[j + 1] == 'N':
			Ropt = 1.309
			alpha = 130.33
		elif elementList[j] == 'N' and elementList[j + 1] == 'O':
			Ropt = 1.248
			alpha = 57.21
		elif elementList[j] == 'O' and elementList[j + 1] == 'N':
			Ropt = 1.248
			alpha = 57.21
#		elif elementList[j] == 'x' and elementList[j + 1] == 'x':
#			Ropt = 1
#			alpha = 100
		diffRoptRi = (float(disMatrix[j]) - Ropt) * (float(disMatrix[j]) - Ropt) * alpha
		sumDiff += diffRoptRi
	valueHOMA = 1 - sumDiff / float(len(disMatrix))
	return valueHOMA

print("Please specify the Gaussian output file path:")

# For Unix/Linux OS
fileName = input("(e.g.: /HOMAcalc/example/4cpp.log)\n")
if fileName.strip()[0] == '\'' and fileName.strip()[-1] == '\'':
    fileName = fileName.strip()[1:-1]

# For Microsoft Windows
#fileName = input("(e.g.: C:\\HOMAcalc\\example\\4cpp.log\n")
#if fileName.strip()[0] == '\"' and fileName.strip()[-1] == '\"':
#    fileName = fileName.strip()[1:-1]

with open(fileName.strip(), 'r') as logFile:
	logFileLines = logFile.readlines()

endOutput = []

print("\n------ Parameters used in HOMAcalc ------")
print("")
print(" J. Chem. Inf. Comput. Sci. 1993, 33, 70 ")
print("")
print("-----------------------------------------\n")

alpha = 98.89
Ropt = 1.397

for lineNo in range(len(logFileLines) - 1, 0, -1):
	endOutput.append(logFileLines[lineNo])
	if logFileLines[lineNo][:5] == ' 1\\1\\':
		break

endOutput.reverse()
endOutput2 = []

for endLineNo in range(len(endOutput)):
	endOutput2.append(endOutput[endLineNo].strip())

endOutStr = "".join(endOutput2)
endOutput3 = endOutStr.split('\\')
endOutput4 = []

for endLineNo3 in range(len(endOutput3)):
	if endOutput3[endLineNo3].count('.') == 3 and endOutput3[endLineNo3].count(',') == 3:
		if endOutput3[endLineNo3][0].isalpha():
			endOutput4.append(endOutput3[endLineNo3])

xCoors = []
yCoors = []
zCoors = []
element = []

for endLineNo4 in range(len(endOutput4)):
	element.append(endOutput4[endLineNo4].split(',')[0])
	xCoors.append(endOutput4[endLineNo4].split(',')[1])
	yCoors.append(endOutput4[endLineNo4].split(',')[2])
	zCoors.append(endOutput4[endLineNo4].split(',')[3])

print("Please input the atom numbers, separated by space:")
userInput = input("(e.g.: 1 2 3 4 5 6)\n")

while userInput != 'q':
	while True:
		try:
			userInputList = userInput.split()
			break
		except ValueError:
			print("\nInput error, HOMAcalc termination.")
	userElementList = elementDetermin(userInputList)
	print(f"\nHOMA value of ring [{userInput}] is {format(calcHOMA(userInputList, userElementList), '.4f')}.")
	print("\nInput atom numbers to calculate for other ring,")
	userInput = input("or input \'q\' to quit HOMAcalc.\n")

print("\n*******************************************************************************")
print("")
print("                       Normal termination of HOMAcalc.")
print("")
print("*******************************************************************************\n")
