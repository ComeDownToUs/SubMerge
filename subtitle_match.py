import subtitleIO

#this is all messy and untested plotting at the moment
def match_process(sublistA, sublistB):
  counter_B = 0
  for subtitle in sublistA:
    start_range, end_range = get_time_range(subtitle.time.start)
    for i in range(counter_B, len(sublistB)):
      if sublistB[i].time.start > end_range:
        break
      elif sublistB[i].time.start < start_range:
        counter_B+=1
        continue
      elif sublistB[i].time.start > start_range or subtitle[i].time.end < end_range:
        subtitle.dialogue.append(sublistB[i].dialogue)
        counter_B +=1
        break

#returns datetime objects to test if subtitle timings match
def get_time_range(root_time, variance=1000):
  start_point = root_time - datetime.timedelta(milliseconds=variance)
  end_point = root_time + datetime.timedelta(milliseconds=variance)
  return start_point, end_point

#just reduces a subtitle's dialogue proportions down to one string with no linebreaks
def remove_newlines_ssa(sublist, newline_replacement = "--"):
  for i in range(len(sublist)):
    if len(sublist[i].dialogue)>1:
      merged_dialogue = ""
      for line in sublist[i].dialogue:
        merged_dialogue += (line + newline_replacement)
      sublist[i].dialogue = [merged_dialogue]
  return sublist

#apply stylings to secondary subs,
#need to test which ones need closing
def apply_styling(sublist, style_change):
  styling = ""
  if "bold" is in style_change:
    styling = "{\b1}"+styling
    #styling[1] += styling[0]+"{\b0}"
  if "fs12" is in style_change:
    styling = "{\fs12}"+styling
  if "italics" is in style_change:
    styling = "{\fs12}"+styling
  for i in range(len(sublist)):
    sublist[i].dialogue[0] = styling + sublist[i].dialogue[0]
  return sublist



#

