import re
import datetime
import json
from collections import OrderedDict

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

#just storing the file reading process within a function
def read_subtitles(sub_file):
  f = open(sub_file, 'r')
  text = f.read()
  f.close()
  return text

def write_subtitles(sub_file, sub_text):
  f = open(sub_file, 'w')
  f.write(subtext)
  f.close()
  return subtext

def subs_to_time(subs_time):
  hours = int(subs_time[0])
  minutes = int(subs_time[1])
  seconds = int(subs_time[2])
  microsec = int(subs_time[3])*1000#srt is in thousandths of a second
  return datetime.time(hours, minutes, seconds, microsec)

def process_config(config_file):
  data = json.load(open(config_file), object_pairs_hook=OrderedDict)
  print data

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

# process ssa
# formatting from here https://matroska.org/technical/specs/subtitles/ssa.html
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
  print formatted_lines
  return formatted_lines


'''
formats an SSA line from a string into its parts
dialogue additional commas handled
'''
def parse_ssa_line(line, formatting=None):
  '''
    input:
      line =
        "Format: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, PrimaryEffect, Text"
    output:
      parsed_line =
        {
          'type': 'Format',
          'values': [
            'Marked',
            'Start,
            'End',
            'Style',
            'Name',
            'MarginL',
            'MarginR',
            'MarginV',
            'PrimaryEffect',
            'Text'
          ]
        }
  '''
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
  print parsed_line
  return parsed_line

#formats to milliseconds to match srt specs
def format_ssa_time(time_str):
  fmt_time = time_str.replace('.', ':').split(':')
  fmt_time[3]+= "0"
  return subs_to_time(fmt_time)


###---OUTPUT FORMATTING--###

#regular converters, reformats subtitles to a string in the correct format
#write srt
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

#write ssa
def format_ssa(sub_lines):
  '''
  read in the config files and build the first two sections from that
  write mix the config and subtitles parts for writing the dialogues
  in merged case, use inline stylings
  '''
  pass

#write sub


