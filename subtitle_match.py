import subtitleIO

#this is all messy and untested plotting at the moment
#for SSA, both sets of subtitles appearing at the same time seems pretty essential
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
#only needed if space on screen is an issue
def remove_newlines(sublist, newline_replacement = "--"):
  for i in range(len(sublist)):
    if len(sublist[i].dialogue)>1:
      merged_dialogue = ""
      for line in sublist[i].dialogue:
        merged_dialogue += (line + newline_replacement)
      sublist[i].dialogue = [merged_dialogue]
  return sublist

#apply stylings to a string,
#need to test which ones need closing
def ssa_apply_styling(sublist, style_change):
  styling = ["", ""]
  if "bold" is in style_change:
    styling[0] = "{\\b1}"+styling[0]
    styling[1] += styling[1]+"{\\b0}"
  if "fs12" is in style_change:
    styling[0] = "{\\fs12}"+styling[0]
    styling[1] += styling[1]+"{\\r}"#will override all overrides
  if "italics" is in style_change:
    styling[0] = "{\i1}"+styling[0]
    styling[1] = styling[0]+"{\i0}"
  if "underline" is in style_change:
    styling[0] = "{\u1}"+styling[0]
    styling[1] = styling[0]+"{\u0}"
  if "strike" is in style_change:
    styling[0] = "{\s1}"+styling[0]
    styling[1] = styling[0]+"{\s0}"
  #return styling[0]+dialogue+styling[1]
  return styling



#

