import json

''' File Processing '''

def read_full_file(sub_file):
  f = open(sub_file, 'r')
  text = f.read()
  f.close()
  return text

def write_file(sub_file, sub_text):
  f = open(sub_file, 'w')
  f.write(sub_text)
  f.close()
  return sub_text

def read_json(json_file): #returns dictionary
  return json.loads(read_full_file(json_file))

def valid_config(config, defaults):
  log_index = 0
  try:
    for i in defaults.keys():
      if type(config[i]) == type(defaults[i]):
        continue
      else:
        print "Wrong type for "+i+", using defaults"
        return defaults
  except AttributeError:
    print "Missing attribute"
    return defaults
  return config

def read_merge_config(merge_config):
  hardcoded_settings = {
    "secondary_char_limit": 80,
    "newline": false,
    "splitter": "==-==",
    "time_variance_ms": 500
  }
  config_data = read_json(merge_config)
  return valid_config(config_data['merger_specs'], hardcoded_settings)

def valid_ssa_cfg(config, defaults, order):
  try:
    for i in order:
      if type(config[i]) == 'str':
        continue
      else:
        print "All SSA configs should be strings, using defaults"
        return defaults
  except AttributeError:
    print "Missing attribute"
    return defaults
  return config

def read_ssa_style_config(config_file):
  hardcoded = {
    "styles": [
      {
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
        "Encoding": "0"
      },
      {
        "title": "Style",
        "Name": "Secondary",
        "Fontname": "Tahoma",
        "Fontsize": "16",
        "PrimaryColour": "12632256",
        "SecondaryColour": "16777215",
        "TertiaryColour": "16777215",
        "BackColour": "12632256",
        "Bold": "-1",
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
  config_data = read_json(config_file)
  style_data = config_data['V4 Styles']['styles']
  validated = []

  validated.append(valid_ssa_config(style_data[0], hardcoded['styles'][0], hardcoded['order'] ))
  validated.append(valid_ssa_config(style_data[1], hardcoded['styles'][1], hardcoded['order'] ))
  return {'styles': validated, 'order': hardcoded_settings['order']}

def validate_ssa_config(config):
  return None
