import unittest
import subtitleIO
import datetime

srt_verifier = [subtitleIO.SubLine(['BROKEN EMBRACES'], datetime.time(0, 1, 12, 833*1000), datetime.time(0, 1, 19, 0) )]
ssa_verifier = [subtitleIO.SubLine(['BROKEN EMBRACES'], datetime.time(0, 1, 12, 83*10000), datetime.time(0, 1, 19, 0) )]
srt_testfile = 'test_files/SRT_3Lines.srt'
ssa_testfile = 'test_files/SSA_3Lines.ssa'
config_testfile = 'test_files/config.json'

#basic reading and writing tests
class TestCore(unittest.TestCase):

  def __init__(self, *args, **kwargs):
    super(TestCore, self).__init__(*args, **kwargs)
    self.srtSubsFormat = subtitleIO.process_srt(subtitleIO.read_subtitles(srt_testfile))
    self.ssaSubsFormat = subtitleIO.process_ssa(subtitleIO.read_subtitles(ssa_testfile))
  
  def test_read_srt_dialogue(self):
    self.assertEqual(self.srtSubsFormat[0].dialogue, srt_verifier[0].dialogue)

  def test_read_srt_times(self):
    self.assertEqual(self.srtSubsFormat[0].time, srt_verifier[0].time)
  
  def test_write_srt(self):
    input_subs = subtitleIO.read_subtitles(srt_testfile)
    output_subs = subtitleIO.format_srt(self.srtSubsFormat)
    self.assertEqual(input_subs, output_subs)
    #write as srt to file
  
  def test_read_ssa_dialogue(self):
    self.assertEqual(self.ssaSubsFormat[0].dialogue, ssa_verifier[0].dialogue)

  def test_read_ssa_times(self):
    self.assertEqual(self.ssaSubsFormat[0].time, ssa_verifier[0].time)

  def write_ssa():
    return 0
    #write as ssa to file, compare

class TestProcessConfig(unittest.TestCase):
  def test_read_config_json(self):
    subtitleIO.process_config(config_testfile)
    return 0


class TestMerges(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestConversion, self).__init__(*args, **kwargs)
    self.srtSubsFormat = subtitleIO.process_srt(subtitleIO.read_subtitles(srt_testfile))
    self.ssaSubsFormat = subtitleIO.process_ssa(subtitleIO.read_subtitles(ssa_testfile))
  
  def pair_lines(self):
    return 0

  def write_file(self):
    return 0
  

if __name__ == '__main__':
    unittest.main()
