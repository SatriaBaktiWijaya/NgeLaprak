import os
import unittest
from ngelaprak.core import LaprakDocxBuilder

TEST_OUT_DIR = os.path.join(os.path.dirname(__file__), "test_outputs")
os.makedirs(TEST_OUT_DIR, exist_ok=True)

class TestCore(unittest.TestCase):
    def test_docx_builder(self):
        builder = LaprakDocxBuilder()
        builder.add_section_heading("I. TUJUAN")
        builder.add_paragraph_text("1. Mahasiswa memahami struktur data.")
        
        out_docx = os.path.join(TEST_OUT_DIR, "sample_test.docx")
        res = builder.save(out_docx)
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 500)

if __name__ == "__main__":
    unittest.main()
