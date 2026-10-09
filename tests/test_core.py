import os
import shutil
import tempfile
import unittest
from ngelaprak.core import (
    LaprakDocxBuilder,
    classify_file,
    infer_workspace_context,
    organize_workspace
)

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

    def test_classify_file(self):
        self.assertEqual(classify_file("Modul 3.pdf"), "modul")
        self.assertEqual(classify_file("TP MODUL 3 STD.pdf"), "tp")
        self.assertEqual(classify_file("STRUKTUR-DATA_MOD-2_109092500017_SatriaBaktiWijaya.pdf"), "laprak")
        self.assertEqual(classify_file("main.cpp"), "code")
        self.assertEqual(classify_file("schema.sql"), "code")
        self.assertEqual(classify_file("screenshot.png"), "screenshot")
        self.assertEqual(classify_file(".gitignore"), "ignore")

    def test_organize_workspace_and_inference(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create loose files
            f_mod = os.path.join(tmp_dir, "Modul 4.pdf")
            f_tp = os.path.join(tmp_dir, "TP MODUL 4.pdf")
            f_lap = os.path.join(tmp_dir, "STRUKTUR-DATA_MOD-3_109092500017_SatriaBaktiWijaya.docx")
            f_code = os.path.join(tmp_dir, "graph.cpp")
            
            with open(f_mod, "w") as f:
                f.write("dummy modul")
            with open(f_tp, "w") as f:
                f.write("dummy tp")
            with open(f_code, "w") as f:
                f.write("// graph implementation in C++\n#include <iostream>\n")

            builder = LaprakDocxBuilder()
            builder.add_section_heading("LAPORAN PRAKTIKUM")
            builder.save(f_lap)

            # Organize
            res = organize_workspace(tmp_dir)
            self.assertTrue(res["scaffolded"])
            self.assertEqual(len(res["moved_files"]), 4)

            # Check directory structure
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "Modul", "Modul 4.pdf")))
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "Modul", "TP MODUL 4.pdf")))
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "Laprak", "STRUKTUR-DATA_MOD-3_109092500017_SatriaBaktiWijaya.docx")))
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "Code", "graph.cpp")))
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "Laprak", "screenshots")))

            # Check context
            ctx = res["context"]
            self.assertEqual(ctx["target_module_number"], 4)
            self.assertEqual(ctx["language"], "C++")
            self.assertEqual(ctx["recommended_ide"], "codeblocks")
            self.assertTrue(ctx["has_code"])
            self.assertEqual(ctx["student_nim"], "109092500017")

if __name__ == "__main__":
    unittest.main()
