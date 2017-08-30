# This code will only use the style validation and hold the constants for now

DEFAULT_SCRIPT_INFO = {
  "title": "Built By https://github.com/ComeDownToUs/SubMerge",
  "Original Script": "Likely Someone Else"}
DEFAULT_V4_STYLES = {
  "title": "Style",
  "Name": "HardDefault",
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
  "Encoding": "0",
  "order": ["Name","Fontname","Fontsize","PrimaryColour","SecondaryColour","TertiaryColour","BackColour","Bold","Italic","BorderStyle","Outline","Shadow","Alignment","MarginL","MarginR","MarginV","AlphaLevel","Encoding"]}
DEFAULT_EVENT = {
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
  "order": ["Marked","Start","End","Style","Name","MarginL","MarginR","MarginV","PrimaryEffect","Text"]}

def validate_info(config_info):
  return valid_ssa_attributes(config_info, DEFAULT_SCRIPT_INFO)

def validate_style(config_style):
  validated = valid_ssa_attributes(config_style, DEFAULT_V4_STYLES)
  if validated['Style'] == 'HardDefault':
    validated['log'] = 'Please use a valid name for Style (NOTE: '+\
      DEFAULT_V4_STYLES['Name']+'is reserved) '
    print validated['log']
    return  validated['log']
  return validated

def validate_event(config_event):
  return valid_ssa_attributes(config_event, DEFAULT_EVENT)

def has_attribute(configurated, defaults):
  output_config = {
    'log' = ''
  }
  for entry in order:
    try:
      if len(entry)>0:
        output_config[entry] = configurated[entry]
      else:
        dummy = entry[0]
    except (AttributeError, TypeError) as e:
      output_config[entry] = defaults[entry]
      output_config['log'] += (entry+':'+e+'\n')
  if output_config['log'] == '':
    output_config['log'] = 'No issues in validation check'
  print output_config['log']
  return output_config

