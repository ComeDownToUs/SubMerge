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

def read_merge_config(config_file):
  hardcoded_settings = {
    "Script Info": {
      "title": "Untitled",
      "Original Script": "<unknown>"
    },
    "Events": {
      "title": "Dialogue",
      "Marked": "Marked=0",
      "Style": "Default",
      "Name": "NTP",
      "MarginL": "0000",
      "MarginR": "0000",
      "MarginV": "0000",
      "PrimaryEffect": "!Effect",
      "order": [
        "title",
        "Marked",
        "Style",
        "Name",
        "MarginL",
        "MarginR",
        "MarginV",
        "PrimaryEffect",
        "Start",
        "End",
        "Text"
      ]
    },
    "V4 Styles": {
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
  }
  read_settings = validate_merge_config(read_json(config_file))
  if (read_settings == None):
    read_settings = hardcoded_settings
  return hardcoded_settings

def validate_merge_config(config):
  return None

def read_ssa_style_config(config_file):
  hardcoded_settings = {
    "secondary_char_limit": 80,
    "newline": false,
    "splitter": "==-==",
    "time_variance_ms": 500
  }
  read_settings = validate_merge_config(read_json(config_file))
  if (read_settings == None):
    read_settings = hardcoded_settings
  return hardcoded_settings

def validate_ssa_config(config):
  return None
