#!/usr/bin/env python
'''
__author__ = "Chris Hall"
__copyright__ = "Copyright 2015, Chris Hall"
__credits__ = ["Sander - http://forums.sabnzbd.org/viewtopic.php?t=13268"]
__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Chris Hall"
__email__ = "twitter.com/chall32"
__status__ = "Production"
#
#### PURPOSE #############################################################################################################
#
This script will use https://www.metascan-online.com to scan a directory of files.
It does this by calcuating an MD5 hash (https://en.wikipedia.org/wiki/MD5) and searching for the MD5 hash using
Metascan's public API.

If the file is not found on Metascan's site, is deemed to have a suspect extension (see extlist below) and is smaller
than the maximum file size for uploading to Metascan (see maxfilesize below), the script will upload a copy of the file
for scanning via Metascan's public API.  It will then recheck Metascan for the results of the scan using the file's MD5
hash.

The script is intially meant to be used as SABnzbd postprocessing script.
#
#### REQUIREMNTS, USE, EXAMPLE ###########################################################################################
#
REQUIREMNETS:
A free Metascan Public API key. This can obtained from https://www.metascan-online.com/en/public-api
Once obtained, paste this into myapikey below

USE:
scan-directory-with-metascan.py <Directory to be Scanned>

EXAMPLE:
python scan-directory-with-metascan.py C:\Files
#
##########################################################################################################################
'''
import os
import hashlib
import sys
import urllib2
import time
import json
#
# Initilize counts for final wrapup
cleanfound = 0
unkwnfound = 0
susipfound = 0
virusfound = 0
problemhlp = 0
#
#### VARIABLES ###########################################################################################################
#
extlist = ['.exe','.com','.vbs','.vbe','.js','.jse','.jar','.wsf', # Extensions of suspect files that should be uploaded
           '.wsh','.msc','.msi','.pif','.scr','.hta','.apk','.jpg',# to Metascan (extensions should be dot lowercase)
           '.jpeg']                                                #
maxfilesize = '10000000' 					   # Maximum file size to be uploaded to Metascan (bytes)
myapikey = ''                                                      # Metascan API key
hashlookupurl = 'https://hashlookup.metascan-online.com/v2/hash/'  # Metascan API hash lookup URL
hashresulturl = 'https://metascan-online.com/en/scanresult/file/'  # Metascan API hash/file result URL
fileuploadurl = 'https://scan.metascan-online.com/v2/file'         # Metascan API file scan upload URL
manualhashurl = 'https://www.metascan-online.com/scanresult/hash/' # Metascan manual hash lookup URL
secondsforscan = '30'                                              # Time to wait for scan of uploaded file (seconds)
#
##########################################################################################################################
# Function to calculate md5 hash of a file
def md5_of_file(fullfilename):
	md5 = hashlib.md5()
	with open(fullfilename,'rb') as f:
	    for chunk in iter(lambda: f.read(8192), b''):
		 md5.update(chunk)
	return md5.hexdigest().upper()
#
# Funtion to post md5 hash of a file to Metascan
def metascan_hash(md5):
        md5url = hashlookupurl + md5
        requestToSeeIfScannedBefore = urllib2.Request(md5url)
        requestToSeeIfScannedBefore.add_header('apikey', myapikey)
        try:
                hashresults = urllib2.urlopen(requestToSeeIfScannedBefore).read().decode("utf-8")
        except:
                print "Problem contacting Metascan.  Please check \n"
                hashresults = ' '
        return hashresults
#
# Funtion to read and log Metascan md5 hash lookup results
def process_hash_lookup(hashlookup):
	if '"scan_all_result_a":"Infected"' in hashlookup:
                print "Virus found in " + file
                hash_response = json.loads(hashresults)
                data_id = hash_response['data_id']
		print "See URL: " + hashresulturl + data_id + "\n"
		newfilename = fullfilename + '__INFECTED'
		os.rename(fullfilename, newfilename)
		global virusfound
		virusfound += 1000
		uploadfile = False
	elif '"scan_all_result_a":"Suspicious"' in hashlookup:
		print "Suspicious file " + file
		hash_response = json.loads(hashresults)
                data_id = hash_response['data_id']
		print "See URL: " + hashresulturl + data_id + "\n"
		newfilename = fullfilename + '__SUSPICIOUS'
		os.rename(fullfilename, newfilename)
		global susipfound
		susipfound += 100
		uploadfile = False
	elif '"scan_all_result_a":"Clean"' in hashlookup:
		print "No Virus found in " + file
                hash_response = json.loads(hashresults)
                data_id = hash_response['data_id']
	 	print "See URL: " + hashresulturl + data_id + "\n"
                global cleanfound
                cleanfound += 10
	 	uploadfile = False
	elif '"Not Found"' in hashlookup:
		print "File not seen before " + file
		print "See URL: " + manualhashurl + md5 + "\n"
	 	global unkwnfound
	 	unkwnfound += 1
	 	uploadfile = False
	 	if extension in extlist:
                        size = os.path.getsize(fullfilename)
                        if size <= maxfilesize:
                                uploadfile = True
        else:
                print "**** Problem Scanning!! **** \n"
                global problemhlp
                problemhlp += 10000
                uploadfile = False
        return uploadfile
#
# Funtion to upload file to Metascan if file extension appears in suspect list (extlist)
def metascan_file(fullfilename):
        print "File is on risky file list.  Uploading copy to Metascan for definitive analysis \n"
        contents = open(fullfilename).read()
        request = urllib2.Request(fileuploadurl, contents)
        request.add_header('apikey', myapikey)
        request.add_header('filename', file)
        try:
                response = urllib2.urlopen(request).read().decode("utf-8")
                decoded_response = json.loads(response)
                print "File uploaded. Waiting " + secondsforscan + " seconds . . . \n"
                time.sleep(float(secondsforscan))
        except:
                print "Problem contacting Metascan.  Please check \n"
#
#### MAIN #################################################################################################################
# Check launch parameters. Launch with valid directory name
if len(sys.argv) < 2:
        sys.exit('Usage: %s directory-name' % sys.argv[0])
dirname = sys.argv[1]
if not os.path.exists(dirname):
        sys.exit('ERROR: Directory not found' % sys.argv[1])
# Main Loop
for root, dirs, files in os.walk(dirname):
        for file in files:
                extension = os.path.splitext(file)[1].lower()
                fullfilename = os.path.join(root, file)
                md5 = md5_of_file(fullfilename)
                hashresults = metascan_hash(md5)
                uploadfile = process_hash_lookup(hashresults)
                if uploadfile:
                   metascan_file(fullfilename)
                   hashresults = metascan_hash(md5)
                   process_hash_lookup(hashresults)
# Final wrapup for SABnzbd WebGUI
finalwrapup = ["cleanfound","unkwnfound","susipfound","virusfound","problemhlp"]
finalscore = max(finalwrapup, key = locals().get)
if finalscore == "virusfound":
	print "**** VIRUS FOUND!! ****"
elif finalscore == "susipfound":
        print "**** SUSPICIOUS FILE!! ****"
elif finalscore == "unkwnfound":
        print "File(s) not known to Metascan"
elif finalscore == "cleanfound":
        print "All OK - no virus found"
elif finalscore == "problemhlp":
        print "**** Problem Scanning!! ****"
else:
        print "**** Something very wrong!! ****"
