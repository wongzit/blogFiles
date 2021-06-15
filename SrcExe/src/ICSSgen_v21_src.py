# ICSSgen v2.1, 2021-05-21
# 2D-ICSS input file generator powered by Python 3.9
# Written by Zhe Wang, Hiroshima university
# Catch me with wongzit@yahoo.co.jp
# Personal webpage: https://www.wangzhe95.net

import random

# Program information section
print("*******************************************************************************")
print("*                                                                             *")
print("*                                I C S S g e n                                *")
print("*                                                                             *")
print("*     =================== Version 2.1 for Source Code ===================     *")
#print("*     ====================== Version 2.1 for macOS ======================     *")
#print("*     ====================== Version 2.1 for Linux ======================     *")
#print("*     ================ Version 2.1 for Microsoft Windows ================     *")
print("*                           Last update: 2021-05-21                           *")
print("*                                                                             *")
print("*      ICSS input file generator, developed by Zhe Wang. Online document      *")
print("*    is available from GitHub (https://github.com/wongzit/ICSSgen).           *")
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
fileName = input("(e.g.: /ICSSgen/example/benzene.gjf)\n")
if fileName.strip()[0] == '\'' and fileName.strip()[-1] == '\'':
    fileName = fileName.strip()[1:-1]

# For Microsift Windows
#fileName = input("(e.g.: C:\\ICSSgen\\example\\benzene.gjf)\n")
#if fileName.strip()[0] == '\"' and fileName.strip()[-1] == '\"':
#    fileName = fileName.strip()[1:-1]

with open(fileName.strip(), 'r') as originalInput:
    inputLines = originalInput.readlines()

# ========================== Working parameters ==========================
# Specify the map plane
plane = input("\nPlease specify the plane for ICSS map (XY, XZ, YZ):\n")
plane = plane.lower()

while plane != 'xy' and plane != 'xz' and plane != 'yz':
    print("\nInput error, please input again.\n")
    plane = input("Please specify the plane for ICSS map (XY, XZ, YZ):\n")
    plane = plane.lower()

# Checking which plane will be used for ICSS map
if plane == 'xy':
    planeFlag = 1
elif plane == 'xz':
    planeFlag = 2
else:
    planeFlag = 3

# Specify the altitude over the plane
while True:
    try:
        altitude = float(input("\nPlease input the altitude over the plane (in angstrom):\n"))
        break
    except ValueError:
        print("\nInput error, please input a number!")
        continue

# Specify the mapping range
if planeFlag == 1:
    z = altitude
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
    print(f"\n2D-ICSS({plane.upper()},{altitude}) map in [X: {x_min} to {x_max}, Y: {y_min} to {y_max}].\n")

elif planeFlag == 2:
    y = altitude
    while True:
        try:
            x_min, x_max = input("\nPlease specify the range of X axis (in angstrom, e.g., -10 10):\n").split()
            x_min = float(x_min)
            x_max = float(x_max)
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
    print(f"\n2D-ICSS({plane.upper()},{altitude}) map in [X: {x_min} to {x_max}, Z: {z_min} to {z_max}].\n")

else:
    x = altitude
    while True:
        try:
            y_min, y_max = input("\nPlease specify the range of Y axis (in angstrom, e.g., -10 10):\n").split()
            y_min = float(y_min)
            y_max = float(y_max)
            break
        except ValueError:
            print("\nInput error, please input 2 numbers:")
            continue
    while True:
        try:
            z_min, z_max = input("\nPlease specify the range of Z axis (in angstrom, e.g., -8 8):\n").split()
            z_min = float(z_min)
            z_max = float(z_max)
            break
        except ValueError:
            print("\nInput error, please input 2 numbers:")
            continue
    print(f"\n2D-ICSS({plane.upper()},{altitude}) map in [Y: {y_min} to {y_max}, Z: {z_min} to {z_max}].\n")

# Specify grid
print("Please specify the grid quality (value smaller than 0.25 is recommended):")
userGrid = input("(press Enter to use default value 0.2)\n")
if userGrid:
    grid = float(userGrid)
    if grid < 0:
    	grid = 0 - grid
    elif grid == 0:
    	print("Input error, default grid value 0.2 will be used.\n")
    	grid = 0.2
else:
    grid = 0.2
print(f"ICSSgen will use grid quality of {grid}.\n")

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

icssInput = open(f"{fileName.strip()[:-4]}_ICSS_{plane.upper()}_{int(altitude)}.gjf", "w")

for route in routeLine:
    icssInput.write(route)

icssInput.write(f"\n{fileName.strip()[:-4]}_ICSS_{plane.upper()}_{int(altitude)}//Created_by_ICSSgen\n\n")
icssInput.write(chargeSpin)

for i in range(len(coordinatesLine)):
    icssInput.write(coordinatesLine[i])

# Coordinates of Bq atoms
if planeFlag == 1:
    x_position = x_min
    bqFlag = 0     # Total Bq atom: 10*(max-min)+1
    while x_position <= (x_max + 0.5 * grid):
        y_position = y_min
        while y_position <= (y_max + 0.5 * grid):
            icssInput.write(f" Bq      {round(x_position, 2)}      {round(y_position, 2)}      {round(z, 2)}\n")
            bqFlag += 1
            y_position += grid
        x_position += grid
    for bqNumber in list(range(1, bqFlag + len(coordinatesLine) + 1)):
        icssInput.write(f"\n{bqNumber}")

elif planeFlag == 2:
    x_position = x_min
    bqFlag = 0
    while x_position <= (x_max + 0.5 * grid):
        z_position = z_min
        while z_position <= (z_max + 0.5 * grid):
            icssInput.write(f" Bq      {round(x_position, 2)}      {round(y, 2)}      {round(z_position, 2)}\n")
            bqFlag += 1
            z_position += grid
        x_position += grid
    for bqNumber in list(range(1, bqFlag + len(coordinatesLine) + 1)):
        icssInput.write(f"\n{bqNumber}")

else:
    y_position = y_min
    bqFlag = 0
    while y_position <= (y_max + 0.5 * grid):
        z_position = z_min
        while z_position <= (z_max + 0.5 * grid):
            icssInput.write(f" Bq      {round(x, 2)}      {round(y_position, 2)}      {round(z_position, 2)}\n")
            bqFlag += 1
            z_position += grid
        y_position += grid
    for bqNumber in list(range(1, bqFlag + len(coordinatesLine) + 1)):
        icssInput.write(f"\n{bqNumber}")

icssInput.write("\n\n")
icssInput.close()

# ========================== Result information ==========================
print("\n*******************************************************************************")
print("")
print("                     Input file is successfully generated.")
print("                        Normal termination of ICSSgen.")
print("")
print("*******************************************************************************\n")

