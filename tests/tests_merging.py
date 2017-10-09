import unittest
import os
from ..SubIO import Subtitling,ProcessSSA,ProcessSRT,FileIO,SubMatch,SSAValidators

__location__ = os.path.realpath(
  os.path.join(os.getcwd(), os.path.dirname(__file__)))

TEST_FILES_DIR = __location__+'/test_files/'
SRT_TESTFILE    = TEST_FILES_DIR+'3Lines.srt'
SSA_TESTFILE    = TEST_FILES_DIR+'3Lines.ssa'

CONFIG_DIR = __location__+'/../configs/'

MERGE_MATCH         = TEST_FILES_DIR+'Merge_Match.srt'
MERGE_1SEC          = TEST_FILES_DIR+'Merge_1sec.srt'
MERGE_MAXLEN        = TEST_FILES_DIR+'Merge_Longline.srt'
MERGE_MULTILINE     = TEST_FILES_DIR+'Merge_Multiline.srt'
RESULT_MERGE_MATCH  = TEST_FILES_DIR+'Result_Merge_Match.srt'
RESULT_1SEC_FAIL    = TEST_FILES_DIR+'Result_1Sec_Fail.srt'


#Testing the merge process, syncing files, validation,etc
#Using SRT for simplicity's sake
class TestMerges(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestMerges, self).__init__(*args, **kwargs)
    self.resultMergeMatch = ProcessSRT.process_srt(FileIO.read_full_file(RESULT_MERGE_MATCH))
    self.resultMergeMatchTxt = ProcessSRT.format_srt(self.resultMergeMatch)
    self.result1SecFail = ProcessSRT.process_srt(FileIO.read_full_file(RESULT_1SEC_FAIL))
    self.result1SecFailTxt = ProcessSRT.format_srt(self.result1SecFail)
    FileIO.write_file(TEST_FILES_DIR+'outputs/result1secFail.srt', self.result1SecFailTxt)
    FileIO.write_file(TEST_FILES_DIR+'outputs/resultMergeMatch.srt', self.resultMergeMatchTxt)

  def test_basic_pair(self):
    print("Merge time match")
    subs1 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_MATCH))
    subs2 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_MATCH))
    SubMatch.match_process(subs1, subs2)
    output = ProcessSRT.format_srt(subs1)
    FileIO.write_file(TEST_FILES_DIR+'outputs/basic_pair.srt', output)
    self.assertEqual(output, self.resultMergeMatchTxt)

  def test_time_window_success(self):
    print("Merge time-variance match")
    subs1 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_MATCH))
    subs2 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_1SEC))
    SubMatch.match_process(subs1, subs2, 1000)
    output = ProcessSRT.format_srt(subs1)
    FileIO.write_file(TEST_FILES_DIR+'outputs/time_window_success.srt', output)
    self.assertEqual(output, self.resultMergeMatchTxt)

  def test_time_window_fail(self):
    print("Merge time-variance non-match")
    subs1 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_MATCH))
    subs2 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_1SEC))
    SubMatch.match_process(subs1, subs2)
    output = ProcessSRT.format_srt(subs1)
    FileIO.write_file(TEST_FILES_DIR+'outputs/time_window_fail.srt', output)
    self.assertEqual(output, self.result1SecFailTxt)

  def test_ssa_write(self):
    print("Trial SSA Merge output")
    subs1 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_MATCH))
    subs2 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_1SEC))
    SubMatch.match_process(subs1, subs2, 1000)
    condir = CONFIG_DIR+'ssa/'
    second = condir+'secondary.config.json'
    white = condir+'whiteBlackOutline.config.json'
    format_data = ProcessSSA.get_ssa_format(FileIO.read_json(second), FileIO.read_json(white))
    headings_string = ProcessSSA.ssa_headings_string(format_data)
    FileIO.write_file('hmm.ssa', headings_string)
    for i in subs1:
      FileIO.append_file('hmm.ssa', ProcessSSA.format_merge_ssa_line(i, format_data['events']['event_shell']))


if __name__ == '__main__':
    unittest.main()
