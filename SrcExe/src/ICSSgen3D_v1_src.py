# ICSSgen3D v1.0, 2021-06-06
# 3D version of ICSSgen
# 3D-ICSS input file generator powered by Python 3.9
# Written by Zhe Wang, Hiroshima university
# Catch me with wongzit@yahoo.co.jp
# Personal webpage: https://www.wangzhe95.net

# Program information section
print("*******************************************************************************")
print("*                                                                             *")
print("*                              I C S S g e n 3 D                              *")
print("*                                                                             *")
print("*     =================== Version 1.0 for Source Code ===================     *")
# Choose platform (for packaging)
#print("*     ====================== Version 1.0 for macOS ======================     *")
#print("*     ====================== Version 1.0 for Linux ======================     *")
#print("*     ================ Version 1.0 for Microsoft Windows ================     *")
print("*                           Last update: 2021-06-06                           *")
print("*                                                                             *")
print("*     3D ICSS input file generator, developed by Zhe Wang. Online document    *")
print("*    is available from GitHub (https://github.com/wongzit/ICSSgen3D).         *")
print("*                                                                             *")
print("*                             -- Catch me with --                             *")
print("*                         E-mail  wongzit@yahoo.co.jp                         *")
print("*                       Homepage  https://www.wangzhe95.net                   *")
print("*                                                                             *")
print("*******************************************************************************")
print("\nPRESS Ctrl+c to exit the program.\n")

# ========================== Read original input file ==========================
print("Please specify the original input file path:")

# For Unix/Linux OS
fileName = input("(e.g.: /ICSSgen3D/example/methylazulene.gjf)\n")
if fileName.strip()[0] == '\'' and fileName.strip()[-1] == '\'':
    fileName = fileName.strip()[1:-1]

# For Microsift Windows
#fileName = input("(e.g.: C:\\ICSSgen3D\\example\\methylazulene.gjf)\n")
#if fileName.strip()[0] == '\"' and fileName.strip()[-1] == '\"':
#    fileName = fileName.strip()[1:-1]

with open(fileName.strip(), 'r') as originalInput:
    inputLines = originalInput.readlines()

# Specify the mapping range
while True:
    try:
        x_min, x_max = input("\nPlease specify the range of X axis (in angstrom, e.g., -10 10):\n").split()
        x_min = float(x_min)
        x_max = float(x_max)
        break
    except ValueError:
        print("\nInput error, please input 2 numbers:")
        continue

while True:
    try:
        y_min, y_max = input("\nPlease specify the range of Y axis (in angstrom, e.g., -8 8):\n").split()
        y_min = float(y_min)
        y_max = float(y_max)
        break
    except ValueError:
        print("\nInput error, please input 2 numbers!")
        continue

while True:
    try:
        z_min, z_max = input("\nPlease specify the range of Z axis (in angstrom, e.g., -8 8):\n").split()
        z_min = float(z_min)
        z_max = float(z_max)
        break
    except ValueError:
        print("\nInput error, please input 2 numbers!")
        continue

print(f"\n3D-ICSS map in [X: {x_min} to {x_max}, Y: {y_min} to {y_max}, Z: {z_min} to {z_max}].\n")

# Specify grid
print("Please specify the grid quality:")
userGrid = input("(press Enter to use default value 0.25)\n")
if userGrid:
    grid = float(userGrid)
    if grid < 0:
    	grid = 0 - grid
    elif grid == 0:
    	print("Input error, default grid value 0.25 will be used.\n")
    	grid = 0.25
else:
    grid = 0.25
print(f"ICSSgen3D will use grid quality of {grid}.\n")

allBqCoors = []
oneBqCoor =[]

x_position = x_min
while x_position <= (x_max + 0.5 * grid):
    y_position = y_min
    while y_position <= (y_max + 0.5 * grid):
        z_position = z_min
        while z_position <= (z_max + 0.5 * grid):
            oneBqCoor = [format(x_position, '.6f'), format(y_position, '.6f'), format(z_position, '.6f')]
            allBqCoors.append(oneBqCoor)
            oneBqCoor = []
            z_position += grid
        y_position += grid
    x_position += grid

# ========================== ICSS input file section ==========================
# Creat input file for ICSS
routeLine = []
coordinatesLine = []
chargeSpin = ''

for line in inputLines:
    if line[0] == '%':
        routeLine.append(line)
    elif line[0] == '#':
        if 'geom=connectivity' in line.lower():
            routeLine.append(line)
        else:
            routeLine.append(f"{line.rstrip()} geom=connectivity\n")
    elif len(line.split()) == 2 and len(''.join(line.rstrip())) < 6:
        chargeSpin = line
    elif ( line[0].isalpha or line[1].isalpha ) and line.count('.') == 3:
        coordinatesLine.append(f"{line.rstrip()}\n")

fileNumbers = 1

if len(allBqCoors) <= 7000 - len(coordinatesLine):
#    print("yes")
    fileNumbers = 1
elif len(allBqCoors) % 7000 == 0:
    fileNumbers = int(len(allBqCoors) / 7000)
else:
    fileNumbers = int(len(allBqCoors) / 7000 + 1)

icssInput = open(f"{fileName.strip()[:-4]}_3DICSS_0001.gjf", "w")

for route in routeLine:
    icssInput.write(route)

icssInput.write(f"\n{fileName.strip()[:-4]}_3DICSS//Created_by_ICSSgen3D\n\n")
icssInput.write(chargeSpin)

for coorLine in coordinatesLine:
    icssInput.write(coorLine)

if fileNumbers == 1:
    for i in range(len(allBqCoors)):
        icssInput.write(f" Bq      {allBqCoors[i][0]}      {allBqCoors[i][1]}      {allBqCoors[i][2]}\n")
    for bqNumber1 in list(range(1, len(coordinatesLine) + len(allBqCoors) + 1)):
        icssInput.write(f"\n{bqNumber1}")
else:
    bqCounter1 = 0
    for i in range(7000):
        icssInput.write(f" Bq      {allBqCoors[i][0]}      {allBqCoors[i][1]}      {allBqCoors[i][2]}\n")
        bqCounter1 += 1
    for bqNumber1 in list(range(7000 + len(coordinatesLine))):
        icssInput.write(f"\n{bqNumber1 + 1}")

icssInput.write("\n\n")
print(f"{fileName.strip()[:-4]}_3DICSS_0001.gjf has been saved.")
icssInput.close()

routeLine[-1] = f"{routeLine[-1].rstrip()} guess=read\n"

if fileNumbers > 1:
    for fileNumber in range(2, fileNumbers + 1):
        fileNameNumber = '%04d' % fileNumber
        icssInput = open(f"{fileName.strip()[:-4]}_3DICSS_{fileNameNumber}.gjf", "w")

        for route in routeLine:
            icssInput.write(route)

        icssInput.write(f"\n{fileName.strip()[:-4]}_3DICSS//Created_by_ICSSgen3D\n\n")
        icssInput.write(chargeSpin)

        for coorLine in coordinatesLine:
            icssInput.write(coorLine)

        bqCounter2 = 0
        while (bqCounter2 < 7000) and bqCounter1 < len(allBqCoors):
            icssInput.write(f" Bq      {allBqCoors[bqCounter1][0]}      {allBqCoors[bqCounter1][1]}      {allBqCoors[bqCounter1][2]}\n")
            bqCounter1 += 1
            bqCounter2 += 1

        for bqNumber2 in list(range(1, len(coordinatesLine) + bqCounter2 + 1)):
            icssInput.write(f"\n{bqNumber2}")

        icssInput.write("\n\n")
        print(f"{fileName.strip()[:-4]}_3DICSS_{fileNameNumber}.gjf has been saved.")
        icssInput.close()

# ========================== Result information ==========================
print("\n*******************************************************************************")
print("")
print("                    Input files are successfully generated.")
print("                 Please submit these input files to Gaussian,")
print("                      and save the output as .log files.")
print("")
print("                       Normal termination of ICSSgen3D.")
print("")
print("*******************************************************************************\n")

