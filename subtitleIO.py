import re
import datetime

#class
  #dialogue array (line by line)
  #milliseconds {start, end}
  #def inframes(frames)
  #def inseconds

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
    out = "{  " + "\n" +\
      "\t'start': " + str(self.time['start']) + "\n" + \
      "\t'end': " + str(self.time['end']) + "\n" + \
      "\tdialogue:" + str(self.dialogue) + "\n" + \
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

#process ssa
# formatting from here https://matroska.org/technical/specs/subtitles/ssa.html
def process_ssa(sub_text):
  #a blank line represents a next section
  segment_split = re.split('\n\[(.*)\]\n', sub_text)
  #re.split includes the split characters
  formatted_lines = []
  dialogue_lines=segment_split[4].split('\n')
  dialogue_format=dialogue_lines.pop(0).split(',')
  for i in range(len(dialogue_format)):
    dialogue_format[i] = dialogue_format[i].strip()
  #get indexes of relevant format pieces
  start_i = dialogue_format.index("Start")
  end_i = dialogue_format.index("End")
  dialogue_i = dialogue_format.index("Text")
  for subtitle in dialogue_lines:
    #resolve indexes
    fragments = subtitle.split(',')
    if len(fragments)<3:
      continue
    start_time = fragments[start_i].strip().replace('.', ':').split(':')
    end_time = fragments[end_i].strip().replace('.', ':').split(':')
    start_time[3]+="0"
    end_time[3]+="0"
    dialogue = [fragments[dialogue_i]]
    formatted_lines.append(SubLine(dialogue, start_time, end_time))
  print formatted_lines
  return formatted_lines

#process .sub
  #convert frames to seconds
  #split dialogue by '|'


#regular converters, reformats subtitles to a string in the correct format 
#write srt
def format_srt(sub_lines):
  srt_output = ""
  counter = 1
  for entry in sub_lines:
    if counter != 1:
      srt_output += "\n"
    srt_output += str(counter)+"\n" 
    srt_output += entry.time['start'].strftime("%H:%M:%S,%f")[0:12] 
    srt_output += " --> " 
    srt_output += entry.time['end'].strftime("%H:%M:%S,%f")[0:12]
    srt_output += "\n"
    for line in entry.dialogue:
      srt_output += line
      srt_output += "\n"
    counter += 1
  return srt_output
#write ssa

#write sub


