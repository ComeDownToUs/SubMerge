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


#To-dos
- Implement basic SSA reading and writing (i.e. only handle newlines in single line formatting)
- Read in formatting options from json file
- Combine two sets of subtitles into a merged set


#Config Defaults
  event = {
    "title": "Dialogue",
    "Marked": "Marked=0",
    "Start": "00:00:05.00",
    "End": "00:00:00.00",
    "Style": "Default",
    "Name": "NTP",
    "MarginL": "0000",
    "MarginR": "0000",
    "MarginV": "0000",
    "PrimaryEffect": "!Effect",
    "Text": "Placeholder",
    "order": [
      "Marked",
      "Start",
      "End",
      "Style",
      "Name",
      "MarginL",
      "MarginR",
      "MarginV",
      "PrimaryEffect",
      "Text"
    ]}
  style = {
    "title": "Style",
    "Name": "Default",
    "Fontname": "Tahoma",
    "Fontsize": "24",
    "PrimaryColour": "16777215",
    "SecondaryColour": "16777215",
    "TertiaryColour": "16777215",
    "BackColour": "12632256",
    "Bold": "-1",
    "Italic": "0",
    "BorderStyle": "1",
    "Outline": "1",
    "Shadow": "0",
    "Alignment": "2",
    "MarginL": "30",
    "MarginR": "30",
    "MarginV": "10",
    "AlphaLevel": "0",
    "Encoding": "0",
    "order": [
      "Name",
      "Fontname",
      "Fontsize",
      "PrimaryColour",
      "SecondaryColour",
      "TertiaryColour",
      "BackColour",
      "Bold",
      "Italic",
      "BorderStyle",
      "Outline",
      "Shadow",
      "Alignment",
      "MarginL",
      "MarginR",
      "MarginV",
      "AlphaLevel",
      "Encoding"
    ]}
