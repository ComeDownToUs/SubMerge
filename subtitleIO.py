import re
import datetime
import json
import warnings

class SubLine:
  def __init__(self, subs, start, end):
    self.dialogue = []
    for x in subs:
      self.dialogue.append(x)
    self.time = {
      'start': start,
      'end': end
    }
  def hms_to_frames(self, frames):
    return frames
  def hms_to_seconds(self):
    return 0
  def __repr__(self):
    out = "{" +\
      " start:" + str(self.time['start']) + \
      ", end:" + str(self.time['end']) + \
      ", dialogue:" + str(self.dialogue) + \
      "}\n"
    return out

def read_full_file(sub_file):
  f = open(sub_file, 'r')
  text = f.read()
  f.close()
  return text
def write_file(sub_file, sub_text):
  f = open(sub_file, 'w')
  f.write(subtext)
  f.close()
  return subtext

#type unspecific, returns datetime object
def subs_to_time(subs_time):
  hours = int(subs_time[0])
  minutes = int(subs_time[1])
  seconds = int(subs_time[2])
  microsec = int(subs_time[3])*1000#srt is in thousandths of a second
  return datetime.time(hours, minutes, seconds, microsec)

#likely needs expansion
def read_json(json_file):
  return json.loads(read_full_file(json_file))

'''
  READING SRT
'''
# <<TODO>> SRT is a fairly simplistic format but there's definitely room for validation and error handling here
def process_srt(sub_text):
  #a blank line represents a next section
  basic_split = sub_text.strip().split('\n\n')
  formatted_lines = []
  for subtitle in basic_split:
    subtitle = subtitle.split('\n')
    times_str = subtitle[1].split('-->')
    time_formatted = []
    for time_str in times_str:
      time_str = time_str.strip().replace(',', ':').split(':')
      time_formatted.append(subs_to_time(time_str))
    dialogue_lines = []
    for dialogue_index in range(2, len(subtitle)):
      dialogue_lines.append(subtitle[dialogue_index])
    formatted_lines.append(SubLine(dialogue_lines, time_formatted[0], time_formatted[1]))
  return formatted_lines

'''
  READING SSA
'''
# formatting from here https://matroska.org/technical/specs/subtitles/ssa.html

#kinda hacky breakdown to find the individual parts, may require an overhaul
def process_ssa(sub_text):
  formatted_lines = []
  #a blank line represents a next section
  segment_split = re.split('\n\[Events\]\n|\n\[V4 Styles\]\n', sub_text)
  dialogue_lines=segment_split[2].split('\n') # <<TODO>> Remove hardcoding for flexibility
  dialogue_format=parse_ssa_line(dialogue_lines.pop(0))
  #get indexes of relevant format pieces
  for subtitle in dialogue_lines:
    #resolve indexes
    if len(subtitle)<3:
      continue
    subtitle = parse_ssa_line(subtitle, dialogue_format['values'])
    start_time = format_ssa_time(subtitle['Start'])
    end_time = format_ssa_time(subtitle['End'])
    dialogue = [subtitle['Text']]
    formatted_lines.append(SubLine(dialogue, start_time, end_time))
  return formatted_lines

#formats an SSA line from a string into its parts, dialogue additional commas handled
# <<TODO>> Error handling for poorly specified files, return an incomplete result?
def parse_ssa_line(line, formatting=None):
  parsed_line = {
    'title': "",
  }
  line = line.split(":", 1)
  parsed_line['title'] = line.pop(0)
  if type(formatting) is list:
    line = line[0].split(',', len(formatting))
    for i in range(len(line)):
      #parsed_line['values'].append(line[i].strip())
      parsed_line[formatting[i]] = line[i].strip()
  else:
    line = line[0].split(',')
    parsed_line['values'] = []
    for entry in line:
      parsed_line['values'].append(entry.strip())
  return parsed_line

#formats to milliseconds to match srt specs
def format_ssa_time(time_str):
  fmt_time = time_str.replace('.', ':').split(':')
  fmt_time[3]+= "0"
  return subs_to_time(fmt_time)


###---OUTPUT FORMATTING--###
#regular converters, reformats subtitles to a string in the correct format

'''
  WRITING SRT
'''
def format_srt(sub_lines):
  srt_output = ""
  counter = 1
  for entry in sub_lines:
    if counter != 1:
      srt_output += "\n"
    srt_output += str(counter)+"\n"
    srt_output += entry.time['start'].strftime("%H:%M:%S,%f")[0:12]#hacky solution to switch from microseconds to milliseconds
    srt_output += " --> "
    srt_output += entry.time['end'].strftime("%H:%M:%S,%f")[0:12]
    srt_output += "\n"
    for line in entry.dialogue:
      srt_output += line
      srt_output += "\n"
    counter += 1
  return srt_output


'''
  WRITING SSA: A long convoluted section
'''

#tests need to be updated when this is expanded upon
def format_ssa(sub_lines):
  ssa_skeleton = get_ssa_format()
  ssa_output = ssa_skeleton[0] + "\n\n[V4 Styles]\n" + ssa_skeleton[1] +"\n\n[Events]\n"+ssa_skeleton[2]['format']+"\n"

  for entry in sub_lines:
    ssa_event = ssa_skeleton[2]['event']
    ssa_event = ssa_event.replace("00:00:00.00", entry.time['start'].strftime("%H:%M:%S.%f")[0:11], 1)
    ssa_event = ssa_event.replace("00:00:00.00", entry.time['end'].strftime("%H:%M:%S.%f")[0:11], 1)
    ssa_output += ssa_event
    for line in entry.dialogue:
      ssa_output += line
      if(len(entry.dialogue)>1):
        ssa_output += "\\n"
    ssa_output+="\n"
  print ssa_output
  return ssa_output

#returns skeletal strings built from config specification to apply time and dialogue to for SSA
def get_ssa_format():
  #<<TODO>> this needs to read in json and validate entries, with default values to fall back upon
  script_info= {
    "title": "<untitled>",
    "Original Script": "<unknown>"
  }
  event = {
    "title": "Dialogue",
    "Marked": "Marked=0",
    "Start": "00:00:00.00",
    "End": "00:00:00.00",
    "Style": "Default",
    "Name": "NTP",
    "MarginL": "0000",
    "MarginR": "0000",
    "MarginV": "0000",
    "PrimaryEffect": "!Effect",
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
  return [ssa_format_title(script_info), ssa_format_style(style), ssa_format_event(event)]

#<<TODO>> style and event violate DRY really
#<<TODO>> very hacky substrings
def ssa_format_title(info):
  return "[Script Info]\nTitle: "+info['title']+"\nOriginal Script: "+info['Original Script']+"\nScriptType: v4.00"
def ssa_format_style(style):
  format_string = "Format: "
  style_string = "Style: "
  for i in style['order']:
    format_string += (i + ", ")
    style_string += (style[i] + ",")
  #return {"format": format_string[:-2], "style": style_string[:-2]}
  return format_string[:-2] +"\n"+style_string[:-1]
def ssa_format_event(event):
  format_string = "Format: "
  event_string = "Dialogue: "
  for i in event['order']:
    format_string += (i + ", ")
    if i in event.keys():
      event_string += (event[i] + ",")
  return {"format": format_string[:-2], "event": event_string}


'''
  WRITING SUB: Pretty simple with a time to frame conversion
'''


