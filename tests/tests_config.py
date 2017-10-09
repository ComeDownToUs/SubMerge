import unittest
import os
from ..SubIO import FileIO, SubMatch, SSAValidators

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

TEST_DIR = __location__+'/test_files/'
CONFIG_DIR = TEST_DIR+'configs/'
CONFIG_ATTR_ERROR   = CONFIG_DIR+'style_attributeerror.json'
CONFIG_BLANK_STR    = CONFIG_DIR+'style_blankstring.json'
CONFIG_TYPE_ERROR   = CONFIG_DIR+'style_typeerror.json'
RESULT_CONFIG       = TEST_DIR+ 'outputs/validate_style.json'


#config file validation
class TestProcessConfig(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestProcessConfig, self).__init__(*args, **kwargs)
    self.result = FileIO.read_json(RESULT_CONFIG)
    self.maxDiff=None

  def test_read_config_json(self):
    print("Config Basic Reading")
    self.assertEqual(self.result['Format'], 'Style')

  def test_config_attr_error(self):
    print("Config handling missing attribute")
    attr_error = FileIO.read_json(CONFIG_ATTR_ERROR)
    resolved = SSAValidators.validate_style(attr_error)
    del resolved['log']
    del resolved['order']
    self.assertDictEqual(self.result, resolved)

  def test_config_blank_string(self):
    print("Config handling blank entry")
    blank_str = FileIO.read_json(CONFIG_BLANK_STR)
    resolved = SSAValidators.validate_style(blank_str)
    del resolved['log']
    del resolved['order']
    self.assertDictEqual(self.result, resolved)

  # TODO This needs significant expansion for actual types
  def test_config_type_error(self):
    print("Config handling type error")
    typ_err = FileIO.read_json(CONFIG_TYPE_ERROR)
    resolved = SSAValidators.validate_style(typ_err)
    del resolved['log']
    del resolved['order']
    self.assertDictEqual(self.result, resolved)
  #test values and keys validation (ensure necessary fields and ordering is included)

if __name__ == '__main__':
  unittest.main()
