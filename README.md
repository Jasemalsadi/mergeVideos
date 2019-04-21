# mergeVideos
Merge webm  Videos based on Major version X.something.something
## Prerequisites
```
Python 3
OptionParser
mkvmerge
```
## Install

```bash
$ pip3 install -r requirements.txt
$ sudo apt install mkvtoolnix
```
## Attributes 
```
-s : Path to the Videos folder (without recursively)  with double quoutes 
-p : Destination path to save the folder with double quoutes
```


## Example 
```bash
$ python3 merge_videos.py -s "/Users/Jasem/Desktop/videos" -d "/Users/Jasem/Desktop/merged"
```
Note: Videos that contain different tracks ID won't be merge. Also it doesn't support recursive folders currently. 
