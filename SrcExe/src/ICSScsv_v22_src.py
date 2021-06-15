# ICSScsv v2.2 2021-05-24
# Extract magnetic shielding tensor from ICSS calcultion output
# Written by Zhe Wang, Hiroshima university
# Catch me with wongzit@yahoo.co.jp
# Personal webpage: https://www.wangzhe95.net

# Program information section
print("*******************************************************************************")
print("*                                                                             *")
print("*                                I C S S c s v                                *")
print("*                                                                             *")
print("*     =================== Version 2.2 for Source Code ===================     *")
#print("*     ====================== Version 2.2 for macOS ======================     *")
#print("*     ====================== Version 2.2 for Linux ======================     *")
#print("*     ================ Version 2.2 for Microsoft Windows ================     *")
print("*                           Last update: 2021-05-24                           *")
print("*                                                                             *")
print("*      Extract magnetic shielding tensor from ICSS output file, developed     *")
print("*    by Zhe Wang. Online document is available from GitHub.                   *")
print("*                                     (https://github.com/wongzit/ICSScsv)    *")
print("*                                                                             *")
print("*                             -- Catch me with --                             *")
print("*                         E-mail  wongzit@yahoo.co.jp                         *")
print("*                       Homepage  https://www.wangzhe95.net                   *")
print("*                                                                             *")
print("*******************************************************************************")
print("\nPRESS Ctrl+c to exit the program.\n")

# ========================== Read original output file ==========================
print("Please specify the Gaussian output file path:")

# For Unix/Linux OS
fileName = input("(e.g.: /ICSScsv/example/benzene.log)\n")
if fileName.strip()[0] == '\'' and fileName.strip()[-1] == '\'':
    fileName = fileName.strip()[1:-1]

# For Microsoft Windows
#fileName = input("(e.g.: C:\\ICSScsv\\example\\benzene.log\n")
#fileName = input("(e.g.: C:\\CSIgen\\example\\DR3b_CS2021.log)\n")
#if fileName.strip()[0] == '\"' and fileName.strip()[-1] == '\"':
with open(fileName.strip(), 'r') as originalOutput:
    outputLines = originalOutput.readlines()

print("\nGaussian output read!")

# ========================== Original output file process section ==========================
# Read Bq coordinates and shielding tensor
coorBq = []
shielTensor = []

for outputLine in outputLines:
	if ' Bq    ' in outputLine and outputLine.count('.') == 3:
		coorBq.append(outputLine.rstrip())
	elif 'Isotropic =' in outputLine:
		shielTensor.append(outputLine.rstrip())
	elif ('XX=  ' in outputLine) and ('YX=  ' in outputLine) and ('ZX=  ' in outputLine):
		shielTensor.append(outputLine.rstrip())
	elif ('XY=  ' in outputLine) and ('YY=  ' in outputLine) and ('ZY=  ' in outputLine):
		shielTensor.append(outputLine.rstrip())
	elif ('XZ=  ' in outputLine) and ('YZ=  ' in outputLine) and ('ZZ=  ' in outputLine):
		shielTensor.append(outputLine.rstrip())

x_all = []
y_all = []
z_all = []

for atomNum in range(len(coorBq)):
	x_all.append(float(coorBq[atomNum].split()[1]))
	y_all.append(float(coorBq[atomNum].split()[2]))
	z_all.append(float(coorBq[atomNum].split()[3]))

x_set = sorted(set(x_all))
y_set = sorted(set(y_all))
z_set = sorted(set(z_all))

x_max, x_min = max(x_set), min(x_set)
y_max, y_min = max(y_set), min(y_set)
z_max, z_min = max(z_set), min(z_set)

# Check plane
planeFlag = 0

if len(x_set) == 1:
	planeFlag = 3
	y_step = y_set[1] - y_set[0]
	z_step = z_set[1] - z_set[0]
	print(f"ICSS will be mapped on YZ plane in Y[{y_min} {y_max}, {round(y_step, 2)}], Z[{z_min} {z_max}, {round(z_step, 2)}].\n")
elif len(y_set) == 1:
	planeFlag = 2
	x_step = x_set[1] - x_set[0]
	z_step = z_set[1] - z_set[0]
	print(f"ICSS will be mapped on XZ plane in X[{x_min} {x_max}, {round(x_step, 2)}], Z[{z_min} {z_max}, {round(z_step, 2)}].\n")
elif len(z_set) == 1:
	planeFlag = 1
	x_step = x_set[1] - x_set[0]
	y_step = y_set[1] - y_set[0]
	print(f"ICSS will be mapped on XY plane in X[{x_min} {x_max}, {round(x_step, 2)}], Y[{y_min} {y_max}, {round(y_step, 2)}].\n")

# Number of target and ghost atoms
totalNum = int(len(shielTensor) / 4)
tarMolNum = int(totalNum - len(coorBq))

# ========================== Shielding tensor saving section ==========================
# For reading isotropic case
isotropicValue = []
for isotropicLine in shielTensor:
	if 'Isotropic =' in isotropicLine:
		isotropicValue.append(- float(isotropicLine.split()[4]))
del isotropicValue[:tarMolNum]

# For reading anisotropy case
anisotropyValue = []
for anisotropyLine in shielTensor:
	if 'Anisotropy =' in anisotropyLine:
		anisotropyValue.append(- float(anisotropyLine.split()[7]))
del anisotropyValue[:tarMolNum]

# For reading XX, YX, ZX tensor
xxValue = []
yxValue = []
zxValue = []
for xxLine in shielTensor:
	if 'XX=' in xxLine:
		xxValue.append(- float(xxLine.split()[1]))
		yxValue.append(- float(xxLine.split()[3]))
		zxValue.append(- float(xxLine.split()[5]))

del xxValue[:tarMolNum]
del yxValue[:tarMolNum]
del zxValue[:tarMolNum]

# For reading XY, YY, ZY tensor
xyValue = []
yyValue = []
zyValue = []
for yyLine in shielTensor:
	if 'YY=' in yyLine:
		xyValue.append(- float(yyLine.split()[1]))
		yyValue.append(- float(yyLine.split()[3]))
		zyValue.append(- float(yyLine.split()[5]))

del xyValue[:tarMolNum]
del yyValue[:tarMolNum]
del zyValue[:tarMolNum]

# For reading XZ, YZ, ZZ tensor
xzValue = []
yzValue = []
zzValue = []
for zzLine in shielTensor:
	if 'ZZ=' in zzLine:
		xzValue.append(- float(zzLine.split()[1]))
		yzValue.append(- float(zzLine.split()[3]))
		zzValue.append(- float(zzLine.split()[5]))

del xzValue[:tarMolNum]
del yzValue[:tarMolNum]
del zzValue[:tarMolNum]

# ========================== User input of tensor component ==========================
print("Choose shielding tensor for ICSS map:")
print("      1 - Isoptropic       2 - Anisotropy")
print("      3 - XX component     4 - YX component     5 - ZX component")
print("      6 - XY component     7 - YY component     8 - ZY component")
print("      9 - XZ component    10 - YZ component    11 - ZZ component")
nicsTensor = input('Please input the No.: ')
tensorType = ''

if nicsTensor == '1':
	mapValue = isotropicValue
	tensorType = 'iso'
elif nicsTensor == '2':
	mapValue = anisotropyValue
	tensorType = 'ani'
elif nicsTensor == '3':
	mapValue = xxValue
	tensorType = 'xx'
elif nicsTensor == '4':
	mapValue = yxValue
	tensorType = 'yx'
elif nicsTensor == '5':
	mapValue = zxValue
	tensorType = 'zx'
elif nicsTensor == '6':
	mapValue = xyValue
	tensorType = 'xy'
elif nicsTensor == '7':
	mapValue = yyValue
	tensorType = 'yy'
elif nicsTensor == '8':
	mapValue = zyValue
	tensorType = 'zy'
elif nicsTensor == '9':
	mapValue = xzValue
	tensorType = 'xz'
elif nicsTensor == '10':
	mapValue = yzValue
	tensorType = 'yz'
elif nicsTensor == '11':
	mapValue = zzValue
	tensorType = 'zz'

# ========================== Output writting section ==========================
icssOutput = open(f"{fileName.strip()[:-4]}_ICSS_output_{tensorType}.csv", 'w')

# General information
icssOutput.write(f"# Data from {fileName.strip()}.\n")
icssOutput.write(f"# Shielding tensor data from {tensorType.upper()} component.\n")
icssOutput.write("# Processed with ICSScsv.\n")
icssOutput.write("# Author: Zhe Wang\n")
icssOutput.write("# Homepage: https://www.wangzhe95.net/program-icsscsv\n\n\n")

# For ICSS map
if planeFlag == 1:
	icssOutput.write("XY,")

	for x_axis in x_set:
		icssOutput.write(f"{x_axis},")
	icssOutput.write("\n")

	y_count = 0
	for n_y in range(len(y_set)):
		if y_count < len(y_set):
			icssOutput.write(f"{y_set[y_count]},")
		for n_x in range(len(x_set)):
			icssOutput.write(f"{mapValue[n_y + len(y_set) * n_x]},")
		y_count += 1
		icssOutput.write("\n")

elif planeFlag == 2:
	icssOutput.write("XZ,")

	for x_axis in x_set:
		icssOutput.write(f"{x_axis},")
	icssOutput.write("\n")

	z_count = 0
	for n_z in range(len(z_set)):
		if z_count < len(z_set):
			icssOutput.write(f"{z_set[z_count]},")
		for n_x in range(len(x_set)):
			icssOutput.write(f"{mapValue[n_z + len(z_set) * n_x]},")
		z_count += 1
		icssOutput.write("\n")

elif planeFlag == 3:
	icssOutput.write("YZ,")

	for y_axis in y_set:
		icssOutput.write(f"{y_axis},")
	icssOutput.write("\n")

	z_count = 0
	for n_z in range(len(z_set)):
		if z_count < len(z_set):
			icssOutput.write(f"{z_set[z_count]},")
		for n_y in range(len(y_set)):
			icssOutput.write(f"{mapValue[n_z + len(z_set) * n_y]},")
		z_count += 1
		icssOutput.write("\n")

icssOutput.close()

# ========================== Result information ==========================
print("\n*******************************************************************************")
print("")
print("                     CSV data file is successfully saved.")
print("                        Normal termination of ICSScsv.")
print("")
print("*******************************************************************************\n")

