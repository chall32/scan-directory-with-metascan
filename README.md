scan-directory-with-metascan
============================
Chris Hall - [chall32.blogspot.com] 
Metascan - [www.metascan-online.com]

### What does this script do?
Scan a folder of files using Metascan's [Public API].
The script is can also be used as [SABnzbd postprocessing script].

**The script performs the following:**

For each file in the folder to be scanned,

1.  Create a MD5 hash of the file
2.  Post the MD5 hash value to metascan via the Metascan public API
3.  Categorise the API return value (categories below)
4.  Report results
5.  If file extension is on the risky file list, upload file to Metascan via public API for analysis
6.  Wait for file analysis to complete
7.  Re-post the MD5 hash value to Metascan via the public API
8.  Categorise the API return value (categories below)
9.  Rename file if file is found infected or suspicious
10.  Report results

**Script Return Categories:**

+ _VIRUS FOUND!!_ - Fairly obvious. Metascan knows that this file is infected with a virus. Infected file's filename is appended with "__INFECTED"
+ _SUSPICIOUS FILE!!_ - Metascan knows that this file is suspicious. Suspicious file's filename is appended with "__SUSPICIOUS"
+ _All OK - no virus found_ - Metascan knows that this file is OK. All good
+ _File(s) not known to Metascan_ - Metascan has not seen this file before
+ _Problem Scanning!!_ - Something went wrong

See Metascan's [API definitions] for further information.

### Setting up the Script
1.  Each API call requires a Metascan Online API key. To obtain your free Metascan Online API key, follow the instructions at Metascan's [Public API] page
2.  Enter your API key into your downloaded copy of the script betweeen the quotes into the variable ```myapikey```
3.  Review the ```extlist``` variable.  Add or remove any file extensions to be scanned as required.  Files with extensions matching those in this list will be uploaded to Metascan for analysis
4.  Save and close the script

### How to Use the Script
Simply:
```python scan-directory-with-metascan.py <path to directory to be scanned>```

For example:
```python scan-directory-with-metascan.py /home/chris/files```

For those running under Linux, dont forget to ```chmod +x scan-directory-with-metascan.py``` to mark the file as an executable first.
### More about Metascan
[![Metascan Video](http://img.youtube.com/vi/rNqwlpuraaI/0.jpg)](http://www.youtube.com/watch?v=rNqwlpuraaI)
(Click to watch video on YouTube)

### What's New?
***See the [changelog] for what's new in the most recent release.***

### [Click here to download latest version](https://github.com/chall32/scan-directory-with-metascan/blob/master/scan-directory-with-metascan.py?raw=true)

If scan-directory-with-metascan helped you, how about buying me a beer? Use the donate button below. THANK YOU!

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=KT462HRW7XQ3J)


[chall32.blogspot.com]: http://chall32.blogspot.com
[www.metascan-online.com]: https://www.metascan-online.com/en/about
[Public API]: https://www.metascan-online.com/en/public-api
[API definitions]: https://www.metascan-online.com/en/public-api#/definitions
[SABnzbd postprocessing script]: http://wiki.sabnzbd.org/user-scripts
[changelog]: https://github.com/chall32/scan-directory-with-metascan/blob/master/ChangeLog.txt
