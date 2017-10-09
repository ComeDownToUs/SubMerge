import os
import unittest
import datetime
from ..SubIO import Subtitling, ProcessSSA, ProcessSRT, FileIO, SSAValidators, SubMatch

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
print(__location__)

SRT_VERIFIER = [Subtitling.SubLine(['BROKEN EMBRACES'], datetime.time(0, 1, 12, 833*1000), datetime.time(0, 1, 19, 0) )]
SSA_VERIFIER = [Subtitling.SubLine(['BROKEN EMBRACES'], datetime.time(0, 1, 12, 83*10000), datetime.time(0, 1, 19, 0) )]
TEST_FILES_DIR = __location__+'/test_files/'
SRT_TESTFILE    = TEST_FILES_DIR+'3Lines.srt'
SSA_TESTFILE    = TEST_FILES_DIR+'3Lines.ssa'

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
    print("Reading SRT dialogue")
    self.assertEqual(self.srtSubsFormat[0].dialogue, SRT_VERIFIER[0].dialogue)
  def test_read_srt_times(self):
    print("Reading SRT time")
    self.assertEqual(self.srtSubsFormat[0].time, SRT_VERIFIER[0].time)
  # Output generation:
  def test_write_srt(self):
    print("Writing SRT")
    output_subs = ProcessSRT.format_srt(self.srtSubsFormat)
    self.assertEqual(self.srtTestText, output_subs)

  # SSA TESTS
  # Input:
  #   testing parsing, only the events data is relevant here current
  def test_read_ssa_dialogue(self):
    print("Reading SSA dialogue")
    self.assertEqual(self.ssaSubsFormat[0].dialogue, SSA_VERIFIER[0].dialogue)
  def test_read_ssa_times(self):
    print("Reading SSA time")
    self.assertEqual(self.ssaSubsFormat[0].time, SSA_VERIFIER[0].time)
  # Output
  #   Config processing is highly related to this section
  def test_ssa_string(self):
    print("Writing SSA")
    output_format = ProcessSSA.format_ssa(self.ssaSubsFormat)
    FileIO.write_file(TEST_FILES_DIR+'outputs/output.ssa', output_format)
    self.assertEqual(self.ssaTestText, output_format)
  def ssa_output(self):
    #output line by line
    return 0

class SSAFormatting(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestConversion, self).__init__(*args, **kwargs)
    self.srtSubsFormat = ProcessSRT.process_srt(FileIO.read_full_file(SRT_TESTFILE))
    self.ssaSubsFormat = ProcessSSA.process_ssa(FileIO.read_full_file(SSA_TESTFILE))

if __name__ == '__main__':
    unittest.main()
