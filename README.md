# Setup

Currently this system is only in a testing stage focusing exclusively on the core read/write operations.
These operations are to function as a subtitle converter for initially SRT and SSA subtitle formats, I'll probably include SUB too purely because they're so easy to do.

```
  python test.py
```

# Why...
### SRT?
It's by far the most prevalent subtitle format
### SSA?
Seemingly most commonly used for karaoke subtitling, it's got something of a safeguard of the formatting dictated within the file being overwritten by a program (VLC, which I'm using, done this with some other formats I tried)
### SUB?
Not yet implemented but it seems like pretty easy bonus functionality


# Details on processing

## Format Reading/Writing
### SRT
A pretty straightforward format with everything split into individual lines and a blank line used to break between subtitles. Looking at an SRT file and the process_srt function should explain everything that's needed here
SRT can only display one subtitle at a time, so a function is required to merge two strings together when merging two sets of subtitles
### SSA
Formatting comes from here https://matroska.org/technical/specs/subtitles/ssa.html
The code is pretty convoluted but the reading of SSA files focuses exclusively on pulling in the dialogue lines, this utilises two stages of processing, one to strip away the formatting and other data and the other to pull the relevant info from each dialogue line. Another function converts the time to match the datetime standards
SSA, being significantly more modifiable will ideally use a config file with a default style option and another style for the secondary subtitles. As more than one subtitle can be displayed on screen at the same time, I'm aiming to keep each entry separate.

## Merge Process choices
TO BE WRITTEN

#To-dos
- Read in formatting options from json file
- Create functions to display defaults
- Break general tasks, core operations, srt, ssa and sub into separate files
- Tweak to work as a basic subtitle conversion library
- Implement merging process
- Implement merge styling
- Assess possibility for both subtitles appearing simultaneously on top and bottom of screen
- Reduce SSA hardcoding, seems like it's ripe for failure right now
