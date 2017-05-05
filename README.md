# Setup

Currently this system is only in a testing stage focusing exclusively on the core read/write operations.
These operations are to function as a subtitle converter for initially SRT and SSA subtitle formats, I'll probably include SUB too purely because they're so easy to do.

```
  python test.py
```

## Why...
### SRT?
It's by far the most prevalent subtitle format
### SSA?
Seemingly most commonly used for karaoke subtitling, it's got something of a safeguard of the formatting dictated within the file being overwritten by a program (VLC, which I'm using, done this with some other formats I tried)
### SUB?
Not yet implemented but it seems like pretty easy bonus functionality


#To-dos
- Implement basic SSA reading and writing (i.e. only handle newlines in single line formatting)
- Read in formatting options from json file
- Create functions to display defaults
- Break general tasks, core operations, srt, ssa and sub into separate files
- Tweak to work as a basic subtitle conversion library
- Implement merging process
- Implement merge styling
- Reassess styling for both subtitles appearing simultaneously on top and bottom of screen

