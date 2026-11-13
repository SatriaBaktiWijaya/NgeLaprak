import glob
import os
import random
import subprocess


_RENDERER_DIR = os.path.dirname(os.path.abspath(__file__))
_JAVA_SRC = os.path.join(_RENDERER_DIR, "NetBeansNativeRenderer.java")
_BIN_DIR = os.path.join(_RENDERER_DIR, "nb_bin")
_CLASS_FILE = os.path.join(_BIN_DIR, "NetBeansNativeRenderer.class")


def _find_netbeans_home():
    candidates = []
    env_home = os.environ.get("NETBEANS_HOME")
    if env_home:
        candidates.append(env_home)
    candidates.append(r"C:\Program Files\Apache NetBeans")
    candidates.extend(sorted(glob.glob(r"C:\Program Files\*NetBeans*"), reverse=True))
    candidates.extend(sorted(glob.glob(r"C:\Program Files (x86)\*NetBeans*"), reverse=True))
    for path in candidates:
        if path and os.path.isdir(path):
            return path
    return None


def _build_classpath(nb_home):
    cp_entries = [_BIN_DIR]
    if nb_home:
        ext_dir = os.path.join(nb_home, "platform", "modules", "ext")
        for pattern in ("flatlaf-*.jar", "jsvg-*.jar"):
            matches = sorted(glob.glob(os.path.join(ext_dir, pattern)), reverse=True)
            if matches:
                cp_entries.append(matches[0])
    return os.pathsep.join(cp_entries)


def _ensure_compiled():
    if not os.path.exists(_JAVA_SRC):
        raise FileNotFoundError(f"NetBeansNativeRenderer.java tidak ditemukan: {_JAVA_SRC}")
    os.makedirs(_BIN_DIR, exist_ok=True)
    need_compile = not os.path.exists(_CLASS_FILE) or (
        os.path.getmtime(_JAVA_SRC) > os.path.getmtime(_CLASS_FILE)
    )
    if need_compile:
        res = subprocess.run(
            ["javac", "-encoding", "UTF-8", "-d", _BIN_DIR, _JAVA_SRC],
            capture_output=True,
            text=True,
        )
        if res.returncode != 0:
            raise RuntimeError(f"Gagal mengompilasi NetBeansNativeRenderer.java:\n{res.stderr or res.stdout}")


def render_netbeans_code(
    filename,
    code_text,
    start_line=1,
    end_line=None,
    out_path="netbeans_shot.png",
    active_line_offset=None,
    with_margin_guide=True,
    with_cursor=True,
    author_tag=None,
    view="editor",
    project_name="ProjekPraktikum",
    extra_files=None,
    sourcepath=None,
):
    """
    Renders a 100% pixel-perfect Apache NetBeans 31 (FlatLaf Light) screenshot using:
    - Real JDK javac Compiler Tree API (semantic field/static/override/warning resolution)
    - Real Java2D LCD_HRGB subpixel text rendering & official NetBeans JAR SVG/PNG assets
    - Real Swing + FlatLightLaf chrome when view='full'
    """
    _ensure_compiled()

    out_path = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    if not code_text:
        code_text = "\n"
    if author_tag and start_line == 1 and not code_text.strip().startswith("//"):
        code_text = f"// @author {author_tag}\n" + code_text

    nb_home = _find_netbeans_home()
    cp = _build_classpath(nb_home)

    cmd = [
        "java",
        "-Dfile.encoding=UTF-8",
        "-cp",
        cp,
        "NetBeansNativeRenderer",
        "--filename",
        os.path.basename(filename) if filename else "Main.java",
        "--out",
        out_path,
        "--start",
        str(start_line),
        "--view",
        view if view in ("editor", "full") else "editor",
        "--project",
        project_name or "ProjekPraktikum",
        "--cursor",
        "true" if with_cursor else "false",
        "--margin-guide",
        "true" if with_margin_guide else "false",
        "--jitter-w",
        str(random.randint(18, 55)),
        "--jitter-h",
        str(random.randint(4, 18)),
    ]

    if end_line is not None:
        cmd.extend(["--end", str(end_line)])
    if active_line_offset is not None:
        cmd.extend(["--active-offset", str(active_line_offset)])
    if sourcepath and os.path.exists(sourcepath):
        cmd.extend(["--sourcepath", os.path.abspath(sourcepath)])
    if extra_files:
        cmd.extend(["--extra-files", ",".join(extra_files)])
    if nb_home:
        cmd.extend(["--nb-home", nb_home])

    res = subprocess.run(
        cmd,
        input=code_text.encode("utf-8"),
        capture_output=True,
    )
    if res.returncode != 0:
        err = res.stderr.decode("utf-8", errors="replace") or res.stdout.decode("utf-8", errors="replace")
        raise RuntimeError(f"NetBeansNativeRenderer gagal:\n{err}")

    return out_path
