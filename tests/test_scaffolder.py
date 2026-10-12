import os
import shutil
import tempfile
import unittest
from ngelaprak.core import (
    scaffold_java_netbeans_project,
    scaffold_cpp_codeblocks_project,
    auto_scaffold_code_directory
)

class TestScaffolder(unittest.TestCase):
    def test_java_scaffolding(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create loose java files in tmp_dir
            app_java = os.path.join(tmp_dir, "App.java")
            helper_java = os.path.join(tmp_dir, "Helper.java")
            with open(app_java, "w", encoding="utf-8") as f:
                f.write("package com.test.modul;\n\npublic class App {\n    public static void main(String[] args) {}\n}\n")
            with open(helper_java, "w", encoding="utf-8") as f:
                f.write("package com.test.modul;\nimport java.sql.Connection;\n\npublic class Helper {}\n")

            res = scaffold_java_netbeans_project(tmp_dir, project_name="TestApp")
            self.assertEqual(res["type"], "java_netbeans")
            self.assertEqual(res["package"], "com.test.modul")
            self.assertEqual(res["main_class"], "com.test.modul.App")

            # Check files created
            pom_path = os.path.join(tmp_dir, "pom.xml")
            nbactions_path = os.path.join(tmp_dir, "nbactions.xml")
            self.assertTrue(os.path.exists(pom_path))
            self.assertTrue(os.path.exists(nbactions_path))

            # Verify pom content
            with open(pom_path, "r", encoding="utf-8") as f:
                pom_txt = f.read()
                self.assertIn("mysql-connector-j", pom_txt)
                self.assertIn("<exec.mainClass>com.test.modul.App</exec.mainClass>", pom_txt)

            # Verify files were relocated to src/main/java/com/test/modul/
            expected_src_app = os.path.join(tmp_dir, "src", "main", "java", "com", "test", "modul", "App.java")
            expected_src_helper = os.path.join(tmp_dir, "src", "main", "java", "com", "test", "modul", "Helper.java")
            self.assertTrue(os.path.exists(expected_src_app))
            self.assertTrue(os.path.exists(expected_src_helper))

            # Root should not have loose java files anymore
            self.assertFalse(os.path.exists(app_java))
            self.assertFalse(os.path.exists(helper_java))

    def test_cpp_scaffolding_single_project(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            main_cpp = os.path.join(tmp_dir, "main.cpp")
            calc_h = os.path.join(tmp_dir, "calc.h")
            calc_cpp = os.path.join(tmp_dir, "calc.cpp")

            with open(main_cpp, "w", encoding="utf-8") as f:
                f.write('#include <iostream>\n#include "calc.h"\nint main() { return 0; }\n')
            with open(calc_h, "w", encoding="utf-8") as f:
                f.write('#ifndef CALC_H\n#define CALC_H\nint add(int a, int b);\n#endif\n')
            with open(calc_cpp, "w", encoding="utf-8") as f:
                f.write('#include "calc.h"\nint add(int a, int b) { return a + b; }\n')

            res = scaffold_cpp_codeblocks_project(tmp_dir, project_name="StrukdatProject")
            self.assertEqual(res["type"], "cpp_codeblocks")
            self.assertEqual(len(res["created_cbp"]), 1)

            cbp_file = os.path.join(tmp_dir, "StrukdatProject.cbp")
            self.assertTrue(os.path.exists(cbp_file))
            with open(cbp_file, "r", encoding="utf-8") as f:
                cbp_txt = f.read()
                self.assertIn('<Unit filename="main.cpp" />', cbp_txt)
                self.assertIn('<Unit filename="calc.h" />', cbp_txt)
                self.assertIn('<Unit filename="calc.cpp" />', cbp_txt)

    def test_cpp_scaffolding_multi_main(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            soal1 = os.path.join(tmp_dir, "soal1.cpp")
            soal2 = os.path.join(tmp_dir, "soal2.cpp")

            with open(soal1, "w", encoding="utf-8") as f:
                f.write('int main() { return 0; }\n')
            with open(soal2, "w", encoding="utf-8") as f:
                f.write('int main() { return 1; }\n')

            res = scaffold_cpp_codeblocks_project(tmp_dir, project_name="Latihan")
            self.assertEqual(res["type"], "cpp_codeblocks")
            self.assertEqual(len(res["created_cbp"]), 2)

            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "soal1", "soal1.cbp")))
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "soal2", "soal2.cbp")))
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "soal1", "soal1.cpp")))
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "soal2", "soal2.cpp")))

    def test_auto_scaffold_entrypoint(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            f = os.path.join(tmp_dir, "Test.java")
            with open(f, "w") as fp:
                fp.write("package demo; public class Test { public static void main(String[] args) {} }")
            res = auto_scaffold_code_directory(tmp_dir)
            self.assertEqual(res["type"], "java_netbeans")
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "pom.xml")))

if __name__ == "__main__":
    unittest.main()
