import unittest
import ETS_Tech_Screener as code 


class TestETS(unittest.TestCase):

	def test_InputFile(self):
		self.assertRaises(Exception, code.readfile, 'sample_errored.csv')
		self.assertRaises(Exception, code.readfile, 'sample_wrongcols.csv')  

	def test_Output(self):
		assert True

if __name__ =="__main__":
    unittest.main() 		