scan-directory-with-metadefender
================================
Chris Hall - [polarclouds.co.uk] 
Metadefender - [www.metadefender.com]

### What does this script do?
Scan a folder of files using Metadefender's [Public API].
The script is can also be used as [SABnzbd postprocessing script].

**The script performs the following:**

For each file in the folder to be scanned,

1.  Create a MD5 hash of the file
2.  Post the MD5 hash value to Metadefender via the Metadefender public API
3.  Categorise the API return value (categories below)
4.  Report results
5.  If file extension is on the risky file list, upload file to Metadefender via public API for analysis
6.  Wait for file analysis to complete
7.  Re-post the MD5 hash value to Metadefender via the public API
8.  Categorise the API return value (categories below)
9.  Rename file if file is found infected or suspicious
10.  Report results

**Script Return Categories:**

+ _VIRUS FOUND!!_ - Fairly obvious. Metadefender knows that this file is infected with a virus. Infected file's filename is appended with "__INFECTED"
+ _SUSPICIOUS FILE!!_ - Metadefender knows that this file is suspicious. Suspicious file's filename is appended with "__SUSPICIOUS"
+ _All OK - no virus found_ - Metadefender knows that this file is OK. All good
+ _File(s) not known to Metadefender_ - Metadefender has not seen this file before
+ _Problem Scanning!!_ - Something went wrong

See Metadefender's [API definitions] for further information.

### Setting up the Script
1.  Each API call requires a Metadefender Online API key. To obtain your free Metadefender Online API key, follow the instructions at Metadefender's [Public API] page
2.  Enter your API key into your downloaded copy of the script betweeen the quotes into the variable ```myapikey```
3.  Review the ```extlist``` variable.  Add or remove any file extensions to be scanned as required.  Files with extensions matching those in this list will be uploaded to Metadefender for analysis
4.  Save and close the script

### How to Use the Script
Simply:
```python scan-directory-with-metascan.py <path to directory to be scanned>```

For example:
```python scan-directory-with-metascan.py /home/chris/files```

For those running under Linux, dont forget to ```chmod +x scan-directory-with-metascan.py``` to mark the file as an executable first.
### More about Metadefender
See the [Opswat] about Metadefender

### What's New?
***See the [changelog] for what's new in the most recent release.***

### [Click here to download latest version](https://github.com/chall32/scan-directory-with-metascan/blob/master/scan-directory-with-metascan.py?raw=true)

If scan-directory-with-metascan helped you, how about buying me a beer? Use the donate button below. THANK YOU!

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=KT462HRW7XQ3J)

[Opswat]: https://www.opswat.com/metadefender-core
[polarclouds.co.uk]: https://polarclouds.co.uk
[www.metadefender.com]: https://www.metadefender.com
[Public API]: https://www.metadefender.com/public-api#!/about
[API definitions]: https://www.metadefender.com/public-api#!/definitions
[SABnzbd postprocessing script]: http://wiki.sabnzbd.org/user-scripts
[changelog]: https://github.com/chall32/scan-directory-with-metascan/blob/master/ChangeLog.txt
