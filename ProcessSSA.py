import re
import Subtitling

''' Inputs (converts to an array of SubLine class files) '''

def process_ssa(sub_text):
  formatted_lines = []
  segment_split = re.split('\n\[Events\]\n|\n\[V4 Styles\]\n', sub_text)
  dialogue_lines=segment_split[2].split('\n')
  dialogue_format=parse_ssa_line(dialogue_lines.pop(0))
  #get indexes of relevant format pieces
  for subtitle in dialogue_lines:
    #resolve indexes
    if len(subtitle)<3: # <<TODO>> improve this, arbitrary means of skipping lines with no content
      continue
    subtitle = parse_ssa_line(subtitle, dialogue_format['values'])
    start_time = format_ssa_time(subtitle['Start'])
    end_time = format_ssa_time(subtitle['End'])
    dialogue = [subtitle['Text']]
    formatted_lines.append(Subtitling.SubLine(dialogue, start_time, end_time))
  return formatted_lines

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

def format_ssa_time(time_str):
  fmt_time = time_str.replace('.', ':').split(':')
  fmt_time[3]+= "0"
  return Subtitling.subs_to_time(fmt_time)


''' Outputs '''

def format_ssa(sub_lines, merge=False):
  ssa_skeleton = get_ssa_format()
  ssa_output = ssa_skeleton["info_string"] + "\n\n"
  ssa_output += "[V4 Styles]\n"
  ssa_output += (ssa_skeleton["style_string"] + "\n")
  ssa_output += "[Events]\n"
  ssa_output += (ssa_skeleton["events"]['format'])
  ssa_output += '\n'

  if merge:
    return ssa_output + format_merge_ssa(sub_lines, ssa_skeleton['events']['event_shell'])

  for entry in sub_lines:
    ssa_event = ssa_skeleton['events']['event_shell'][0]
    ssa_event = ssa_event.replace("00:00:00.00", entry.time['start'].strftime("%H:%M:%S.%f")[0:11], 1)
    ssa_event = ssa_event.replace("00:00:00.00", entry.time['end'].strftime("%H:%M:%S.%f")[0:11], 1)
    ssa_output += ssa_event
    for line in entry.dialogue:
      ssa_output += line
      if(len(entry.dialogue)>1):
        ssa_output += "\\n"
    ssa_output+="\n"
  return ssa_output

def format_merge_ssa(sub_lines, event_shells):
  ssa_merge_output = ''
  for entry in sub_lines:
    for index, line in enumerate(entry.dialogue):
      line = line.replace('\n', '\\n')
      if index > 1:
        break
      ssa_event = event_shells[index] + line
      ssa_event = ssa_event.replace("00:00:00.00", entry.time['start'].strftime("%H:%M:%S.%f")[0:11], 1)
      ssa_event = ssa_event.replace("00:00:00.00", entry.time['end'].strftime("%H:%M:%S.%f")[0:11], 1)
      ssa_merge_output += ssa_event
      ssa_merge_output += '\n'
  return ssa_merge_output

#returns skeletal strings built from config specification to apply time and dialogue to for SSA
def get_ssa_format():
  #<<TODO>> this needs to read in json and validate entries, with default values to fall back upon
  #<<TODO>> replace these with ordered lists
  #<<TODO>> provide function to output defaults
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
    "styles": [
      {
        "title": "Style",
        "Name": "Default",
        "Fontname": "Tahoma",
        "Fontsize": "24",
        "PrimaryColour": "16777215",
        "SecondaryColour": "00000000",
        "TertiaryColour": "00000000",
        "BackColour": "00000000",
        "Bold": "0",
        "Italic": "0",
        "BorderStyle": "1",
        "Outline": "1",
        "Shadow": "0",
        "Alignment": "2",
        "MarginL": "30",
        "MarginR": "30",
        "MarginV": "10",
        "AlphaLevel": "0",
        "Encoding": "0"
      },
      {
        "title": "Style",
        "Name": "Secondary",
        "Fontname": "Tahoma",
        "Fontsize": "16",
        "PrimaryColour": "12632256",
        "SecondaryColour": "00000000",
        "TertiaryColour": "00000000",
        "BackColour": "00000000",
        "Bold": "0",
        "Italic": "1",
        "BorderStyle": "1",
        "Outline": "1",
        "Shadow": "0",
        "Alignment": "2",
        "MarginL": "30",
        "MarginR": "30",
        "MarginV": "10",
        "AlphaLevel": "0",
        "Encoding": "0"
      }
    ],
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
    ]
  }
  return {
    "info_string": ssa_format_title(script_info),
    "style_string": ssa_format_style(style),
    "events": ssa_format_event(event)
  }

def ssa_format_title(info):
  return "[Script Info]\nTitle: " \
        + info['title']+"\nOriginal Script: " \
        + info['Original Script'] \
        + "\nScriptType: v4.00"

def ssa_format_style(styles):
  format_string = "Format: "
  styles_string = ""
  for i in styles['order']:
    format_string += (i + ", ")
  for style in styles['styles']:
    style_holder = 'Style: '
    for j in styles['order']:
      style_holder += (style[j] + ", ")
    styles_string += (style_holder[:-2]+'\n')
  return format_string[:-2] +"\n"+styles_string

def ssa_format_event(event):
  format_string = "Format: "
  event_strings = ["Dialogue: ", "Dialogue: "]
  for i in event['order']:
    format_string += (i + ", ")
    if i in event.keys():
      event_strings[0] += (event[i] + ",")
      if i == 'Style':
        event_strings[1] += "Secondary,"
      else:
        event_strings[1] += (event[i] + ",")
  return {"format": format_string[:-2], "event_shell": event_strings}




