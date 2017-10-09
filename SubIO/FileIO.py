import json
import codecs

''' File Processing '''

def read_full_file(sub_file):
  with codecs.open(sub_file,'r',encoding='utf8') as f:
    text = f.read()
  return text

def write_file(sub_file, sub_text):
  with codecs.open(sub_file,'w',encoding='utf8') as f:
    text = f.write(sub_text)
  return text

def append_file(sub_file, sub_text):
  with codecs.open(sub_file,'a',encoding='utf8') as f:
    text = f.write(sub_text)
  return text


def read_json(json_file): #returns dictionary
  return json.loads(read_full_file(json_file))

def read_merge_config(merge_config):
  hardcoded_settings = {
    "secondary_char_limit": 80,
    "newline": false,
    "splitter": "==-==",
    "time_variance_ms": 500
  }
  config_data = read_json(merge_config)
  return valid_config(config_data['merger_specs'], hardcoded_settings)
