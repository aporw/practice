import os
import unittest
import pandas as pd

import ETS_Tech_Screener as code


class TestETS(unittest.TestCase):
    def test_readfile(self):
        # TestCase: File not found
        self.assertRaises(FileNotFoundError, code.readfile, "sample_errored.csv")
        # TestCase: Invalid columns
        self.assertRaises(Exception, code.readfile, "sample_wrongcols.csv")

        # TestCase: Correct file input
        assert isinstance(code.readfile("sentences.csv"), pd.DataFrame)

    def test_tagging(self):
        sentence = "this is for testing"

        assert code.get_tags(sentence) == (
            ["this", "is", "for", "testing"],
            ["DT", "VBZ", "IN", "VBG"],
        )

    def test_preps_idx(self):
        words = ["this", "is", "for", "testing"]
        tags = ["DT", "VBZ", "IN", "VBG"]

        assert code.get_preps_idx(words, tags) == [2]

    def test_features(self):
        sentence = "this is for testing"
        features = list(code.get_features(sentence))

        assert features == [
            (
                "for",
                [
                    "is for",
                    "for testing",
                    "is for testing",
                    "this is for",
                    "for testing",
                    "this is for testing",
                    "VBZ IN",
                    "IN VBG",
                    "VBZ IN VBG",
                    "DT VBZ IN",
                    "IN VBG",
                    "DT VBZ IN VBG",
                ],
            )
        ]

    def test_output(self):
        df = pd.DataFrame({'Id': [1], 'Sentence': ["this is for testing"]})

        outfile = 'sample_test_outfile';
        if os.path.exists(outfile):
            os.remove(outfile)

        code.extract_features(df, outfile)

        with open(outfile) as f:
            out = f.read()

        assert out == """{"id": "1_0", "prep": "for", "features": ["is for", "for testing", "is for testing", "this is for", "for testing", "this is for testing", "VBZ IN", "IN VBG", "VBZ IN VBG", "DT VBZ IN", "IN VBG", "DT VBZ IN VBG"]}\n"""


if __name__ == "__main__":
    unittest.main()
