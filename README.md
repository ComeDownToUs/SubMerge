# Setup

Currently this system is only in a testing stage focusing exclusively on the core read/write operations.

These operations are to function as a subtitle converter for initially SRT and SSA subtitle formats, I'll probably include SUB too purely because they're so easy to do.


The next steps are to include a docopt interface in the root director for a fully operating package. As it stands, please use the following commands to test functionality. Currently this has to be ran from outside the directory; I'm going to build a DocOpt CLI in the root so the code actually does someting next

```
  python -m SubMerge.tests.tests_core
  python -m SubMerge.tests.tests_config
  python -m SubMerge.tests.tests_merging
```

# Why...

### SRT?

It's by far the most prevalent subtitle format

### SSA?

Seemingly most commonly used for karaoke subtitling, that gives it something of a safeguard for the formatting dictated within the file being retained by compat (VLC, which I'm using, done this with some other formats I tried)

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
There are two sets of subtitles, the code is large constructed to potentially handle more but I wasn't keeping track of this too much. The first set passed in are the primary set, this means they will be included in their entirety, only subtitles from the second set which match their time breakages will be included.
Several arguments will exist for the purposes of prioritisation and screen space maximising:
- a character limit on the second set of subtitles
- the level of variance in time for the second set of subtitles
- if newlines are included
- if not, what represents where a line break would have been

# To-dos
- Read in formatting options from json file (partially complete)
- Config type validations
- Reduce SSA hardcoding, seems like it's ripe for failure right now
- Log decoupling issues (ideally want merge operations split from subtitle conversion as much as possible, and everything split by format too)
- Switch to python 3.3
- Flag coupling issues (specifically hardcoded values)
- Refactor again once running basic operations


### Future features
- Build a docopt interface
- Build a CLI
- Tweak to work as a basic subtitle conversion library
- SUB format support
