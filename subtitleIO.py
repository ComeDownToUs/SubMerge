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
  #should split into 3-5 segments
  #segment three contains the events, so it's the one we'll be working with
  formatted_lines = []
  dialogue_lines=segment_split[2].split('\n')
  dialogue_format=dialogue_lines.pop(0)
  #get indexes of relevant format pieces
  for subtitle in dialogue_lines:
    #resolve indexes
    fragments = subtitle.split(',')
  #print str(formatted_lines)
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


