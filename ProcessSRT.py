import Subtitling

def process_srt(sub_text):
  basic_split = sub_text.strip().split('\n\n') #blank line between subtitles
  formatted_lines = []
  for subtitle in basic_split:
    subtitle = subtitle.split('\n')
    times_str = subtitle[1].split('-->')
    time_formatted = []
    for time_str in times_str:
      time_str = time_str.strip().replace(',', ':').split(':')
      time_formatted.append(Subtitling.subs_to_time(time_str))
    dialogue_lines = []
    for dialogue_index in range(2, len(subtitle)):
      dialogue_lines.append(subtitle[dialogue_index])
    formatted_lines.append(Subtitling.SubLine(dialogue_lines, time_formatted[0], time_formatted[1]))
  return formatted_lines

# SRT
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
