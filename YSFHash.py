#!/usr/bin/python3

import sys
import time
import cgi, cgitb

# Copyright 2019 Chris Petersen, K9EQ
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Program to take a YSF Reflector name and determine the hash
# Input can either be from the command line or via a cgi-bin call
# Command line:
#	Enter the reflector number and name as the first and second arguments
#		as in hasher.py 21493 "US MNWIS"
# cgi-bin
# 	Input name via the YSFReflectorName and WiresxRoomName variables
#	cgi-bin will be used if there is no command line input
# Result is the reflector number

# Revision history
# 0.1	Initial release
Rev = '0.1'	

if sys.stdin.isatty():  # Running from command line?
	cgibin = False
else:
	cgibin = True
	cgitb.enable() # Enable debugging for cgi-bin

def YSFHash(YSFName): # Function to calculate the hash
	hash = 0
	for c in YSFName:
		hash += c
		hash += (hash << 10)
		hash &= 0xffffffff	# Hash only works on 32 bit integers mask
		hash ^= (hash >> 6)
	# Finalize
	hash += (hash << 3)
	hash &= 0xffffffff	# Mask for 32-bit c integers
	hash ^= (hash >> 11)
	hash += (hash << 15)
	hash &= 0xffffffff
	hash = hash % 100000
	return(hash)

Error = False
htmlText = ""

if (cgibin == True):
	htmlText = "<p>" # Only add new line if running as cgi-bin
	try:
		print("Content-Type: text/html") # Output HTML header
		print()
	except:
		cgi.print_exception()
		Error = True

	form = cgi.FieldStorage()

	if "YSFReflectorName" not in form:
		print("<H1>Error<H1><p>")
		print("Enter YSF Reflector name up to 16 characters<p>")
		Error = True
	
	if "WiresxRoomNumber" not in form:
		print("<H1>Error<H1>")
		print("Enter the desired WiRES-X Room number - 5 digits<p>")
		Error = True
	try:
		RoomName = form.getvalue("YSFReflectorName", "")
	except:
		print("Must provide a YSF Reflector name<p>")
		Error = True
	try:
		DesiredNumber = int(form.getvalue("WiresxRoomNumber", ""))
	except:
		print("Must provide a WiRES-X Room number<p>")
		Error = True
else: # Command line
	try:
		DesiredNumber = int(sys.argv[1])
		RoomName = sys.argv[2]
	except:
		print("Must provide a YSF reflector number and name")

if (DesiredNumber > 99999) ^ (DesiredNumber == 0):
	print("Desired WiRES-X Room number must be between 1 and 99999" + htmlText)
	Error = True
	sys.exit(1)

searchType = 0 # Default value

NumberofResults = 5 # Default

# Start performance timer
if (Error == False):
	start=time.process_time()

# Attempt to match number by adding characters
# Use only printable characters

	testString = " ABCDEFGHIJKLMNOPQRSTUVWXYZ" # Select printable characters here
	if (searchType == 1):
		testString = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" # Select printable characters here
	else:
		if (searchType == 2):
			testString = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz" # Select printable characters here

	RoomName = RoomName[:12] # Truncate Name to 12 characters
	RoomName = '{:16}'.format(RoomName) # Expand Name with spaces to 16 characters
	count = 0
	tests = 0
	finalName = ''
	finalHash = 0
	testName = bytearray(RoomName.encode())
	break_loop = False
	print("YSF Hasher " + Rev + " by K9EQ" + htmlText, flush=True)
	print("Calculating YSF Reflector names for the hash " + str(DesiredNumber) + htmlText, flush=True)
	sys.stdout.flush()
	for c1 in testString:
		for c2 in testString:
			for c3 in testString:
				for c4 in testString:
					tests += 1
					#testName = Name + c1 + c2 + c3 + c4 # Use the last four characters of the name
					testName[12] = ord(c1)
					testName[13] = ord(c2)
					testName[14] = ord(c3)
					testName[15] = ord(c4)
					result = YSFHash(testName)
					if (result == DesiredNumber):
						count += 1
						print("<pre>" + testName.decode() + htmlText + "</pre>")
						finalHash = result
						if (count >= NumberofResults):
							break_loop = True
						if (break_loop == True):
							break
				if (break_loop == True):
					break
			if (break_loop == True):
				break
		if (break_loop == True):
			break

	print("\n" + str(count) + " results found" + htmlText)

	# Stop performance timer
	elapsed = time.process_time() - start
	#print("Elapsed time: " + str(elapsed) + " seconds")
	print("Elapsed time: %6.2f seconds%s" % (elapsed, htmlText))
	print("Number of tests performed: " + str(tests) + htmlText)
	timePerTest = (elapsed*1000)/tests
	print("Time per test (ms): %6.3f%s" % (timePerTest, htmlText))

if (cgibin == True):
	print("<p><H3>Press back on your browser to return to the previous screen</H3>")
# End
