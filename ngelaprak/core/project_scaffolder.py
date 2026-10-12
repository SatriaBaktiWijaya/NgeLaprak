import os
import re
import shutil

# ==============================================================================
# 1. Java NetBeans (Maven Project Scaffolder)
# ==============================================================================

POM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>{group_id}</groupId>
    <artifactId>{artifact_id}</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.release>{java_release}</maven.compiler.release>
        <exec.mainClass>{main_class}</exec.mainClass>
    </properties>

    <dependencies>
{dependencies_xml}
    </dependencies>
</project>
"""

NBACTIONS_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<actions>
    <action>
        <actionName>run</actionName>
        <packagings>
            <packaging>jar</packaging>
        </packagings>
        <goals>
            <goal>process-classes</goal>
            <goal>org.codehaus.mojo:exec-maven-plugin:3.5.1:exec</goal>
        </goals>
        <properties>
            <exec.vmArgs>-Xms64m -Xmx256m</exec.vmArgs>
            <exec.args>${{exec.vmArgs}} -classpath %classpath ${{exec.mainClass}} ${{exec.appArgs}}</exec.args>
            <exec.appArgs></exec.appArgs>
            <exec.mainClass>{main_class}</exec.mainClass>
            <exec.executable>java</exec.executable>
        </properties>
    </action>
    <action>
        <actionName>debug</actionName>
        <packagings>
            <packaging>jar</packaging>
        </packagings>
        <goals>
            <goal>process-classes</goal>
            <goal>org.codehaus.mojo:exec-maven-plugin:3.5.1:exec</goal>
        </goals>
        <properties>
            <exec.vmArgs>-Xms64m -Xmx256m -agentlib:jdwp=transport=dt_socket,server=n,address=${{jpda.address}}</exec.vmArgs>
            <exec.args>${{exec.vmArgs}} -classpath %classpath ${{exec.mainClass}} ${{exec.appArgs}}</exec.args>
            <exec.appArgs></exec.appArgs>
            <exec.mainClass>{main_class}</exec.mainClass>
            <exec.executable>java</exec.executable>
            <jpda.listen>true</jpda.listen>
        </properties>
    </action>
</actions>
"""

DEP_MYSQL = """        <!-- MySQL JDBC Connector Driver -->
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <version>8.3.0</version>
        </dependency>"""

def detect_java_package(content):
    """Extracts package declaration from Java source code."""
    m = re.search(r'^\s*package\s+([a-zA-Z0-9_.]+)\s*;', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return None

def detect_java_main_class(content, default_name=None):
    """Detects if file has public static void main and returns class name."""
    if re.search(r'\bpublic\s+static\s+void\s+main\s*\(', content):
        m = re.search(r'\bpublic\s+(?:final\s+)?class\s+([a-zA-Z0-9_]+)', content)
        if m:
            return m.group(1).strip()
        m2 = re.search(r'\bclass\s+([a-zA-Z0-9_]+)', content)
        if m2:
            return m2.group(1).strip()
        if default_name:
            return os.path.splitext(default_name)[0]
    return None

def detect_java_needs_jdbc(all_java_contents):
    """Checks if MySQL / JDBC dependency is needed."""
    combined = " ".join(all_java_contents)
    return any(k in combined for k in [
        "java.sql", "com.mysql", "DriverManager", "ResultSet", "Connection", "Statement", "PreparedStatement"
    ])

def scaffold_java_netbeans_project(code_dir, project_name="modul_project", package_name=None, main_class=None):
    """
    Scaffolds a standard Apache NetBeans Maven Project:
    - Relocates loose .java files into src/main/java/{package_path}/
    - Generates pom.xml with JDK release and auto-detected dependencies (e.g. mysql-connector-j)
    - Generates nbactions.xml for F6 (Run Project) in NetBeans
    """
    code_dir = os.path.abspath(code_dir)
    os.makedirs(code_dir, exist_ok=True)

    # Find all java files
    java_files = []
    for root, _, files in os.walk(code_dir):
        for f in files:
            if f.endswith(".java"):
                java_files.append(os.path.join(root, f))

    all_contents = []
    detected_package = package_name
    detected_main = None

    for jf in java_files:
        try:
            with open(jf, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                all_contents.append(content)
                pkg = detect_java_package(content)
                if pkg and not detected_package:
                    detected_package = pkg
                main_candidate = detect_java_main_class(content, os.path.basename(jf))
                if main_candidate:
                    detected_main = main_candidate
        except Exception:
            pass

    pkg_name = detected_package or "modul"
    pkg_dir_rel = pkg_name.replace(".", "/")
    main_cls_name = detected_main or "Main"
    full_main_class = f"{pkg_name}.{main_cls_name}"

    # Relocate loose .java files directly in code_dir root
    src_java_dir = os.path.join(code_dir, "src", "main", "java", *pkg_name.split("."))
    os.makedirs(src_java_dir, exist_ok=True)

    relocated = []
    for jf in java_files:
        # Check if file is already inside src/main/java/
        norm_jf = os.path.normpath(jf)
        norm_src = os.path.normpath(os.path.join(code_dir, "src", "main", "java"))
        if not norm_jf.startswith(norm_src):
            target_path = os.path.join(src_java_dir, os.path.basename(jf))
            shutil.move(jf, target_path)
            relocated.append(os.path.basename(jf))

    # Dependencies
    deps_list = []
    if detect_java_needs_jdbc(all_contents):
        deps_list.append(DEP_MYSQL)

    deps_xml = "\n".join(deps_list)

    # Clean artifact id
    clean_artifact = re.sub(r'[^a-zA-Z0-9_\-]', '', project_name.lower()) or "modul-project"

    # Write pom.xml if not exists or needs update
    pom_path = os.path.join(code_dir, "pom.xml")
    pom_content = POM_TEMPLATE.format(
        group_id="com.student",
        artifact_id=clean_artifact,
        java_release="25",
        main_class=full_main_class,
        dependencies_xml=deps_xml
    )
    with open(pom_path, "w", encoding="utf-8") as f:
        f.write(pom_content)

    # Write nbactions.xml
    nbactions_path = os.path.join(code_dir, "nbactions.xml")
    nbactions_content = NBACTIONS_TEMPLATE.format(main_class=full_main_class)
    with open(nbactions_path, "w", encoding="utf-8") as f:
        f.write(nbactions_content)

    return {
        "type": "java_netbeans",
        "code_dir": code_dir,
        "package": pkg_name,
        "main_class": full_main_class,
        "pom_path": pom_path,
        "nbactions_path": nbactions_path,
        "src_dir": src_java_dir,
        "relocated_files": relocated
    }


# ==============================================================================
# 2. C / C++ Code::Blocks Project Scaffolder
# ==============================================================================

CBP_TEMPLATE = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<CodeBlocks_project_file>
	<FileVersion major="1" minor="6" />
	<Project>
		<Option title="{project_name}" />
		<Option pch_mode="2" />
		<Option compiler="gcc" />
		<Build>
			<Target title="Debug">
				<Option output="bin/Debug/{clean_name}" prefix_auto="1" extension_auto="1" />
				<Option object_output="obj/Debug/" />
				<Option type="1" />
				<Option compiler="gcc" />
				<Compiler>
					<Add option="-g" />
				</Compiler>
			</Target>
			<Target title="Release">
				<Option output="bin/Release/{clean_name}" prefix_auto="1" extension_auto="1" />
				<Option object_output="obj/Release/" />
				<Option type="1" />
				<Option compiler="gcc" />
				<Compiler>
					<Add option="-O2" />
				</Compiler>
				<Linker>
					<Add option="-s" />
				</Linker>
			</Target>
		</Build>
		<Compiler>
			<Add option="-Wall" />
			<Add option="-fexceptions" />
		</Compiler>
{units_xml}
		<Extensions />
	</Project>
</CodeBlocks_project_file>
"""

def detect_cpp_has_main(file_path):
    """Checks if a C/C++ file contains an entry main function."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            return bool(re.search(r'\bint\s+main\s*\(', content))
    except Exception:
        return False

def generate_cbp_xml(project_name, file_rel_paths):
    """Generates Code::Blocks .cbp XML string."""
    clean_name = re.sub(r'[^a-zA-Z0-9_\-]', '', project_name) or "MainProject"
    units = []
    for rel_p in sorted(file_rel_paths):
        # Normalize to forward slashes for cross-platform XML
        clean_rel = rel_p.replace("\\", "/")
        units.append(f'\t\t<Unit filename="{clean_rel}" />')
    units_xml = "\n".join(units)

    return CBP_TEMPLATE.format(
        project_name=project_name,
        clean_name=clean_name,
        units_xml=units_xml
    )

def scaffold_cpp_codeblocks_project(code_dir, project_name="CppProject"):
    """
    Scaffolds a standard Code::Blocks Project (.cbp):
    - Analyzes .cpp and .h files in code_dir
    - If multiple files contain independent main() functions, handles subprojects
      or generates .cbp for each task so Code::Blocks builds without 'multiple definition of main'.
    - If single project, creates {project_name}.cbp in code_dir root.
    """
    code_dir = os.path.abspath(code_dir)
    os.makedirs(code_dir, exist_ok=True)

    cpp_files = []
    h_files = []
    main_files = []

    for root, _, files in os.walk(code_dir):
        # Ignore build output folders
        if any(b in root for b in ["bin", "obj", ".git"]):
            continue
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            fp = os.path.join(root, f)
            rel_p = os.path.relpath(fp, code_dir)
            if ext in [".cpp", ".c", ".cxx"]:
                cpp_files.append((fp, rel_p))
                if detect_cpp_has_main(fp):
                    main_files.append((fp, rel_p))
            elif ext in [".h", ".hpp"]:
                h_files.append((fp, rel_p))

    created_cbp = []

    # Scenario A: Multiple independent files each having main()
    # In C++, having multiple main() in a single project causes linker error.
    # We create a .cbp for each subfolder or separate task.
    if len(main_files) > 1:
        # Check if already organized in subdirectories
        subdirs_with_main = {}
        for fp, rel_p in main_files:
            parent_rel = os.path.dirname(rel_p)
            subdirs_with_main.setdefault(parent_rel, []).append((fp, rel_p))

        # If they are all loose in code_dir root, organize them into task subfolders
        if "" in subdirs_with_main and len(subdirs_with_main[""]) > 1:
            for fp, rel_p in subdirs_with_main[""]:
                base_name = os.path.splitext(os.path.basename(fp))[0]
                task_dir = os.path.join(code_dir, base_name)
                os.makedirs(task_dir, exist_ok=True)
                new_fp = os.path.join(task_dir, os.path.basename(fp))
                shutil.move(fp, new_fp)

                # Generate .cbp in task_dir
                cbp_path = os.path.join(task_dir, f"{base_name}.cbp")
                cbp_xml = generate_cbp_xml(base_name, [os.path.basename(new_fp)])
                with open(cbp_path, "w", encoding="utf-8") as f:
                    f.write(cbp_xml)
                created_cbp.append(cbp_path)
        else:
            # Files already in subfolders (e.g. soal1/, soal2/) -> generate .cbp inside each
            for sdir, m_list in subdirs_with_main.items():
                if not sdir:
                    continue
                sdir_abs = os.path.join(code_dir, sdir)
                dir_name = os.path.basename(sdir_abs)
                dir_files = [f for f in os.listdir(sdir_abs) if os.path.splitext(f)[1].lower() in [".cpp", ".c", ".h", ".hpp"]]
                cbp_path = os.path.join(sdir_abs, f"{dir_name}.cbp")
                cbp_xml = generate_cbp_xml(dir_name, dir_files)
                with open(cbp_path, "w", encoding="utf-8") as f:
                    f.write(cbp_xml)
                created_cbp.append(cbp_path)

    # Scenario B: Single project (1 main or purely modular headers + cpp)
    else:
        all_rel = [rel_p for _, rel_p in cpp_files + h_files]
        if not all_rel:
            # Create placeholder main.cpp if empty
            placeholder = os.path.join(code_dir, "main.cpp")
            if not os.path.exists(placeholder):
                with open(placeholder, "w", encoding="utf-8") as f:
                    f.write('#include <iostream>\n\nusing namespace std;\n\nint main() {\n    cout << "Hello Code::Blocks!" << endl;\n    return 0;\n}\n')
                all_rel.append("main.cpp")

        cbp_path = os.path.join(code_dir, f"{project_name}.cbp")
        cbp_xml = generate_cbp_xml(project_name, all_rel)
        with open(cbp_path, "w", encoding="utf-8") as f:
            f.write(cbp_xml)
        created_cbp.append(cbp_path)

    return {
        "type": "cpp_codeblocks",
        "code_dir": code_dir,
        "created_cbp": created_cbp
    }


# ==============================================================================
# 3. Universal Auto-Scaffolder Entrypoint
# ==============================================================================

def auto_scaffold_code_directory(code_dir, language=None, project_name="ProjekPraktikum"):
    """
    Automatically detects language (Java vs C++) and scaffolds the proper IDE project structure:
    - Java -> Apache NetBeans Maven Project (pom.xml, nbactions.xml, src/main/java/{pkg}/)
    - C/C++ -> Code::Blocks Project (.cbp)
    """
    code_dir = os.path.abspath(code_dir)
    os.makedirs(code_dir, exist_ok=True)

    # Detect language from existing files if language not specified
    if not language:
        has_java = False
        has_cpp = False
        for root, _, files in os.walk(code_dir):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext == ".java":
                    has_java = True
                elif ext in [".cpp", ".c", ".h", ".hpp", ".cbp"]:
                    has_cpp = True

        if has_java:
            language = "Java"
        elif has_cpp:
            language = "C++"

    lang_upper = (language or "").upper()

    if "JAVA" in lang_upper:
        return scaffold_java_netbeans_project(code_dir, project_name=project_name)
    elif "C++" in lang_upper or "CPP" in lang_upper or "C" in lang_upper:
        return scaffold_cpp_codeblocks_project(code_dir, project_name=project_name)
    else:
        return {"type": "none", "code_dir": code_dir}
