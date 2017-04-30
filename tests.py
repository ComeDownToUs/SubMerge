import unittest
import subtitleIO
import datetime

srt_verifier = [subtitleIO.SubLine(['BROKEN EMBRACES'], datetime.time(0, 1, 12, 833*1000), datetime.time(0, 1, 19, 0) )]
ssa_verifier = [subtitleIO.SubLine(['BROKEN EMBRACES'], datetime.time(0, 1, 12, 83*10000), datetime.time(0, 1, 19, 0) )]
srt_testfile = 'test_files/3Lines.srt'
ssa_testfile = 'test_files/3Lines.ssa'
config_testfile = 'config.json'

#basic reading and writing tests
class TestCore(unittest.TestCase):

  def __init__(self, *args, **kwargs):
    super(TestCore, self).__init__(*args, **kwargs)
    self.srtTestText = subtitleIO.read_full_file(srt_testfile)
    self.ssaTestText = subtitleIO.read_full_file(ssa_testfile)
    self.srtSubsFormat = subtitleIO.process_srt(self.srtTestText)
    self.ssaSubsFormat = subtitleIO.process_ssa(self.ssaTestText)
  
  # SRT TESTS
  # Input interpretation:
  def test_read_srt_dialogue(self):
    self.assertEqual(self.srtSubsFormat[0].dialogue, srt_verifier[0].dialogue)
  def test_read_srt_times(self):
    self.assertEqual(self.srtSubsFormat[0].time, srt_verifier[0].time)
  # Output generation:
  def test_write_srt(self):
    output_subs = subtitleIO.format_srt(self.srtSubsFormat)
    self.assertEqual(self.srtTestText, output_subs)
    #write as srt to file
  
  # SSA TESTS
  # Input: testing parsing, only the events data is relevant here current
  def test_read_ssa_dialogue(self):
    self.assertEqual(self.ssaSubsFormat[0].dialogue, ssa_verifier[0].dialogue)
  def test_read_ssa_times(self):
    self.assertEqual(self.ssaSubsFormat[0].time, ssa_verifier[0].time)
  # Output <<TODO>> Handle config file, test various aspects
  def test_write_ssa(self):
    output_format = subtitleIO.format_ssa(self.ssaSubsFormat)
    self.assertEqual(self.ssaTestText, output_format)
    #write as ssa to file, compare

#config file validation
class TestProcessConfig(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestProcessConfig, self).__init__(*args, **kwargs)

  def test_read_config_json(self):
    result = subtitleIO.read_json(config_testfile)
    return 0
  def verify_order():
    #reorder entries when necessary values are in wrong order
    return 0
  def verify_types():
    #ensure only strings and numbers in relevant fields
    return 0
  #test values and keys validation (ensure necessary fields and ordering is included)
  #if 


class TestMerges(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestConversion, self).__init__(*args, **kwargs)
    self.srtSubsFormat = subtitleIO.process_srt(subtitleIO.read_full_file(srt_testfile))
    self.ssaSubsFormat = subtitleIO.process_ssa(subtitleIO.read_full_file(ssa_testfile))
  
  def pair_lines(self):
    #needs to scan for subtitles with matching start times
    return 0

  def format_merges(self):
    #needs to apply the necessary formatting changes to the two strings
    return 0
  
  def write_file(self):
    #ideally unnecessary, use the default SSA writer
    return 0
  

if __name__ == '__main__':
    unittest.main()
