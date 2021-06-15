# NICSgen v1.2, 2021-04-28
# NICS input file generator powered by Python 3.9
# Written by Zhe Wang, Hiroshima university
# Catch me with wongzit@yahoo.co.jp
# Personal webpage: https://www.wangzhe95.net

# Program information section
print("*******************************************************************************")
print("*                                                                             *")
print("*     $$$      $$  $$$     $$$$      $$$$                                     *")
print("*     $$ $     $$   $    $$    $$  $$    $$                                   *")
print("*     $$  $    $$   $   $$         $$                                         *")
print("*     $$   $   $$   $   $$           $$$$      $$$$      $$$$    $$$$$$$      *")
print("*     $$    $  $$   $   $$               $$  $$    $$  $$    $$  $$    $$     *")
print("*     $$     $ $$   $    $$    $$  $$    $$  $$    $$  $$    $$  $$    $$     *")
print("*     $$      $$$  $$$     $$$$      $$$$      $$$$$$  $$$$$$$   $$    $$     *")
print("*                                                  $$  $$        $$    $$     *")
print("*                                            $$    $$   $$$$$$   $$    $$     *")
print("*                                              $$$$                           *")
print("*                                                                             *")
print("*     =================== Version 1.2 for Source Code ===================     *")
print("*                           Last update: 2021-04-28                           *")
print("*                                                                             *")
print("*      A NICS input file generator, developed by Zhe Wang. Online document    *")
print("*    is available from GitHub (https://github.com/wongzit/NICSgen).           *")
print("*                                                                             *")
print("*                             -- Catch me with --                             *")
print("*                         E-mail  wongzit@yahoo.co.jp                         *")
print("*               Personal webpage  https://www.wangzhe95.net                   *")
print("*                                                                             *")
print("*******************************************************************************")
print("\nPRESS Ctrl+c to exit the program.\n")

continueFlag = 'y'

# ========================== Read original input file ==========================
print("Please specify the original input file path:")

# For Unix/Linux OS
fileName = input("(eg.: /NICSgen/example/biphenyl.gjf)\n")
if fileName.strip()[0] == '\'' and fileName.strip()[-1] == '\'':
    fileName = fileName[1:-2]

# For Microsift Windows
#fileName = input("(eg.: C:\\NICSgen\\example\\biphenyl.gjf)\n")

with open(fileName.strip(), 'r') as inputFile:
	inputLines = inputFile.readlines()

# ========================== Input file section ==========================
# Creat input file for ICSS
routeLine = []
coordinatesLine = []
chargeSpin = ''

for line in inputLines:

    if line[0] == '%':
        routeLine.append(line)

    elif line[0] == '#':
        routeLine.append(line)

    elif len(line.split()) == 2 and len(''.join(line.rstrip())) < 6:
        chargeSpin = line

    elif ( line[0].isalpha or line[1].isalpha ) and line.count('.') == 3:
        coordinatesLine.append(f"{line.rstrip()}\n")

nicsInput = open(f"{fileName.strip()[:-4]}_NICS.gjf", "w")

for route in routeLine:
    nicsInput.write(route)

nicsInput.write(f"\nNICSinput//Created_by_NICSgen\n\n")
nicsInput.write(chargeSpin)

for i in range(len(coordinatesLine)):
    nicsInput.write(coordinatesLine[i])

while continueFlag == 'y':

# Calculate the coordinates of Bq(0)
    userX = []
    userY = []
    userZ = []

    userAtomsInput = input("\nPlease specify the target atoms number:\n")
    userAtomsNumber = []

    userAltitudeInput = input("\nPlease specify the altitude n of NICS(n):\n")
    userAltitude = float(userAltitudeInput)

    for userAtomInput in userAtomsInput.split():
    	userAtomsNumber.append(int(userAtomInput))

    for userAtomNumber in userAtomsNumber:
    	userX.append(float(coordinatesLine[userAtomNumber - 1].split()[1]))
    	userY.append(float(coordinatesLine[userAtomNumber - 1].split()[2]))
    	userZ.append(float(coordinatesLine[userAtomNumber - 1].split()[3]))

    allX = 0.0000000
    allY = 0.0000000
    allZ = 0.0000000

    for x in userX:
    	allX += x

    for y in userY:
    	allY += y

    for z in userZ:
    	allZ += z

    bqZeroCenterX = allX / float(len(userAtomsNumber))
    bqZeroCenterY = allY / float(len(userAtomsNumber))
    bqZeroCenterZ = allZ / float(len(userAtomsNumber))

    nicsInput.write(f" Bq                 {'{:11f}'.format(bqZeroCenterX)}    {'{:11f}'.format(bqZeroCenterY)}    {'{:11f}'.format(bqZeroCenterZ)}\n")

    if userAltitude != 0.00000:
        para_a = (userY[1] - userY[0]) * (userZ[2] - userZ[0]) - (userY[2] - userY[0]) * (userZ[1] - userZ[0])
        para_b = (userZ[1] - userZ[0]) * (userX[2] - userX[0]) - (userZ[2] - userZ[0]) * (userX[1] - userX[0])
        para_c = (userX[1] - userX[0]) * (userY[2] - userY[0]) - (userX[2] - userX[0]) * (userY[1] - userY[0])

        if para_a != 0.00000000:
            para_A3 = 1 + para_b * para_b / para_a / para_a + para_c * para_c / para_a / para_a
            para_B3 = - 2 * bqZeroCenterX - 2 * para_b * para_b * bqZeroCenterX / para_a / para_a - 2 * para_c * para_c * bqZeroCenterX / para_a / para_a
            para_C3 = bqZeroCenterX * bqZeroCenterX + para_b * para_b * bqZeroCenterX * bqZeroCenterX / para_a / para_a + para_c * para_c * bqZeroCenterX * bqZeroCenterX / para_a / para_a - userAltitude * userAltitude
            deltaValue = para_B3 * para_B3 - 4 * para_A3 * para_C3

            if deltaValue != 0:
                bqN1X = (- para_B3 + pow(deltaValue, 1.0/2)) / 2 / para_A3
                bqN2X = (- para_B3 - pow(deltaValue, 1.0/2)) / 2 / para_A3
                bqN1Y = para_b / para_a * (bqN1X - bqZeroCenterX) + bqZeroCenterY
                bqN2Y = para_b / para_a * (bqN2X - bqZeroCenterX) + bqZeroCenterY
                bqN1Z = para_c / para_a * (bqN1X - bqZeroCenterX) + bqZeroCenterZ
                bqN2Z = para_c / para_a * (bqN2X - bqZeroCenterX) + bqZeroCenterZ
                nicsInput.write(f" Bq                 {'{:11f}'.format(bqN1X)}    {'{:11f}'.format(bqN1Y)}    {'{:11f}'.format(bqN1Z)}\n")
                nicsInput.write(f" Bq                 {'{:11f}'.format(bqN2X)}    {'{:11f}'.format(bqN2Y)}    {'{:11f}'.format(bqN2Z)}\n")

            else:
                bqNX = - para_B3 / 2 / para_A3
                bqNY = para_b / para_a * (bqNX - bqZeroCenterX) + bqZeroCenterY
                bqNZ = para_c / para_a * (bqNX - bqZeroCenterX) + bqZeroCenterZ
                nicsInput.write(f" Bq                 {'{:11f}'.format(bqNX)}    {'{:11f}'.format(bqNY)}    {'{:11f}'.format(bqNZ)}\n")
        
        elif userX[0] == userX[1] and userX[1] == userX[2]:
        	nicsInput.write(f" Bq                 {userAltitude}    {'{:11f}'.format(bqZeroCenterY)}    {'{:11f}'.format(bqZeroCenterZ)}\n")
        	nicsInput.write(f" Bq                 {- userAltitude}    {'{:11f}'.format(bqZeroCenterY)}    {'{:11f}'.format(bqZeroCenterZ)}\n")

        elif userY[0] == userY[1] and userY[1] == userY[2]:
        	nicsInput.write(f" Bq                 {'{:11f}'.format(bqZeroCenterX)}    {userAltitude}    {'{:11f}'.format(bqZeroCenterZ)}\n")
        	nicsInput.write(f" Bq                 {'{:11f}'.format(bqZeroCenterX)}    {- userAltitude}    {'{:11f}'.format(bqZeroCenterZ)}\n")

        elif userZ[0] == userZ[1] and userZ[1] == userZ[2]:
        	nicsInput.write(f" Bq                 {'{:11f}'.format(bqZeroCenterX)}    {'{:11f}'.format(bqZeroCenterY)}    {userAltitude}\n")
        	nicsInput.write(f" Bq                 {'{:11f}'.format(bqZeroCenterX)}    {'{:11f}'.format(bqZeroCenterY)}    {- userAltitude}\n")

    continueFlag = input("\nContinue to add other Bq atoms? (y/n):\n")

nicsInput.write("\n\n")
nicsInput.close()

# ========================== Result information ==========================
print("\n*******************************************************************************")
print("")
print("                     Input file is successfully generated.")
print("                        Normal termination of NICSgen.")
print("")
print("*******************************************************************************\n")

