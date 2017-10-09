# This code will only use the style validation and hold the constants for now

DEFAULT_SCRIPT_INFO = {
  "Title": "Built By https://github.com/ComeDownToUs/SubMerge",
  "Original Script": "Likely Someone Else"}
DEFAULT_V4_STYLES = {
  "Format": "Style",
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
  "order": ["Format","Name","Fontname","Fontsize","PrimaryColour","SecondaryColour","TertiaryColour","BackColour","Bold","Italic","BorderStyle","Outline","Shadow","Alignment","MarginL","MarginR","MarginV","AlphaLevel","Encoding"]}
DEFAULT_EVENT = {
  "Format": "Dialogue",
  "Marked": "Marked=0",
  "Start": "00:00:00.00",
  "End": "00:00:00.00",
  "Style": "Default",
  "Name": "NTP",
  "MarginL": "0000",
  "MarginR": "0000",
  "MarginV": "0000",
  "PrimaryEffect": "!Effect",
  "order": ["Format","Marked","Start","End","Style","Name","MarginL","MarginR","MarginV","PrimaryEffect","Text"]}

def validate_info(config_info):
  return attribute_cleanup(config_info, DEFAULT_SCRIPT_INFO)

#needs to avoid reserved keywords
def validate_style(config_style={}):
  try:
    if(config_style == {}):
      print("SSA Validator -- validate_style: No styles passed in, using defaults")
      return DEFAULT_V4_STYLES
    validated = attribute_cleanup(config_style, DEFAULT_V4_STYLES)
    validated['order'] = DEFAULT_V4_STYLES['order']
    return validated
  except TypeError:
    print "Invalid type passed as style, using defaults"
    return DEFAULT_V4_STYLES

def validate_event(config_event):
  return attribute_cleanup(config_event, DEFAULT_EVENT)

def attribute_cleanup(configurated, defaults):
  output_config = {
    'log': ''
  }
  for entry in defaults['order']:
    try:
      if len(configurated[entry])>0:
        output_config[entry] = configurated[entry]
      else:
        output_config[entry] = defaults[entry]
        output_config['log'] += ('Blank string at '+entry)
    except (AttributeError, KeyError, TypeError) as e:
      output_config[entry] = defaults[entry]
      output_config['log'] += ('Error at key '+str(e)+'\n')
  if output_config['log'] == '':
    output_config['log'] = 'No issues in validation check'
  else:
    print "OUTPUT CONFIG ISSUES\n=============="
    print output_config['log']
  return output_config

''' Type validation '''

''' this is somehow breaking tests at the moment
    so I'm gonna leave it for the time being
    and get back to it once everything is running '''
def is_float(a):
  try:
    float(a)
    return True
  except ValueError:
    return False
def is_int(a):
  try:
    int(a)
    return True
  except ValueError:
    return False
def attr_type(a):
  if is_float(a):
    return 'float'
  elif is_int(a):
    return 'int'
def type_match(a,b):
  return attr_type(a) == attr_type(b)


