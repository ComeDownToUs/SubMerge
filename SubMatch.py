import datetime
import Subtitling
import ProcessSSA

#this is all messy and untested plotting at the moment
#for SSA, both sets of subtitles appearing at the same time seems pretty essential
def match_process(sublistA, sublistB, time_variance=500, newlines='\n'):
  remove_newlines(sublistA, newlines)
  remove_newlines(sublistB, '[]')
  counter_B = 0
  for subtitle in sublistA:
    start_range, end_range = get_time_range(subtitle.time['start'], time_variance)
    for i in range(counter_B, len(sublistB)):
      if sublistB[i].time['start'] > end_range:
        break
      elif sublistB[i].time['start'] < start_range:
        counter_B+=1
        continue
      elif sublistB[i].time['start'] > start_range or subtitle[i].time['end'] < end_range:
        subtitle.dialogue.append(character_cutoff(sublistB[i].dialogue[0]))
        counter_B +=1
        break

#returns datetime objects to test if subtitle timings match
def get_time_range(root_time, variance=1000):
  dt_root_time = datetime.datetime(100, 1, 1, root_time.hour, root_time.minute, root_time.second, root_time.microsecond)
  delta_variance = datetime.timedelta(milliseconds=variance)
  dt_start = dt_root_time - delta_variance
  dt_end = dt_root_time + delta_variance
  t_start = datetime.time(dt_start.hour, dt_start.minute, dt_start.second, dt_start.microsecond)
  t_end = datetime.time(dt_end.hour, dt_end.minute, dt_end.second, dt_end.microsecond)
  return t_start, t_end

#just reduces a subtitle's dialogue proportions down to one string with no linebreaks
#only needed if space on screen is an issue
def remove_newlines(sublist, newline_replacement = "--"):
  for i in range(len(sublist)):
    if len(sublist[i].dialogue)>1:
      merged_dialogue = ""
      for line in sublist[i].dialogue:
        merged_dialogue += (line + newline_replacement)
      sublist[i].dialogue = [merged_dialogue.strip(newline_replacement)]
  return sublist

def character_cutoff(dialogue, limit=140):
  if(len(dialogue)<=limit):
    return dialogue
  else:
    return dialogue[:(limit-4)]+'[...]'

def merge_srt_format(sublist):
  return ProcessSRT.format_srt(sublist)

def merge_ssa_format(sublist):
  return ProcessSSA.format_ssa(sublist, True)

# NOTE: This function is likely not required as SSA allows multiple subtitles at once
#apply stylings to a string,
#need to test which ones need closing
def ssa_apply_styling(sublist, style_change):
  styling = ["", ""]
  if "bold" in style_change:
    styling[0] = "{\\b1}"+styling[0]
    styling[1] += styling[1]+"{\\b0}"
  if "fs12" in style_change:
    styling[0] = "{\\fs12}"+styling[0]
    styling[1] += styling[1]+"{\\r}"#will override all overrides
  if "italics" in style_change:
    styling[0] = "{\i1}"+styling[0]
    styling[1] = styling[0]+"{\i0}"
  if "underline" in style_change:
    styling[0] = "{\u1}"+styling[0]
    styling[1] = styling[0]+"{\u0}"
  if "strike" in style_change:
    styling[0] = "{\s1}"+styling[0]
    styling[1] = styling[0]+"{\s0}"
  #return styling[0]+dialogue+styling[1]
  return styling

