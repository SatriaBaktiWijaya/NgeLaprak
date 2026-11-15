import os
import sys
import subprocess
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
    # =========================================================================
    # Apache NetBeans 31 Tests (Features 1-8, 17, 18, 20)
    # =========================================================================

    def test_netbeans_renderer(self):
        """Backward compatibility: --view editor generates clean editor snippet."""
        out_png = os.path.join(TEST_OUT_DIR, "test_nb_editor.png")
        res = render_netbeans_code("Sample.java", SAMPLE_JAVA, out_path=out_png, view="editor")
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 5000)
        with Image.open(res) as im:
            self.assertGreater(im.width, 300)
            self.assertGreater(im.height, 200)

    def test_netbeans_full_renderer(self):
        """Default --view full: full window with unified title, toolbar, left split, bottom dock."""
        out_png = os.path.join(TEST_OUT_DIR, "test_nb_full.png")
        res = render_netbeans_code(
            "Sample.java",
            SAMPLE_JAVA,
            out_path=out_png,
            view="full",
            project_name="ModulTest",
            extra_files=["Sample.java", "Main.java"],
            caret_line=1,
            caret_col=1,
            show_bottom_dock=True,
            show_navigator=True,
            scale=1.0,
        )
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 10000)
        with Image.open(res) as im:
            self.assertGreaterEqual(im.width, 900)
            self.assertGreaterEqual(im.height, 550)

    def test_netbeans_hide_bottom_dock(self):
        """NetBeans: --hide-bottom-dock removes bottom output dock, reducing total height."""
        out_full = os.path.join(TEST_OUT_DIR, "test_nb_with_dock.png")
        out_no_dock = os.path.join(TEST_OUT_DIR, "test_nb_no_dock.png")

        render_netbeans_code(
            "Sample.java", SAMPLE_JAVA, out_path=out_full, view="full", show_bottom_dock=True
        )
        render_netbeans_code(
            "Sample.java", SAMPLE_JAVA, out_path=out_no_dock, view="full", show_bottom_dock=False
        )

        with Image.open(out_full) as im_full, Image.open(out_no_dock) as im_no_dock:
            self.assertGreater(im_full.height, im_no_dock.height)

    def test_netbeans_hide_navigator(self):
        """NetBeans: --hide-navigator hides AST navigator panel."""
        out_no_nav = os.path.join(TEST_OUT_DIR, "test_nb_no_nav.png")
        res = render_netbeans_code(
            "Sample.java", SAMPLE_JAVA, out_path=out_no_nav, view="full", show_navigator=False
        )
        self.assertTrue(os.path.exists(res))
        with Image.open(res) as im:
            self.assertGreaterEqual(im.width, 900)
            self.assertGreaterEqual(im.height, 500)

    def test_netbeans_caret_positioning(self):
        """NetBeans: custom caret coordinates (e.g. line 5, col 10)."""
        out_png = os.path.join(TEST_OUT_DIR, "test_nb_caret.png")
        res = render_netbeans_code(
            "Sample.java", SAMPLE_JAVA, out_path=out_png, view="full", caret_line=5, caret_col=10
        )
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 10000)

    def test_netbeans_scale(self):
        """NetBeans: --scale 1.5 scales raster dimensions by 1.5x."""
        out_1x = os.path.join(TEST_OUT_DIR, "test_nb_scale1x.png")
        out_15x = os.path.join(TEST_OUT_DIR, "test_nb_scale15x.png")

        render_netbeans_code("Sample.java", SAMPLE_JAVA, out_path=out_1x, view="full", scale=1.0)
        render_netbeans_code("Sample.java", SAMPLE_JAVA, out_path=out_15x, view="full", scale=1.5)

        with Image.open(out_1x) as im1, Image.open(out_15x) as im15:
            expected_w = int(im1.width * 1.5)
            self.assertAlmostEqual(im15.width, expected_w, delta=5)

    # =========================================================================
    # Code::Blocks 25.03 Tests (Features 9-16, 17, 18, 20)
    # =========================================================================

    def test_codeblocks_renderer(self):
        """Backward compatibility: --view editor generates clean editor snippet."""
        out_png = os.path.join(TEST_OUT_DIR, "test_cb_editor.png")
        res = render_codeblocks_code(SAMPLE_CPP, out_path=out_png, view="editor")
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 3000)
        with Image.open(res) as im:
            self.assertGreater(im.width, 300)
            self.assertGreater(im.height, 100)

    def test_codeblocks_full_renderer(self):
        """Default --view full: full window with 3-row toolbar, 15 menus, clean changebar, 8 status panes."""
        out_png = os.path.join(TEST_OUT_DIR, "test_cb_full.png")
        res = render_codeblocks_code(
            SAMPLE_CPP,
            out_path=out_png,
            view="full",
            filename="main.cpp",
            project_name="ModulTest",
            extra_files=["main.cpp", "helper.h"],
            caret_line=1,
            caret_col=1,
            show_bottom_dock=True,
            show_changebar=False,
            scale=1.0,
        )
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 10000)
        with Image.open(res) as im:
            self.assertGreaterEqual(im.width, 900)
            self.assertGreaterEqual(im.height, 500)

    def test_codeblocks_hide_bottom_dock(self):
        """Code::Blocks: --hide-bottom-dock removes bottom notebook, reducing window height."""
        out_full = os.path.join(TEST_OUT_DIR, "test_cb_with_dock.png")
        out_no_dock = os.path.join(TEST_OUT_DIR, "test_cb_no_dock.png")

        render_codeblocks_code(SAMPLE_CPP, out_path=out_full, view="full", show_bottom_dock=True)
        render_codeblocks_code(SAMPLE_CPP, out_path=out_no_dock, view="full", show_bottom_dock=False)

        with Image.open(out_full) as im_full, Image.open(out_no_dock) as im_no_dock:
            self.assertGreater(im_full.height, im_no_dock.height)

    def test_codeblocks_show_changebar(self):
        """Code::Blocks: --show-changebar enables Scintilla margin 2 green modification marker."""
        out_png = os.path.join(TEST_OUT_DIR, "test_cb_changebar.png")
        res = render_codeblocks_code(
            SAMPLE_CPP, out_path=out_png, view="full", show_changebar=True
        )
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 10000)

    def test_codeblocks_caret_positioning(self):
        """Code::Blocks: custom caret coordinates (e.g. line 3, col 5)."""
        out_png = os.path.join(TEST_OUT_DIR, "test_cb_caret.png")
        res = render_codeblocks_code(
            SAMPLE_CPP, out_path=out_png, view="full", caret_line=3, caret_col=5
        )
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 10000)

    def test_codeblocks_scale(self):
        """Code::Blocks: --scale 1.5 scales raster dimensions proportionally."""
        out_1x = os.path.join(TEST_OUT_DIR, "test_cb_scale1x.png")
        out_15x = os.path.join(TEST_OUT_DIR, "test_cb_scale15x.png")

        render_codeblocks_code(SAMPLE_CPP, out_path=out_1x, view="full", scale=1.0)
        render_codeblocks_code(SAMPLE_CPP, out_path=out_15x, view="full", scale=1.5)

        with Image.open(out_1x) as im1, Image.open(out_15x) as im15:
            expected_w = int(im1.width * 1.5)
            self.assertAlmostEqual(im15.width, expected_w, delta=5)

    # =========================================================================
    # End-to-End CLI Integration Tests (Features 17, 18, 20)
    # =========================================================================

    def test_cli_netbeans_full_flags(self):
        """CLI E2E: NetBeans full view with --caret, --hide-bottom-dock, --scale."""
        src_path = os.path.join(TEST_OUT_DIR, "CLITest.java")
        with open(src_path, "w", encoding="utf-8") as f:
            f.write(SAMPLE_JAVA)

        out_png = os.path.join(TEST_OUT_DIR, "test_cli_nb.png")
        cmd = [
            sys.executable,
            "-m",
            "ngelaprak",
            "render",
            "--ide",
            "netbeans",
            "--view",
            "full",
            "--file",
            src_path,
            "--caret",
            "2:4",
            "--hide-bottom-dock",
            "--scale",
            "1.0",
            "--out",
            out_png,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"CLI stderr: {result.stderr}")
        self.assertTrue(os.path.exists(out_png))
        with Image.open(out_png) as im:
            self.assertGreaterEqual(im.width, 900)

    def test_cli_codeblocks_full_flags(self):
        """CLI E2E: Code::Blocks full view with --caret, --show-changebar, --hide-bottom-dock."""
        src_path = os.path.join(TEST_OUT_DIR, "clitest.cpp")
        with open(src_path, "w", encoding="utf-8") as f:
            f.write(SAMPLE_CPP)

        out_png = os.path.join(TEST_OUT_DIR, "test_cli_cb.png")
        cmd = [
            sys.executable,
            "-m",
            "ngelaprak",
            "render",
            "--ide",
            "codeblocks",
            "--view",
            "full",
            "--file",
            src_path,
            "--caret",
            "3:2",
            "--show-changebar",
            "--hide-bottom-dock",
            "--scale",
            "1.0",
            "--out",
            out_png,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"CLI stderr: {result.stderr}")
        self.assertTrue(os.path.exists(out_png))
        with Image.open(out_png) as im:
            self.assertGreaterEqual(im.width, 900)

    def test_cli_editor_backward_compat(self):
        """CLI E2E: Backward compatibility with --view editor."""
        src_path = os.path.join(TEST_OUT_DIR, "clicompat.cpp")
        with open(src_path, "w", encoding="utf-8") as f:
            f.write(SAMPLE_CPP)

        out_png = os.path.join(TEST_OUT_DIR, "test_cli_cb_editor.png")
        cmd = [
            sys.executable,
            "-m",
            "ngelaprak",
            "render",
            "--ide",
            "codeblocks",
            "--view",
            "editor",
            "--file",
            src_path,
            "--out",
            out_png,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"CLI stderr: {result.stderr}")
        self.assertTrue(os.path.exists(out_png))

    # =========================================================================
    # Supporting Renderers (VS Code, Terminal, Database)
    # =========================================================================

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
