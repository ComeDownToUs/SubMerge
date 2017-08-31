import unittest
import datetime
import Subtitling
import ProcessSSA
import ProcessSRT
import FileIO
import SubMatch
import SSAValidators

SRT_VERIFIER = [Subtitling.SubLine(['BROKEN EMBRACES'], datetime.time(0, 1, 12, 833*1000), datetime.time(0, 1, 19, 0) )]
SSA_VERIFIER = [Subtitling.SubLine(['BROKEN EMBRACES'], datetime.time(0, 1, 12, 83*10000), datetime.time(0, 1, 19, 0) )]
MATCH_VERIFIER = [Subtitling.SubLine(['BROKEN EMBRACES', 'Los abrazos rotos'], datetime.time(0, 1, 12, 833*1000), datetime.time(0, 1, 19, 0) )]
TEST_FILES_DIR = 'test_files/'
SRT_TESTFILE    = TEST_FILES_DIR+'3Lines.srt'
SSA_TESTFILE    = TEST_FILES_DIR+'3Lines.ssa'

MERGE_MATCH     = TEST_FILES_DIR+'Merge_Match.srt'
MERGE_1SEC      = TEST_FILES_DIR+'Merge_1sec.srt'
MERGE_MAXLEN    = TEST_FILES_DIR+'Merge_Longline.srt'
MERGE_MULTILINE = TEST_FILES_DIR+'Merge_Multiline.srt'
RESULT_MERGE_MATCH  = TEST_FILES_DIR+'Result_Merge_Match.srt'
RESULT_1SEC_FAIL    = TEST_FILES_DIR+'Result_1Sec_Fail.srt'

CONFIG_ATTR_ERROR   = TEST_FILES_DIR+'configs/style_attributeerror.json'
CONFIG_BLANK_STR    = TEST_FILES_DIR+'configs/style_blankstring.json'
CONFIG_TYPE_ERROR   = TEST_FILES_DIR+'configs/style_typeerror.json'
RESULT_CONFIG       = TEST_FILES_DIR + 'outputs/validate_style.json'

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
    print "Reading SRT dialogue"
    self.assertEqual(self.srtSubsFormat[0].dialogue, SRT_VERIFIER[0].dialogue)
  def test_read_srt_times(self):
    print "Reading SRT time"
    self.assertEqual(self.srtSubsFormat[0].time, SRT_VERIFIER[0].time)
  # Output generation:
  def test_write_srt(self):
    print "Writing SRT"
    output_subs = ProcessSRT.format_srt(self.srtSubsFormat)
    self.assertEqual(self.srtTestText, output_subs)

  # SSA TESTS
  # Input:
  #   testing parsing, only the events data is relevant here current
  def test_read_ssa_dialogue(self):
    print "Reading SSA dialogue"
    self.assertEqual(self.ssaSubsFormat[0].dialogue, SSA_VERIFIER[0].dialogue)
  def test_read_ssa_times(self):
    print "Reading SSA time"
    self.assertEqual(self.ssaSubsFormat[0].time, SSA_VERIFIER[0].time)
  # Output
  #   Config processing is highly related to this section
  def test_ssa_string(self):
    print "Writing SSA"
    output_format = ProcessSSA.format_ssa(self.ssaSubsFormat)
    FileIO.write_file(TEST_FILES_DIR+'outputs/output.ssa', output_format)
    self.assertEqual(self.ssaTestText, output_format)
  def ssa_output(self):
    #output line by line
    return 0


#config file validation
class TestProcessConfig(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestProcessConfig, self).__init__(*args, **kwargs)
    self.result = FileIO.read_json(RESULT_CONFIG)
    self.maxDiff=None

  def test_read_config_json(self):
    print "Config Basic Reading"
    self.assertEqual(self.result['Format'], 'Style')
  def test_config_attr_error(self):
    print "Config handling missing attribute"
    attr_error = FileIO.read_json(CONFIG_ATTR_ERROR)
    resolved = SSAValidators.validate_style(attr_error)
    del resolved['log']
    self.assertDictEqual(self.result, resolved)
  def test_config_blank_string(self):
    print "Config handling blank entry"
    blank_str = FileIO.read_json(CONFIG_BLANK_STR)
    resolved = SSAValidators.validate_style(blank_str)
    del resolved['log']
    self.assertDictEqual(self.result, resolved)
  def test_config_type_error(self):
    print "Config handling type error"
    blank_str = FileIO.read_json(CONFIG_BLANK_STR)
    resolved = SSAValidators.validate_style(blank_str)
    del resolved['log']
    self.assertDictEqual(self.result, resolved)
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
    FileIO.write_file(TEST_FILES_DIR+'outputs/result1secFail.srt', self.result1SecFailTxt)
    FileIO.write_file(TEST_FILES_DIR+'outputs/resultMergeMatch.srt', self.resultMergeMatchTxt)

  def test_basic_pair(self):
    print "Merge time match"
    subs1 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_MATCH))
    subs2 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_MATCH))
    SubMatch.match_process(subs1, subs2)
    output = ProcessSRT.format_srt(subs1)
    FileIO.write_file(TEST_FILES_DIR+'outputs/basic_pair.srt', output)
    self.assertEqual(output, self.resultMergeMatchTxt)

  def test_time_window_success(self):
    print "Merge time-variance match"
    subs1 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_MATCH))
    subs2 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_1SEC))
    SubMatch.match_process(subs1, subs2, 1000)
    output = ProcessSRT.format_srt(subs1)
    FileIO.write_file(TEST_FILES_DIR+'outputs/time_window_success.srt', output)
    self.assertEqual(output, self.resultMergeMatchTxt)

  def test_time_window_fail(self):
    print "Merge time-variance non-match"
    subs1 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_MATCH))
    subs2 = ProcessSRT.process_srt(FileIO.read_full_file(MERGE_1SEC))
    SubMatch.match_process(subs1, subs2)
    output = ProcessSRT.format_srt(subs1)
    FileIO.write_file(TEST_FILES_DIR+'outputs/time_window_fail.srt', output)
    self.assertEqual(output, self.result1SecFailTxt)


class SSAFormatting(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestConversion, self).__init__(*args, **kwargs)
    self.srtSubsFormat = ProcessSRT.process_srt(FileIO.read_full_file(SRT_TESTFILE))
    self.ssaSubsFormat = ProcessSSA.process_ssa(FileIO.read_full_file(SSA_TESTFILE))


if __name__ == '__main__':
    unittest.main()
