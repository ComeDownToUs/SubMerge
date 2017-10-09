import re
import Subtitling
import SSAValidators

''' Inputs (converts to an array of SubLine class files) '''

# <<TODO>> improve this, arbitrary means of skipping lines with no content, likely buggy
def process_ssa(sub_text):
  formatted_lines = []
  segment_split = re.split('\n\[Events\]\n|\n\[V4 Styles\]\n', sub_text)
  dialogue_lines=segment_split[2].split('\n')
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
  ssa_output += (ssa_skeleton["styles_string"] + "\n")
  ssa_output += "[Events]\n"
  ssa_output += (ssa_skeleton["events"]['format'])
  ssa_output += '\n'
  if merge:
    return ssa_output + format_merge_ssa(sub_lines, ssa_skeleton['events']['event_shell'])
  for entry in sub_lines:
    ssa_output += format_ssa_line(entry, ssa_skeleton['events']['event_shell'][0])
  return ssa_output


def format_ssa_line(subtitle, event_shell):
  ssa_event = event_shell
  ssa_event = ssa_event.replace("00:00:00.00", subtitle.time['start'].strftime("%H:%M:%S.%f")[0:11], 1)
  ssa_event = ssa_event.replace("00:00:00.00", subtitle.time['end'].strftime("%H:%M:%S.%f")[0:11], 1)
  for line in subtitle.dialogue:
    ssa_event += line
    ssa_event += "\\n"
  ssa_event = ssa_event[:-2] + "\n"
  return ssa_event

def format_merge_ssa_dialogue(sub_lines, event_shells):
  ssa_merge_output = ''
  for entry in sub_lines:
    ssa_merge_output += format_merge_ssa_line(entry, event_shells)
  return ssa_merge_output

def format_merge_ssa_line(subtitle, event_shells):
  ssa_subtitle_out = ''
  for index, line in enumerate(subtitle.dialogue):
    line = line.replace('\n', '\\n')
    if index > 1:
      break
    ssa_event = event_shells[index] + line
    ssa_event = ssa_event.replace("00:00:00.00", subtitle.time['start'].strftime("%H:%M:%S.%f")[0:11], 1)
    ssa_event = ssa_event.replace("00:00:00.00", subtitle.time['end'].strftime("%H:%M:%S.%f")[0:11], 1)
    ssa_subtitle_out += ssa_event
    ssa_subtitle_out += '\n'
  return ssa_subtitle_out


#returns skeletal strings built from config specification to apply time and dialogue to for SSA
def get_ssa_format(style1={}, style2={}):
  #<<TODO>> Read in JSON configs and overwrite where appropriate
  script_info= {
    "title": "Built By https://github.com/ComeDownToUs/SubMerge",
    "Original Script": "Likely Someone Else"
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
  styles = [SSAValidators.validate_style(style1)]
  if( len(style2.keys()) != 0):
    styles.append(SSAValidators.validate_style(style2)) #<<TODO>> handle if empty
  return {
    "info_string": ssa_format_title(script_info),
    "styles_string": ssa_format_style(styles),
    "events": ssa_format_event(event,styles)
  }

def ssa_headings_string(ssa_formats):
  ssa_output = ssa_formats["info_string"] + "\n\n"
  ssa_output += "[V4 Styles]\n"
  ssa_output += (ssa_formats["styles_string"] + "\n")
  ssa_output += "[Events]\n"
  ssa_output += (ssa_formats["events"]['format'])
  ssa_output += '\n'
  return ssa_output

def ssa_format_title(info):
  return "[Script Info]\nTitle: " \
        + info['title']+"\nOriginal Script: " \
        + info['Original Script'] \
        + "\nScriptType: v4.00"

def ssa_format_style(styles):
  format_string = ""
  styles_string = ""
  for i in styles[0]['order']:
    format_string += (i + ", ")
  format_string = format_string.replace(',', ':', 1)
  for style in styles:
    style_holder = ''
    for j in style['order']:
      style_holder += (style[j] + ", ")
    style_holder = style_holder.replace(',', ':', 1)
    styles_string += (style_holder[:-2]+'\n')
  return format_string[:-2] +"\n"+styles_string

def ssa_format_event(event, styles):
  format_string = "Format: "
  event_string_template = "Dialogue: "
  event_strings = []
  for i in event['order']:
    format_string += (i + ", ")
    if i in event.keys():
      if i == 'Style':
        event_string_template += 'PLACEHOLDER,'
      else:
        event_string_template += (event[i] + ",")
  for style in styles:
    event_strings.append(event_string_template.replace('PLACEHOLDER', style['Name']))
  return {"format": format_string[:-2], "event_shell": event_strings}



