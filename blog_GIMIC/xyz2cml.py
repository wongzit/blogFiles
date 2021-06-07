# xyz2cml v1.0
# Convert .xyz to .cml, powered by Python 3.9
# Last Update: 2021-05-24
# Author: Zhe Wang
# Homepage: https://www.wangzhe95.net/program
# xyz2cml reads mol.xyz file at current dictionary and convert it to mol-bohr.cml

print("*******************************************************************************")
print("*                                                                             *")
print("*                                x y z 2 c m l                                *")
print("*                                                                             *")
print("*     ======================= Convert .xyz to .cml ======================     *")
print("*                           Last update: 2021-05-23                           *")
print("*                                                                             *")
print("*                             -- Catch me with --                             *")
print("*                         E-mail  wongzit@yahoo.co.jp                         *")
print("*                       Homepage  https://www.wangzhe95.net                   *")
print("*                         GitHub  https://github.com/wongzit                  *")
print("*                                                                             *")
print("*******************************************************************************")

print("\nReading geometric information form ./mol.xyz ...")
print("Writting geometric information to ./mol-bohr.cml ...")

with open("mol.xyz", "r") as xyzFile:
	xyzLines = xyzFile.readlines()

atomNumbers = int(xyzLines[0].strip())

def atomArraySection (id, elementType, x3, y3, z3):
	cmlFile.write(f"  <atom id=\"a{id}\" elementType=\"{elementType}\" x3=\"{x3}\" y3=\"{y3}\" z3=\"{z3}\"/>\n")

def bondArraySection (idA, idB):
	cmlFile.write(f"  <bond atomRefs2=\"a{idA} a{idB}\" order=\"1\"/>\n")

cmlFile = open("mol-bohr.cml", "w")

cmlFile.write("<?xml version=\"1.0\"?>\n")
cmlFile.write("<molecule id=\"mol.xyz\" xmlns=\"http://www.xml-cml.org/schema\">\n")

atomCoors = []

for atomNumber in range(2, atomNumbers + 2):
	if xyzLines[atomNumber].strip() != '':
		atomCoors.append(xyzLines[atomNumber].strip())

cmlFile.write(" <atomArray>\n")

xCoors = []
yCoors = []
zCoors = []

for atomNumber2 in range(atomNumbers):
	element = atomCoors[atomNumber2].split()[0]
	xPosition = atomCoors[atomNumber2].split()[1]
	xBohr = format(float(xPosition)/0.529177, '.6f')
	xCoors.append(xBohr)
	yPosition = atomCoors[atomNumber2].split()[2]
	yBohr = format(float(yPosition)/0.529177, '.6f')
	yCoors.append(yBohr)
	zPosition = atomCoors[atomNumber2].split()[3]
	zBohr = format(float(zPosition)/0.529177, '.6f')
	zCoors.append(zBohr)
	atomArraySection(atomNumber2 + 1, element, xBohr, yBohr, zBohr)

cmlFile.write(" </atomArray>\n")

disMatrixs = []

for atomA in range(atomNumbers):
	disMatrix = []
	for atomB in range(atomNumbers):
		if atomA < atomB:
			disABx = float(xCoors[atomA]) - float(xCoors[atomB])
			disABy = float(yCoors[atomA]) - float(yCoors[atomB])
			disABz = float(zCoors[atomA]) - float(zCoors[atomB])
			disAB = pow(disABx * disABx + disABy * disABy + disABz * disABz, 0.5)
			disMatrix.append(disAB)
		else:
			disMatrix.append("none")
	disMatrixs.append(disMatrix)

cmlFile.write(" <bondArray>\n")

for noA in range(atomNumbers):
	for noB in range(atomNumbers):
		if disMatrixs[noA][noB] != 'none' and float(disMatrixs[noA][noB]) < 3.22:
			bondArraySection(noA + 1, noB + 1)

cmlFile.write(" </bondArray>\n")
cmlFile.write("</molecule>\n")
cmlFile.write("\n")

cmlFile.close()

print("\n*******************************************************************************")
print("                       Normal termination of xyz2cml.")
print("*******************************************************************************\n")
