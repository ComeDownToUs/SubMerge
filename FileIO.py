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
