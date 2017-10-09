import datetime

#a standard class to act as an intermediary between formats
class SubLine:
  def __init__(self, subs, start, end):
    self.dialogue = []
    for x in subs:
      self.dialogue.append(x)
    self.time = {
      'start': start,
      'end': end
    }
  def hms_to_frames(self, framerate):
    return framerate
  def hms_to_seconds(self):
    return 0
  def __repr__(self):
    out = "[SUBLINE]=>{" +\
      " start:" + str(self.time['start']) + \
      ", end:" + str(self.time['end']) + \
      ", dialogue:" + str(self.dialogue) + \
      "}\n"
    return out


''' Time Conversion Functions '''

def delay_subtitles(subtitles, delayMilliseconds=0):
  updatedSubtitles = []
  for subline in subtitles:
    start_ms = get_time_in_milliseconds(subline.time.start) - delayMilliseconds
    end_ms = get_time_in_milliseconds(subline.time.start) - delayMilliseconds
    if start_ms < 0 or end_ms < 0:
      continue
    subtitles.time.start = milliseconds_to_datetime(start_ms)
    subtitles.time.end = milliseconds_to_datetime(end_ms)
    updatedSubtitles.append(subtitles)
  return updatedSubtitles

def get_time_in_milliseconds(time_obj):
  return time_obj.hour*60*60*1000 \
    + time_obj.minute*60*1000 \
    + time_obj.microsecond/1000

def milliseconds_to_datetime(milliseconds):
  hours_ms = milliseconds % (60*60*1000)
  minutes_ms = (milliseconds - hours_ms) % (60*1000)
  seconds_ms = (milliseconds - hours_ms - minutes_ms) % (1000)
  hours = hours_ms / (60*60*1000)
  minutes = minutes_ms / (60*1000)
  seconds = seconds_ms / 1000
  microseconds = (milliseconds - hours_ms - minutes_ms - seconds_ms) * 1000
  return datetime.time(hours, minutes, seconds, microseconds)

def subs_to_time(subs_time): #returns datetime object
  hours = int(subs_time[0])
  minutes = int(subs_time[1])
  seconds = int(subs_time[2])
  microsec = int(subs_time[3])*1000 #srt 1/1000s, ssa 1/100s
  return datetime.time(hours, minutes, seconds, microsec)
