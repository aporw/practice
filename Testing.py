import unittest
import pandas as pd
import ETS_Tech_Screener as code


class TestETS(unittest.TestCase):
    def test_InputFile(self):
        # TestCase: File not found
        self.assertRaises(FileNotFoundError, code.readfile, "sample_errored.csv")
        # TestCase: Invalid columns
        self.assertRaises(Exception, code.readfile, "sample_wrongcols.csv")

        # TestCase: Correct file input
        assert isinstance(code.readfile("sentences.csv"), pd.DataFrame)

    def test_Output(self):
        assert True


if __name__ == "__main__":
    unittest.main()
