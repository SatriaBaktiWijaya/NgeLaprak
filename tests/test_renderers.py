import os
import unittest
from PIL import Image
from ngelaprak.renderers import (
    render_netbeans_code,
    render_codeblocks_code,
    render_vscode_code,
    render_terminal_output,
    frame_windows_gui,
    render_database_query
)

TEST_OUT_DIR = os.path.join(os.path.dirname(__file__), "test_outputs")
os.makedirs(TEST_OUT_DIR, exist_ok=True)

SAMPLE_JAVA = """package com.student.test;

import java.util.List;
import java.util.ArrayList;

/**
 * Sample Javadoc.<p>Testing semantic render.
 * @author Praktikan
 */
public class Sample {
    static final String url = "jdbc:mysql://localhost:3306/test";
    private String nama;

    public Sample(String nama) {
        this.nama = nama;
    }

    @Override
    public String toString() {
        List<String> list = new ArrayList<>();
        list.add(this.nama);
        return url + ":" + nama;
    }
}"""

SAMPLE_CPP = """#include <iostream>
using namespace std;

int main() {
    char grade = 'A';
    cout << "Hello CodeBlocks: " << grade << endl;
    return 0;
}"""


class TestRenderers(unittest.TestCase):
    def test_netbeans_renderer(self):
        out_png = os.path.join(TEST_OUT_DIR, "test_nb.png")
        res = render_netbeans_code("Sample.java", SAMPLE_JAVA, out_path=out_png)
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 5000)
        with Image.open(res) as im:
            self.assertGreater(im.width, 300)
            self.assertGreater(im.height, 200)

    def test_netbeans_full_renderer(self):
        out_png = os.path.join(TEST_OUT_DIR, "test_nb_full.png")
        res = render_netbeans_code(
            "Sample.java",
            SAMPLE_JAVA,
            out_path=out_png,
            view="full",
            project_name="ModulTest",
            extra_files=["Sample.java", "Main.java"],
        )
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 10000)
        with Image.open(res) as im:
            self.assertGreaterEqual(im.width, 900)
            self.assertGreaterEqual(im.height, 550)

    def test_codeblocks_renderer(self):
        out_png = os.path.join(TEST_OUT_DIR, "test_cb.png")
        res = render_codeblocks_code(SAMPLE_CPP, out_path=out_png)
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 3000)
        with Image.open(res) as im:
            self.assertGreater(im.width, 300)
            self.assertGreater(im.height, 100)

    def test_codeblocks_full_renderer(self):
        out_png = os.path.join(TEST_OUT_DIR, "test_cb_full.png")
        res = render_codeblocks_code(
            SAMPLE_CPP,
            out_path=out_png,
            view="full",
            filename="main.cpp",
            project_name="ModulTest",
            extra_files=["main.cpp", "helper.h"],
        )
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 10000)
        with Image.open(res) as im:
            self.assertGreaterEqual(im.width, 900)
            self.assertGreaterEqual(im.height, 500)

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

    def test_database_renderer(self):
        out_png = os.path.join(TEST_OUT_DIR, "test_db.png")
        res = render_database_query(
            "SELECT * FROM test;",
            ["id", "name"],
            [(1, "Alice"), (2, "Bob")],
            out_path=out_png
        )
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 1000)

if __name__ == "__main__":
    unittest.main()
