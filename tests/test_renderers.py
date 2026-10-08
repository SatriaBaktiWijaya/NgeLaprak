import os
import unittest
from ngelaprak.renderers import (
    render_netbeans_code,
    render_codeblocks_code,
    render_vscode_code,
    render_terminal_output,
    frame_windows_gui
)

TEST_OUT_DIR = os.path.join(os.path.dirname(__file__), "test_outputs")
os.makedirs(TEST_OUT_DIR, exist_ok=True)

class TestRenderers(unittest.TestCase):
    def test_netbeans_renderer(self):
        sample_java = """package com.student.test;

public class Sample {
    static final String url = "jdbc:mysql://localhost:3306/test";
    public static void main(String[] args) {
        System.out.println("Hello Test");
    }
}"""
        out_png = os.path.join(TEST_OUT_DIR, "test_nb.png")
        res = render_netbeans_code("Sample.java", sample_java, out_path=out_png)
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 1000)

    def test_codeblocks_renderer(self):
        sample_cpp = """#include <iostream>
using namespace std;

int main() {
    cout << "Hello CodeBlocks" << endl;
    return 0;
}"""
        out_png = os.path.join(TEST_OUT_DIR, "test_cb.png")
        res = render_codeblocks_code(sample_cpp, out_path=out_png)
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 1000)

    def test_vscode_renderer(self):
        sample_py = """def calculate_total(items):
    total = 0
    for item in items:
        total += item['price']
    return total"""
        out_png = os.path.join(TEST_OUT_DIR, "test_vsc.png")
        res = render_vscode_code(sample_py, out_path=out_png)
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 1000)

    def test_terminal_renderer(self):
        sample_lines = ["mysql> SELECT * FROM users;", "1 row in set (0.01 sec)"]
        out_png = os.path.join(TEST_OUT_DIR, "test_term.png")
        res = render_terminal_output("MySQL 8.0 Client", sample_lines, out_path=out_png)
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 1000)

if __name__ == "__main__":
    unittest.main()
