import unittest
import datetime
import Subtitling
import ProcessSSA
import ProcessSRT
import FileIO
import SubMatch

SRT_VERIFIER = [Subtitling.SubLine(['BROKEN EMBRACES'], datetime.time(0, 1, 12, 833*1000), datetime.time(0, 1, 19, 0) )]
SSA_VERIFIER = [Subtitling.SubLine(['BROKEN EMBRACES'], datetime.time(0, 1, 12, 83*10000), datetime.time(0, 1, 19, 0) )]
MATCH_VERIFIER = [Subtitling.SubLine(['BROKEN EMBRACES', 'Los abrazos rotos'], datetime.time(0, 1, 12, 833*1000), datetime.time(0, 1, 19, 0) )]
SRT_TESTFILE = 'test_files/3Lines.srt'
SSA_TESTFILE = 'test_files/3Lines.ssa'
MERGE_MATCH = 'test_files/Merge_Match.srt'
MERGE_1SEC = 'test_files/Merge_1sec.srt'
MERGE_MAXLEN = 'test_files/Merge_Longline.srt'
MERGE_MULTILINE = 'test_files/Merge_Multiline.srt'
RESULT_MERGE_MATCH = 'test_files/Result_Merge_Match.srt'
RESULT_1SEC_FAIL = 'test_files/Result_1Sec_Fail.srt'
CONFIG_FILE = 'config.json'

#basic reading and writing tests
class TestCore(unittest.TestCase):

  def __init__(self, *args, **kwargs):
    super(TestCore, self).__init__(*args, **kwargs)
    self.srtTestText = FileIO.read_full_file(SRT_TESTFILE)
    self.ssaTestText = FileIO.read_full_file(SSA_TESTFILE)
    self.srtSubsFormat = ProcessSRT.process_srt(self.srtTestText)
    self.ssaSubsFormat = ProcessSSA.process_ssa(self.ssaTestText)

  # SRT TESTS
  # Input interpretation:
  def test_read_srt_dialogue(self):
    self.assertEqual(self.srtSubsFormat[0].dialogue, SRT_VERIFIER[0].dialogue)
  def test_read_srt_times(self):
    self.assertEqual(self.srtSubsFormat[0].time, SRT_VERIFIER[0].time)
  # Output generation:
  def test_write_srt(self):
    output_subs = ProcessSRT.format_srt(self.srtSubsFormat)
    self.assertEqual(self.srtTestText, output_subs)
    #write as srt to file

  # SSA TESTS
  # Input: testing parsing, only the events data is relevant here current
  def test_read_ssa_dialogue(self):
    self.assertEqual(self.ssaSubsFormat[0].dialogue, SSA_VERIFIER[0].dialogue)
  def test_read_ssa_times(self):
    self.assertEqual(self.ssaSubsFormat[0].time, SSA_VERIFIER[0].time)
  # Output <<TODO>> Handle config file, test various aspects
  def test_write_ssa(self):
    output_format = ProcessSSA.format_ssa(self.ssaSubsFormat)
    self.assertEqual(self.ssaTestText, output_format)
    #write as ssa to file, compare

#config file validation
class TestProcessConfig(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestProcessConfig, self).__init__(*args, **kwargs)

  def test_read_config_json(self):
    result = FileIO.read_json(CONFIG_FILE)
    return 0
  def verify_order():
    #reorder entries when necessary values are in wrong order
    return 0
  def verify_types():
    #ensure only strings and numbers in relevant fields
    return 0
  #test values and keys validation (ensure necessary fields and ordering is included)
  #if

#Testing the merge process, syncing files, validation,etc
#Using SRT for simplicity's sake
class TestMerges(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestMerges, self).__init__(*args, **kwargs)
    self.resultMergeMatch = ProcessSRT.process_srt(FileIO.read_full_file(RESULT_MERGE_MATCH))
    self.resultMergeMatchTxt = ProcessSRT.format_srt(self.resultMergeMatch)
    self.result1SecFail = ProcessSRT.process_srt(FileIO.read_full_file(RESULT_1SEC_FAIL))
    self.result1SecFailTxt = ProcessSRT.format_srt(self.result1SecFail)
    FileIO.write_file('test_files/outputs/result1secFail.srt', self.result1SecFailTxt)
    FileIO.write_file('test_files/outputs/resultMergeMatch.srt', self.resultMergeMatchTxt)

  def test_basic_pair(self):
    subs1 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_MATCH))
    subs2 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_MATCH))
    SubMatch.match_process(subs1, subs2)
    output = ProcessSRT.format_srt(subs1)
    FileIO.write_file('test_files/outputs/basic_pair.srt', output)
    self.assertEqual(output, self.resultMergeMatchTxt)

  def test_time_window_fail(self):
    subs1 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_MATCH))
    subs2 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_1SEC))
    SubMatch.match_process(subs1, subs2)
    output = ProcessSRT.format_srt(subs1)
    FileIO.write_file('test_files/outputs/time_window_fail.srt', output)
    self.assertEqual(output, self.result1SecFailTxt)

  def test_time_window_success(self):
    subs1 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_MATCH))
    subs2 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_1SEC))
    SubMatch.match_process(subs1, subs2, 1000)
    output = ProcessSRT.format_srt(subs1)
    FileIO.write_file('test_files/outputs/time_window_success.srt', output)
    self.assertEqual(output, self.resultMergeMatchTxt)

  def write_file():
    #ideally unnecessary, use the default SSA writer
    print 'c'

#class CollapseDialogues
#class SRT Out Merge
#class TestConfig
#class TestSSAMerge

class SSAFormatting(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestConversion, self).__init__(*args, **kwargs)
    self.srtSubsFormat = ProcessSRT.process_srt(FileIO.read_full_file(SRT_TESTFILE))
    self.ssaSubsFormat = ProcessSSA.process_ssa(FileIO.read_full_file(SSA_TESTFILE))


if __name__ == '__main__':
    unittest.main()
