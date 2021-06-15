# ICSScub3D v1.0 2021-06-06
# 3D version of ICSScsv
# Extracting shielding tensor and save as .cub file
# Written by Zhe Wang, Hiroshima university
# Catch me with wongzit@yahoo.co.jp
# Personal webpage: https://www.wangzhe95.net

# Program information section
print("*******************************************************************************")
print("*                                                                             *")
print("*                              I C S S c u b 3 D                              *")
print("*                                                                             *")
print("*     =================== Version 1.0 for Source Code ===================     *")
# Choose platform (for packaging)
#print("*     ====================== Version 1.0 for macOS ======================     *")
#print("*     ====================== Version 1.0 for Linux ======================     *")
#print("*     ================ Version 1.0 for Microsoft Windows ================     *")
print("*                           Last update: 2021-06-06                           *")
print("*                                                                             *")
print("*     Extract magnetic shielding tensor from 3D-ICSS output file, developed   *")
print("*    by Zhe Wang. Online document is available from GitHub.                   *")
print("*                                   (https://github.com/wongzit/ICSScub3D)    *")
print("*                                                                             *")
print("*                             -- Catch me with --                             *")
print("*                         E-mail  wongzit@yahoo.co.jp                         *")
print("*                       Homepage  https://www.wangzhe95.net                   *")
print("*                                                                             *")
print("*******************************************************************************")
print("\nPRESS Ctrl+c to exit the program.\n")

def elementNo (element):
	eleNumber = 6.000000
	periodTable = ['Bq', 'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', \
					'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', \
					'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', \
					'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Ym', 'Yb', 'Lu', 'Ha', 'Ta', \
					'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', \
					'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', \
					'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']
	eleNumber = periodTable.index(element)
	return eleNumber

# ========================== Read original output file ==========================
print("Please specify the Gaussian output file path of NMR task:")
print("Assume that you input \"/path/ben_\", then /path/ben_0001.log, /path/ben_0002.log,\
	 /path/ben_0003.log, ... will be loaded.")

# For Unix/Linux OS
fileName = input("(e.g.: /ICSScub3D/example/methylazulene_3DICSS_)\n")
if fileName.strip()[0] == '\'' and fileName.strip()[-1] == '\'':
    fileName = fileName.strip()[1:-1]

# For Microsoft Windows
#fileName = input("(e.g.: C:\\ICSScub3D\\example\\methylazulene_3DICSS_\n")
#if fileName.strip()[0] == '\"' and fileName.strip()[-1] == '\"':
#    fileName = fileName.strip()[1:-1]

maxFileNumber = 999999
fileNameList = []
for i in range(1, maxFileNumber):
	i2 = '%04d' % i
	currentFileTest = fileName.strip() + str(i2) + '.log'
	try:
		with open(currentFileTest, 'r') as icssOutTest:
			fileNameList.append(currentFileTest)
	except FileNotFoundError:
		break

totalFiles = len(fileNameList)
if totalFiles == 1:
	print("\nICSScsv3D found 1 output file.")
elif totalFiles > 1:
	print(f"\nICSScsv3D found {totalFiles} output files.")

print("\nPlease wait...")
print("ICSScub3D is extracting magnetic shielding tensor from the output files...\n")

shieldTensorIso = []
shieldTensorAni = []
shieldTensorXX = []
shieldTensorYX = []
shieldTensorZX = []
shieldTensorXY = []
shieldTensorYY = []
shieldTensorZY = []
shieldTensorXZ = []
shieldTensorYZ = []
shieldTensorZZ = []
bqCoorsXList = []
bqCoorsYList = []
bqCoorsZList = []

for j in range(len(fileNameList)):
	with open(fileNameList[j], 'r') as icssOut:
		outputLines = icssOut.readlines()

	print(f"Processing {fileNameList[j]}...")

	for line1 in outputLines:
		if 'Bq              ' in line1:
			bqCoorsXList.append(line1.split()[1])
			bqCoorsYList.append(line1.split()[2])
			bqCoorsZList.append(line1.split()[3])
		elif 'NumDoF:  NAt= ' in line1:
			sysAtomNumbers1 = int(line1.split()[2])

	tensorCount = 0

	for outputLine in outputLines:
		if ' NumDoF:  NAt=' in outputLine:
			sysAtomNumbers = int(outputLine.split()[2])
			bqAtomNumbers = int(outputLine.split()[4]) - int(outputLine.split()[2])
		elif 'Isotropic =' in outputLine:
			tensorCount += 1
			if tensorCount > sysAtomNumbers:
				shieldTensorIso.append(- float(outputLine.split()[4]))
				shieldTensorAni.append(- float(outputLine.split()[7]))
		elif ('XX=  ' in outputLine) and ('YX=  ' in outputLine) and ('ZX=  ' in outputLine) and (tensorCount > sysAtomNumbers):
			shieldTensorXX.append(- float(outputLine.split()[1]))
			shieldTensorYX.append(- float(outputLine.split()[3]))
			shieldTensorZX.append(- float(outputLine.split()[5]))
		elif ('XY=  ' in outputLine) and ('YY=  ' in outputLine) and ('ZY=  ' in outputLine) and (tensorCount > sysAtomNumbers):
			shieldTensorXY.append(- float(outputLine.split()[1]))
			shieldTensorYY.append(- float(outputLine.split()[3]))
			shieldTensorZY.append(- float(outputLine.split()[5]))
		elif ('XZ=  ' in outputLine) and ('YZ=  ' in outputLine) and ('ZZ=  ' in outputLine) and (tensorCount > sysAtomNumbers):
			shieldTensorXZ.append(- float(outputLine.split()[1]))
			shieldTensorYZ.append(- float(outputLine.split()[3]))
			shieldTensorZZ.append(- float(outputLine.split()[5]))

sysCoorCount = 0
sysElemsList = []
sysCoorsXList = []
sysCoorsYList = []
sysCoorsZList = []

with open(fileName.strip() + '0001.log', 'r') as icssOut:
	outLines2 = icssOut.readlines()

for line2 in outLines2:
	if line2.strip() and line2.count('.') == 3 and line2.strip()[0].isalpha():
		sysElemsList.append(line2.split()[0])
		sysCoorsXList.append(line2.split()[1])
		sysCoorsYList.append(line2.split()[2])
		sysCoorsZList.append(line2.split()[3])
		sysCoorCount += 1
	if sysCoorCount == sysAtomNumbers:
		break

bqCoorsXList2 = []
bqCoorsYList2 = []
bqCoorsZList2 = []

for bqCoorX in bqCoorsXList:
	bqCoorsXList2.append(round(float(bqCoorX), 5))

for bqCoorY in bqCoorsYList:
	bqCoorsYList2.append(round(float(bqCoorY), 5))

for bqCoorZ in bqCoorsZList:
	bqCoorsZList2.append(round(float(bqCoorZ), 5))

bqCoorsXList3 = list(set(bqCoorsXList2))
bqCoorsXList3.sort()
bqCoorsYList3 = list(set(bqCoorsYList2))
bqCoorsYList3.sort()
bqCoorsZList3 = list(set(bqCoorsZList2))
bqCoorsZList3.sort()

print("Processing finished!\n")

print("Choose shielding tensor for 3D-ICSS map:")
print("      1 - Isoptropic       2 - Anisotropy")
print("      3 - XX component     4 - YX component     5 - ZX component")
print("      6 - XY component     7 - YY component     8 - ZY component")
print("      9 - XZ component    10 - YZ component    11 - ZZ component")
nicsTensor = input('Please input the No.: ')
tensorType = ''

if nicsTensor == '1':
	mapValue = shieldTensorIso
	tensorType = 'iso'
elif nicsTensor == '2':
	mapValue = shieldTensorAni
	tensorType = 'ani'
elif nicsTensor == '3':
	mapValue = shieldTensorXX
	tensorType = 'xx'
elif nicsTensor == '4':
	mapValue = shieldTensorYX
	tensorType = 'yx'
elif nicsTensor == '5':
	mapValue = shieldTensorZX
	tensorType = 'zx'
elif nicsTensor == '6':
	mapValue = shieldTensorXY
	tensorType = 'xy'
elif nicsTensor == '7':
	mapValue = shieldTensorYY
	tensorType = 'yy'
elif nicsTensor == '8':
	mapValue = shieldTensorZY
	tensorType = 'zy'
elif nicsTensor == '9':
	mapValue = shieldTensorXZ
	tensorType = 'xz'
elif nicsTensor == '10':
	mapValue = shieldTensorYZ
	tensorType = 'yz'
elif nicsTensor == '11':
	mapValue = shieldTensorZZ
	tensorType = 'zz'

icssCubeFile = open(f"{fileName}{tensorType}.cub", 'w')

numCount = 0

icssCubeFile.write("Generated by ICSScsv3D developed by Zhe Wang\n")
icssCubeFile.write(f"Totally {len(mapValue)} grid points\n")

icssCubeFile.write(f" {int(sysAtomNumbers)}  {format(min(bqCoorsXList3) * 1.88973, '.6f')}  {format(min(bqCoorsYList3) * 1.88973, '.6f')}  {format(min(bqCoorsZList3) * 1.88973, '.6f')}\n")
icssCubeFile.write(f" {len(bqCoorsXList3)}    {format((bqCoorsXList3[1] - bqCoorsXList3[0]) * 1.88973, '.6f')}    0.000000    0.000000\n")
icssCubeFile.write(f" {len(bqCoorsYList3)}    0.000000    {format((bqCoorsYList3[1] - bqCoorsYList3[0]) * 1.88973, '.6f')}    0.000000\n")
icssCubeFile.write(f" {len(bqCoorsZList3)}    0.000000    0.000000    {format((bqCoorsZList3[1] - bqCoorsZList3[0]) * 1.88973, '.6f')}\n")

for k in range(sysAtomNumbers):
	icssCubeFile.write(f" {elementNo(sysElemsList[k])}    {format(elementNo(sysElemsList[k]), '.6f')}    ")
	icssCubeFile.write(f" {format(float(sysCoorsXList[k]) * 1.88973, '.6f')}    {format(float(sysCoorsYList[k]) * 1.88973, '.6f')}    {format(float(sysCoorsZList[k]) * 1.88973, '.6f')}\n")

for num in mapValue:
	icssCubeFile.write('%e' % num)
	icssCubeFile.write(' ')
	numCount += 1
	if numCount % 6 == 0:
		icssCubeFile.write('\n')

icssCubeFile.close()

# ========================== Result information ==========================
print("\n*******************************************************************************")
print("")
print("                       The cube file has been exported.")
print("                       Normal termination of ICSScsv3D.")
print("")
print("*******************************************************************************\n")

