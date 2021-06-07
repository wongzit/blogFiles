# gimicInp v0.2
# GIMIC input file generator, powered by Python 3.9
# Last Update: 2021-06-07
# Author: Zhe Wang
# Homepage: https://www.wangzhe95.net/program
# Set parameters, and gimic.inp file would be generated in current dictionary

print("*******************************************************************************")
print("*                                                                             *")
print("*                               g i m i c I n p                               *")
print("*                                                                             *")
print("*     ==================== GIMIC input file generator ===================     *")
print("*                           Last update: 2021-06-07                           *")
print("*                                                                             *")
print("*                             -- Catch me with --                             *")
print("*                         E-mail  wongzit@yahoo.co.jp                         *")
print("*                       Homepage  https://www.wangzhe95.net                   *")
print("*                         GitHub  https://github.com/wongzit                  *")
print("*                                                                             *")
print("*******************************************************************************")
print("Press Ctrl+C to quit the program.\n")

gimicInp = open("./gimic.inp", 'w')
calc = 'cdens'
basis = './MOL'
xdens = './XDENS'
openshell = 'false'
magnet = '0,0,1'
gridType = 'even'
gridOrigin = '-8.0, -7.0, -6.0'
ivec = '1.0, 0.0, 0.0'
jvec = '0.0, 1.0, 0.0'
lengths = '16.0, 14.0, 12.0'
gridPoint = '50, 50, 50'
spherical = 'off'
diamag = 'on'
paramag = 'on'
acid = 'on'
jmod = 'on'

while True:
	print("======================== Current parameters =======================")
	#print("")
	#print("------------------------- General Section ------------------------")
	print(f"    1 - Calculation type: {calc}")
	print(f"    2 - MOL file path: {basis}")
	print(f"    3 - XDENS file path: {xdens}")
	print(f"    4 - Open-shell calculation: {openshell}")
	print(f"    5 - External magnetic field: {magnet}")
	print("-------------------------- Grid Section --------------------------")
	print(f"    6 - Grid types = {gridType}")
	print(f"    7 - Origin of grid (bottom left cornor): {gridOrigin}")
	print(f"    8 - Direction of vertical basis vector: {ivec}")
	print(f"    9 - Direction of the horizontal basis vector: {jvec}")
	print(f"   10 - Length of each side of the cube: {lengths}")
	print(f"   11 - Number of grid points in each direction: {gridPoint}")
	print(f"   12 - Use spherical Cartesian: {spherical}")
	print(f"   13 - Turn on/off diamagnetic contributions: {diamag}")
	print(f"   14 - Turn on/off paramagnetic contributions: {paramag}")
	print(f"   15 - Turn on/off ACID calculation: {acid}")
	print(f"   16 - Turn on/off the mod(J) integral calculation: {jmod}")
	#print("")
	print("==================================================================")
	paraInp = input("Press ENTER to use current settings, input number to modify the parameters.\n")

	if paraInp == '':
		break
	elif paraInp == '1':
		calc = input("Calculation type (cdens/integral):")
		print("")
	elif paraInp == '2':
		basis = input("MOL file path:")
		print("")
	elif paraInp == '3':
		xdens = input("XDENS file path:")
		print("")
	elif paraInp == '4':
		openshell = input("Open-shell calculation? Input true or false:")
		print("")
	elif paraInp == '5':
		magnet = input("External magnetic field:")
		print("")
	elif paraInp == '6':
		gridType = input("Grid type (even/base/bond):")
		print("")
	elif paraInp == '7':
		gridOrigin = input("Origin of grid (bottom left cornor):")
		print("")
	elif paraInp == '8':
		ivec = input("Direction of vertical basis vector:")
		print("")
	elif paraInp == '9':
		jvec = input("Direction of the horizontal basis vector:")
		print("")
	elif paraInp == '10':
		lengths = input("Length of each side of the cube:")
		print("")
	elif paraInp == '11':
		gridPoint = input("Number of grid points in each direction:")
		print("")
	elif paraInp == '12':
		spherical = input("Use spherical Cartesian (on/off):")
		print("")
	elif paraInp == '13':
		diamag = input("Turn on/off diamagnetic contributions (on/off):")
		print("")
	elif paraInp == '14':
		paramag = input("Turn on/off paramagnetic contributions (on/off):")
		print("")
	elif paraInp == '15':
		acid = input("Turn on/off ACID calculation (on/off):")
		print("")
	elif paraInp == '16':
		jmod = input("Turn on/off the mod(J) integral calculation (on/off):")
		print("")
	else:
		print("Input error, use current settings.\n")
		break

gimicInp.write(f"calc={calc}\n")
gimicInp.write(f"basis=\"{basis}\"\n")
gimicInp.write(f"xdens=\"{xdens}\"\n")
gimicInp.write(f"openshell={openshell}\n")
gimicInp.write(f"magnet=[{magnet}]\n")
gimicInp.write("\n")
gimicInp.write("Grid(base) {\n")
gimicInp.write(f"    type={gridType}\n")
gimicInp.write(f"    origin=[{gridOrigin}]\n")
gimicInp.write(f"    ivec=[{ivec}]\n")
gimicInp.write(f"    jvec=[{jvec}]\n")
gimicInp.write(f"    lengths=[{lengths}]\n")
gimicInp.write(f"    grid_point=[{gridPoint}]\n")
gimicInp.write("}\n")
gimicInp.write("\n")
gimicInp.write("Advanced {\n")
gimicInp.write(f"    spherical={spherical}\n")
gimicInp.write(f"    diamag={diamag}\n")
gimicInp.write(f"    paramag={paramag}\n")
gimicInp.write("}\n")
gimicInp.write("\n")
gimicInp.write("Essential {\n")
gimicInp.write(f"    acid={acid}\n")
gimicInp.write(f"    jomd={jmod}\n")
gimicInp.write("}\n")
gimicInp.write("\n")
gimicInp.close()
