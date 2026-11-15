import java.awt.*;
import java.awt.geom.*;
import java.awt.image.BufferedImage;
import java.io.*;
import java.lang.reflect.Method;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.List;
import java.util.jar.JarFile;
import java.util.zip.ZipEntry;
import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.border.*;
import javax.swing.tree.*;
import javax.tools.*;
import javax.lang.model.element.*;
import com.sun.source.tree.*;
import com.sun.source.util.*;

public class NetBeansNativeRenderer {

    private static final String DEFAULT_NB_HOME = "C:\\Program Files\\Apache NetBeans";

    // FlatLaf Light Official Palette (from FlatLafLight-tokenColorings.xml & FlatLafLight-highlights.xml)
    private static final Color COL_BG = Color.WHITE;
    private static final Color COL_FG = Color.BLACK;
    private static final Color COL_CARET_ROW = new Color(0xF9, 0xF4, 0xE0);
    private static final Color COL_GUTTER_BG = new Color(0xE9, 0xE8, 0xE2);
    private static final Color COL_GUTTER_BORDER = new Color(0xD6, 0xD5, 0xCE);
    private static final Color COL_LINE_NUM = new Color(0x6E, 0x6E, 0x6E);
    private static final Color COL_FOLD_BAR = new Color(0x8C, 0x8C, 0x8C);
    private static final Color COL_INDENT_GUIDE = new Color(0xD3, 0xD3, 0xD3);
    private static final Color COL_TEXT_LIMIT = new Color(0xE2, 0xE2, 0xE2); // Subtle gray margin guide at column 80

    private static final Color COL_KEYWORD = new Color(0x33, 0x6B, 0xDD);
    private static final Color COL_STRING = new Color(0x1E, 0x93, 0x47);
    private static final Color COL_COMMENT = new Color(0x96, 0x96, 0x96);
    private static final Color COL_FIELD = new Color(0xCE, 0x54, 0xB8);
    private static final Color COL_HTML_TAG = new Color(0x99, 0x99, 0xFF);
    private static final Color COL_UNUSED_WAVE = new Color(0x99, 0x99, 0x99);
    private static final Color COL_WARN_WAVE = new Color(0xFF, 0xA5, 0x00);

    private static final Set<String> JAVA_KEYWORDS = new HashSet<>(Arrays.asList(
        "abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class", "const",
        "continue", "default", "do", "double", "else", "enum", "extends", "final", "finally", "float",
        "for", "goto", "if", "implements", "import", "instanceof", "int", "interface", "long", "native",
        "new", "package", "private", "protected", "public", "return", "short", "static", "strictfp",
        "super", "switch", "synchronized", "this", "throw", "throws", "transient", "try", "void",
        "volatile", "while", "true", "false", "null", "var", "record", "sealed", "permits", "yield"
    ));

    static class MemberItem {
        enum Kind { CLASS, CONSTRUCTOR, METHOD, FIELD }
        Kind kind;
        String name;
        String returnType; // null/empty for void or constructor
        String params;     // e.g. "Transaksi t"
        String type;       // for field: type
        boolean isStatic;
        boolean isPrivate;
        boolean isProtected;
        boolean isPublic = true;

        public String getDisplayLabel() {
            if (kind == Kind.CLASS) return name;
            if (kind == Kind.CONSTRUCTOR) return name + "(" + (params != null ? params : "") + ")";
            if (kind == Kind.METHOD) {
                String p = params != null ? params : "";
                if (returnType == null || returnType.isEmpty() || "void".equalsIgnoreCase(returnType)) {
                    return name + "(" + p + ")";
                } else {
                    return name + "(" + p + ") : " + returnType;
                }
            }
            if (kind == Kind.FIELD) {
                return name + (type != null && !type.isEmpty() ? " : " + type : "");
            }
            return name;
        }
    }

    static class AnalysisResult {
        Color[] fg;
        boolean[] bold;
        boolean[] italic;
        Color[] wave;
        Set<Integer> foldStartLines = new HashSet<>();
        Map<Integer, Integer> foldPairs = new LinkedHashMap<>();
        Set<Integer> overrideLines = new HashSet<>();
        Set<Integer> warningLines = new HashSet<>();
        String packageName = "";
        String className = "";
        boolean hasMain = false;
        List<MemberItem> members = new ArrayList<>();
    }

    public static void main(String[] args) throws Exception {
        Map<String, String> opts = parseArgs(args);
        String filePath = opts.get("file");
        String outPath = opts.getOrDefault("out", "netbeans_shot.png");
        String filename = opts.getOrDefault("filename", filePath != null ? new File(filePath).getName() : "Main.java");
        int startLine = Integer.parseInt(opts.getOrDefault("start", "1"));
        int endLine = Integer.parseInt(opts.getOrDefault("end", "-1"));

        // Caret position defaults to line 1 col 1 per specification
        int caretLine = Integer.parseInt(opts.getOrDefault("caret-line", "1"));
        int caretCol = Integer.parseInt(opts.getOrDefault("caret-col", "1"));
        if (opts.containsKey("active-offset")) {
            int activeOffset = Integer.parseInt(opts.get("active-offset"));
            if (activeOffset >= 0) {
                caretLine = startLine + activeOffset;
            }
        }

        boolean withCursor = Boolean.parseBoolean(opts.getOrDefault("cursor", "true"));
        boolean withMarginGuide = Boolean.parseBoolean(opts.getOrDefault("margin-guide", "true"));
        boolean showBottomDock = Boolean.parseBoolean(opts.getOrDefault("show-bottom-dock", "true"));
        boolean showNavigator = Boolean.parseBoolean(opts.getOrDefault("show-navigator", "true"));
        String view = opts.getOrDefault("view", "editor");
        String projectName = opts.getOrDefault("project", "ProjekPraktikum");
        String sourcePath = opts.getOrDefault("sourcepath", "");
        String extraFilesRaw = opts.getOrDefault("extra-files", "");
        String nbHome = opts.getOrDefault("nb-home", DEFAULT_NB_HOME);
        int jitterW = Integer.parseInt(opts.getOrDefault("jitter-w", "32"));
        int jitterH = Integer.parseInt(opts.getOrDefault("jitter-h", "6"));

        double defaultScale = "full".equalsIgnoreCase(view) ? 1.0 : 1.5;
        double scale = Double.parseDouble(opts.getOrDefault("scale", String.valueOf(defaultScale)));

        String code;
        if (filePath != null && !filePath.isEmpty()) {
            code = Files.readString(Path.of(filePath), StandardCharsets.UTF_8);
        } else {
            code = new String(System.in.readAllBytes(), StandardCharsets.UTF_8);
        }
        code = code.replace("\r\n", "\n").replace("\r", "\n");

        AnalysisResult ar = analyzeJava(code, filename, sourcePath);

        if ("full".equalsIgnoreCase(view)) {
            List<String> extraFiles = new ArrayList<>();
            if (!extraFilesRaw.isEmpty()) {
                for (String s : extraFilesRaw.split(",")) {
                    if (!s.trim().isEmpty()) extraFiles.add(s.trim());
                }
            }
            if (!extraFiles.contains(filename)) extraFiles.add(0, filename);
            renderFullWindow(
                code, ar, filename, projectName, extraFiles,
                startLine, endLine, caretLine, caretCol, withCursor, withMarginGuide,
                showBottomDock, showNavigator, scale, jitterW, jitterH, nbHome, new File(outPath)
            );
        } else {
            renderEditorOnly(
                code, ar, startLine, endLine, caretLine, caretCol,
                withCursor, withMarginGuide, scale, jitterW, jitterH, nbHome, new File(outPath)
            );
        }
    }

    private static Map<String, String> parseArgs(String[] args) {
        Map<String, String> map = new HashMap<>();
        for (int i = 0; i < args.length; i++) {
            if (args[i].startsWith("--") && i + 1 < args.length) {
                map.put(args[i].substring(2), args[i + 1]);
                i++;
            }
        }
        return map;
    }

    private static AnalysisResult analyzeJava(String code, String filename, String sourcePath) {
        AnalysisResult ar = new AnalysisResult();
        int len = code.length();
        ar.fg = new Color[len];
        ar.bold = new boolean[len];
        ar.italic = new boolean[len];
        ar.wave = new Color[len];
        Arrays.fill(ar.fg, COL_FG);

        // 1. Lexical token pass (comments, Javadoc tags, strings, escapes, keywords)
        int idx = 0;
        while (idx < len) {
            char c = code.charAt(idx);
            if (c == '/' && idx + 1 < len && code.charAt(idx + 1) == '/') {
                int end = code.indexOf('\n', idx);
                if (end == -1) end = len;
                for (int k = idx; k < end; k++) ar.fg[k] = COL_COMMENT;
                idx = end;
            } else if (c == '/' && idx + 1 < len && code.charAt(idx + 1) == '*') {
                boolean isJavadoc = idx + 2 < len && code.charAt(idx + 2) == '*';
                int end = code.indexOf("*/", idx + 2);
                if (end == -1) end = len; else end += 2;
                for (int k = idx; k < end; k++) ar.fg[k] = COL_COMMENT;
                if (isJavadoc) {
                    highlightJavadocSubtokens(code, idx, end, ar);
                }
                int sLine = 0;
                for (int k = 0; k < idx; k++) if (code.charAt(k) == '\n') sLine++;
                int eLine = sLine;
                for (int k = idx; k < end; k++) if (code.charAt(k) == '\n') eLine++;
                if (eLine > sLine) {
                    ar.foldStartLines.add(sLine);
                    ar.foldPairs.put(sLine, eLine);
                }
                idx = end;
            } else if (c == '"' || c == '\'') {
                char quote = c;
                // Check Java text block """
                if (quote == '"' && idx + 2 < len && code.charAt(idx + 1) == '"' && code.charAt(idx + 2) == '"') {
                    int end = code.indexOf("\"\"\"", idx + 3);
                    if (end == -1) end = len; else end += 3;
                    for (int k = idx; k < end; k++) ar.fg[k] = COL_STRING;
                    idx = end;
                } else {
                    int end = idx + 1;
                    while (end < len) {
                        if (code.charAt(end) == '\\') {
                            end += 2;
                        } else if (code.charAt(end) == quote) {
                            end++;
                            break;
                        } else if (code.charAt(end) == '\n') {
                            break;
                        } else {
                            end++;
                        }
                    }
                    int lim = Math.min(end, len);
                    for (int k = idx; k < lim; k++) {
                        ar.fg[k] = COL_STRING;
                        if (code.charAt(k) == '\\' && k + 1 < lim) {
                            ar.bold[k] = true;
                            ar.bold[k + 1] = true;
                        }
                    }
                    idx = end;
                }
            } else if (Character.isJavaIdentifierStart(c)) {
                int end = idx + 1;
                while (end < len && Character.isJavaIdentifierPart(code.charAt(end))) end++;
                String word = code.substring(idx, end);
                if (JAVA_KEYWORDS.contains(word)) {
                    for (int k = idx; k < end; k++) ar.fg[k] = COL_KEYWORD;
                }
                idx = end;
            } else {
                idx++;
            }
        }

        // 2. Real javac Compiler AST + Semantic Analysis
        Set<String> declaredFields = new HashSet<>();
        Set<String> declaredStaticFields = new HashSet<>();
        Set<String> declaredStaticMethods = new HashSet<>();

        try {
            JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
            if (compiler != null) {
                DiagnosticCollector<JavaFileObject> diags = new DiagnosticCollector<>();
                String cleanName = filename.endsWith(".java") ? filename : filename + ".java";
                SimpleJavaFileObject fileObj = new SimpleJavaFileObject(URI.create("string:///" + cleanName), JavaFileObject.Kind.SOURCE) {
                    @Override
                    public CharSequence getCharContent(boolean ignoreEncodingErrors) {
                        return code;
                    }
                };
                List<String> javacOpts = new ArrayList<>();
                javacOpts.add("-proc:none");
                if (sourcePath != null && !sourcePath.isEmpty() && new File(sourcePath).exists()) {
                    javacOpts.add("-sourcepath");
                    javacOpts.add(sourcePath);
                }

                JavacTask task = (JavacTask) compiler.getTask(new StringWriter(), null, diags, javacOpts, null, List.of(fileObj));
                Iterable<? extends CompilationUnitTree> asts = task.parse();
                try { task.analyze(); } catch (Exception ignored) {}
                Trees trees = Trees.instance(task);

                // Collect package, declared fields, static methods & members for Navigator
                for (CompilationUnitTree cu : asts) {
                    if (cu.getPackageName() != null) {
                        ar.packageName = cu.getPackageName().toString();
                    }
                }

                for (CompilationUnitTree cu : asts) {
                    LineMap lineMap = cu.getLineMap();
                    SourcePositions pos = trees.getSourcePositions();

                    // First pass: collect class-level fields, static methods, and member structure for Navigator
                    new TreePathScanner<Void, Void>() {
                        @Override
                        public Void visitClass(ClassTree node, Void p) {
                            if (ar.className.isEmpty()) ar.className = node.getSimpleName().toString();
                            MemberItem classItem = new MemberItem();
                            classItem.kind = MemberItem.Kind.CLASS;
                            classItem.name = node.getSimpleName().toString();
                            ar.members.add(classItem);

                            for (Tree member : node.getMembers()) {
                                if (member instanceof MethodTree) {
                                    MethodTree mt = (MethodTree) member;
                                    String mName = mt.getName().toString();
                                    MemberItem mItem = new MemberItem();
                                    mItem.isStatic = mt.getModifiers().getFlags().contains(Modifier.STATIC);
                                    mItem.isPrivate = mt.getModifiers().getFlags().contains(Modifier.PRIVATE);
                                    mItem.isProtected = mt.getModifiers().getFlags().contains(Modifier.PROTECTED);
                                    mItem.isPublic = mt.getModifiers().getFlags().contains(Modifier.PUBLIC) || (!mItem.isPrivate && !mItem.isProtected);

                                    StringBuilder sb = new StringBuilder();
                                    for (VariableTree vt : mt.getParameters()) {
                                        if (sb.length() > 0) sb.append(", ");
                                        sb.append(vt.getType() != null ? vt.getType().toString() : "Object")
                                          .append(" ")
                                          .append(vt.getName().toString());
                                    }
                                    mItem.params = sb.toString();

                                    if ("<init>".equals(mName)) {
                                        mItem.kind = MemberItem.Kind.CONSTRUCTOR;
                                        mItem.name = classItem.name.isEmpty() ? "Constructor" : classItem.name;
                                        mItem.returnType = null;
                                    } else {
                                        mItem.kind = MemberItem.Kind.METHOD;
                                        mItem.name = mName;
                                        mItem.returnType = mt.getReturnType() != null ? mt.getReturnType().toString() : "void";
                                    }
                                    ar.members.add(mItem);
                                } else if (member instanceof VariableTree) {
                                    VariableTree vt = (VariableTree) member;
                                    MemberItem fItem = new MemberItem();
                                    fItem.kind = MemberItem.Kind.FIELD;
                                    fItem.name = vt.getName().toString();
                                    fItem.type = vt.getType() != null ? vt.getType().toString() : "";
                                    fItem.isStatic = vt.getModifiers().getFlags().contains(Modifier.STATIC);
                                    fItem.isPrivate = vt.getModifiers().getFlags().contains(Modifier.PRIVATE);
                                    fItem.isProtected = vt.getModifiers().getFlags().contains(Modifier.PROTECTED);
                                    fItem.isPublic = vt.getModifiers().getFlags().contains(Modifier.PUBLIC) || (!fItem.isPrivate && !fItem.isProtected);
                                    ar.members.add(fItem);
                                }
                            }
                            return super.visitClass(node, p);
                        }

                        @Override
                        public Void visitVariable(VariableTree node, Void p) {
                            Tree parent = getCurrentPath().getParentPath().getLeaf();
                            if (parent instanceof ClassTree) {
                                String fn = node.getName().toString();
                                declaredFields.add(fn);
                                if (node.getModifiers().getFlags().contains(Modifier.STATIC)) {
                                    declaredStaticFields.add(fn);
                                }
                            }
                            return super.visitVariable(node, p);
                        }

                        @Override
                        public Void visitMethod(MethodTree node, Void p) {
                            String mn = node.getName().toString();
                            if ("main".equals(mn)) ar.hasMain = true;
                            if (node.getModifiers().getFlags().contains(Modifier.STATIC)) {
                                declaredStaticMethods.add(mn);
                            }
                            return super.visitMethod(node, p);
                        }
                    }.scan(cu, null);

                    // Second pass: apply NetBeans semantic coloring and gutter annotations
                    new TreePathScanner<Void, Void>() {
                        private void registerFold(Tree node) {
                            long s = pos.getStartPosition(cu, node);
                            long e = pos.getEndPosition(cu, node);
                            if (s >= 0 && e > s) {
                                int sLine = (int) lineMap.getLineNumber(s) - 1;
                                int eLine = (int) lineMap.getLineNumber(e) - 1;
                                if (eLine > sLine) {
                                    ar.foldStartLines.add(sLine);
                                    ar.foldPairs.put(sLine, eLine);
                                }
                            }
                        }

                        @Override
                        public Void visitClass(ClassTree node, Void p) {
                            registerFold(node);
                            return super.visitClass(node, p);
                        }

                        @Override
                        public Void visitMethod(MethodTree node, Void p) {
                            registerFold(node);
                            boolean isStatic = node.getModifiers().getFlags().contains(Modifier.STATIC);
                            boolean hasOverride = false;
                            for (AnnotationTree ann : node.getModifiers().getAnnotations()) {
                                if (ann.getAnnotationType().toString().endsWith("Override")) {
                                    hasOverride = true;
                                }
                            }
                            if (hasOverride) {
                                long ms = pos.getStartPosition(cu, node);
                                if (ms >= 0) {
                                    String mSlice = code.substring((int) ms, (int) Math.min(pos.getEndPosition(cu, node), len));
                                    int parenIdx = mSlice.indexOf('(');
                                    int namePos = parenIdx > 0 ? mSlice.lastIndexOf(node.getName().toString(), parenIdx) : 0;
                                    long badgeOffset = ms + Math.max(0, namePos);
                                    int mLine = (int) lineMap.getLineNumber(badgeOffset) - 1;
                                    ar.overrideLines.add(mLine);
                                }
                            }

                            String name = node.getName().toString();
                            if (name.equals("<init>")) {
                                Tree parent = getCurrentPath().getParentPath().getLeaf();
                                if (parent instanceof ClassTree) {
                                    name = ((ClassTree) parent).getSimpleName().toString();
                                }
                            }
                            long bodyStart = node.getBody() != null ? pos.getStartPosition(cu, node.getBody()) : pos.getEndPosition(cu, node);
                            long start = pos.getStartPosition(cu, node);
                            if (start >= 0 && bodyStart > start) {
                                String header = code.substring((int) start, (int) Math.min(bodyStart, len));
                                int idxParen = header.indexOf('(');
                                if (idxParen > 0) {
                                    int nameIdx = header.lastIndexOf(name, idxParen);
                                    if (nameIdx >= 0) {
                                        int s = (int) start + nameIdx;
                                        for (int k = s; k < s + name.length(); k++) {
                                            ar.bold[k] = true;
                                            if (isStatic) ar.italic[k] = true;
                                        }
                                    }
                                }
                            }
                            return super.visitMethod(node, p);
                        }

                        @Override
                        public Void visitVariable(VariableTree node, Void p) {
                            Element el = trees.getElement(getCurrentPath());
                            Tree parent = getCurrentPath().getParentPath().getLeaf();
                            boolean isField = (parent instanceof ClassTree) || (el != null && el.getKind().isField());
                            boolean isStatic = node.getModifiers().getFlags().contains(Modifier.STATIC)
                                    || (el != null && el.getModifiers().contains(Modifier.STATIC));
                            if (isField) {
                                long s = pos.getStartPosition(cu, node);
                                long e = node.getInitializer() != null ? pos.getStartPosition(cu, node.getInitializer()) : pos.getEndPosition(cu, node);
                                if (s >= 0 && e > s) {
                                    String decl = code.substring((int) s, (int) Math.min(e, len));
                                    String vname = node.getName().toString();
                                    int rel = decl.lastIndexOf(vname);
                                    if (rel >= 0) {
                                        int abs = (int) s + rel;
                                        for (int k = abs; k < abs + vname.length(); k++) {
                                            ar.fg[k] = COL_FIELD;
                                            if (isStatic) ar.italic[k] = true;
                                        }
                                    }
                                }
                            }
                            return super.visitVariable(node, p);
                        }

                        @Override
                        public Void visitIdentifier(IdentifierTree node, Void p) {
                            Element el = trees.getElement(getCurrentPath());
                            String name = node.getName().toString();
                            long s = pos.getStartPosition(cu, node);
                            long e = pos.getEndPosition(cu, node);
                            if (s >= 0 && e > s && e <= len) {
                                boolean isField = (el != null)
                                        ? el.getKind().isField()
                                        : declaredFields.contains(name);
                                boolean isStatic = (el != null)
                                        ? (el.getModifiers().contains(javax.lang.model.element.Modifier.STATIC)
                                            && el.getKind() != ElementKind.CLASS
                                            && el.getKind() != ElementKind.INTERFACE
                                            && el.getKind() != ElementKind.ENUM
                                            && el.getKind() != ElementKind.PACKAGE)
                                        : (declaredStaticFields.contains(name) || declaredStaticMethods.contains(name));
                                for (int k = (int) s; k < (int) e; k++) {
                                    if (isField) ar.fg[k] = COL_FIELD;
                                    if (isStatic) ar.italic[k] = true;
                                }
                            }
                            return super.visitIdentifier(node, p);
                        }

                        @Override
                        public Void visitMemberSelect(MemberSelectTree node, Void p) {
                            Element el = trees.getElement(getCurrentPath());
                            String memberName = node.getIdentifier().toString();
                            long s = pos.getStartPosition(cu, node);
                            long e = pos.getEndPosition(cu, node);
                            if (s >= 0 && e > s && e <= len) {
                                int dotIdx = code.lastIndexOf('.', (int) e - 1);
                                if (dotIdx >= s) {
                                    int idStart = dotIdx + 1;
                                    boolean isField = (el != null && el.getKind().isField())
                                            || (node.getExpression().toString().equals("this") && declaredFields.contains(memberName));
                                    boolean isStatic = (el != null && el.getModifiers().contains(Modifier.STATIC) && el.getKind() != ElementKind.CLASS && el.getKind() != ElementKind.PACKAGE);
                                    if (el == null) {
                                        String exprStr = node.getExpression().toString();
                                        if (!exprStr.isEmpty() && Character.isUpperCase(exprStr.charAt(0)) && getCurrentPath().getParentPath().getLeaf() instanceof MethodInvocationTree) {
                                            isStatic = true;
                                        }
                                    }
                                    for (int k = idStart; k < (int) e; k++) {
                                        if (isField) ar.fg[k] = COL_FIELD;
                                        if (isStatic) ar.italic[k] = true;
                                    }
                                }
                            }
                            return super.visitMemberSelect(node, p);
                        }
                    }.scan(cu, null);
                }

                // Register fold for multi-line import block if >= 2 lines
                String[] rawLines = code.split("\n", -1);
                int firstImport = -1, lastImport = -1;
                for (int ln = 0; ln < rawLines.length; ln++) {
                    String tr = rawLines[ln].trim();
                    if (tr.startsWith("import ")) {
                        if (firstImport == -1) firstImport = ln;
                        lastImport = ln;
                    }
                }
                if (firstImport != -1 && lastImport > firstImport) {
                    ar.foldStartLines.add(firstImport);
                    ar.foldPairs.put(firstImport, lastImport);
                }

                // Record real javac warnings (e.g. unchecked/deprecation)
                for (Diagnostic<? extends JavaFileObject> d : diags.getDiagnostics()) {
                    if (d.getKind() == Diagnostic.Kind.WARNING || d.getKind() == Diagnostic.Kind.MANDATORY_WARNING) {
                        if (d.getLineNumber() > 0) {
                            ar.warningLines.add((int) d.getLineNumber() - 1);
                        }
                    }
                }
            }
        } catch (Exception ignored) {}

        // Fallback member extraction if AST did not find any members
        if (ar.members.isEmpty()) {
            String cls = ar.className.isEmpty() ? (filename.endsWith(".java") ? filename.substring(0, filename.length() - 5) : filename) : ar.className;
            MemberItem ci = new MemberItem();
            ci.kind = MemberItem.Kind.CLASS;
            ci.name = cls;
            ar.members.add(ci);

            java.util.regex.Pattern methPat = java.util.regex.Pattern.compile(
                "(?:public|protected|private)?\\s*(?:static\\s+)?(?:([\\w<>\\[\\]]+)\\s+)?(\\w+)\\s*\\(([^)]*)\\)"
            );
            for (String line : code.split("\n", -1)) {
                String tr = line.trim();
                if (tr.startsWith("//") || tr.startsWith("/*") || tr.startsWith("*")) continue;
                java.util.regex.Matcher m = methPat.matcher(tr);
                if (m.find()) {
                    String ret = m.group(1);
                    String name = m.group(2);
                    String params = m.group(3);
                    if (JAVA_KEYWORDS.contains(name) || "if".equals(name) || "for".equals(name) || "while".equals(name) || "switch".equals(name) || "catch".equals(name)) {
                        continue;
                    }
                    MemberItem item = new MemberItem();
                    if (ret == null || name.equals(cls)) {
                        item.kind = MemberItem.Kind.CONSTRUCTOR;
                        item.name = cls;
                    } else {
                        item.kind = MemberItem.Kind.METHOD;
                        item.name = name;
                        item.returnType = ret;
                    }
                    item.params = params != null ? params.trim() : "";
                    ar.members.add(item);
                }
            }
        }

        return ar;
    }

    private static void highlightJavadocSubtokens(String code, int start, int end, AnalysisResult ar) {
        int i = start;
        while (i < end) {
            char ch = code.charAt(i);
            if (ch == '@' && i + 1 < end && Character.isLetter(code.charAt(i + 1))) {
                int j = i + 1;
                while (j < end && Character.isJavaIdentifierPart(code.charAt(j))) j++;
                for (int k = i; k < j; k++) ar.bold[k] = true;
                i = j;
            } else if (ch == '<') {
                int j = code.indexOf('>', i + 1);
                if (j != -1 && j < end) {
                    for (int k = i; k <= j; k++) {
                        ar.fg[k] = COL_HTML_TAG;
                        ar.bold[k] = true;
                    }
                    i = j + 1;
                } else {
                    i++;
                }
            } else {
                i++;
            }
        }
    }

    private static BufferedImage loadJarBitmap(String jarPath, String entryPath) {
        File jf = new File(jarPath);
        if (!jf.exists()) return null;
        try (JarFile jar = new JarFile(jf)) {
            ZipEntry entry = jar.getEntry(entryPath);
            if (entry != null) {
                try (InputStream is = jar.getInputStream(entry)) {
                    return ImageIO.read(is);
                }
            }
        } catch (Exception ignored) {}
        return null;
    }

    private static Icon loadJarIcon(String jarPath, String svgEntry, String fallbackPngEntry, int size) {
        File jf = new File(jarPath);
        if (!jf.exists()) return null;
        if (svgEntry != null) {
            try (JarFile jar = new JarFile(jf)) {
                ZipEntry entry = jar.getEntry(svgEntry);
                if (entry != null) {
                    try (InputStream is = jar.getInputStream(entry)) {
                        Class<?> loaderCls = Class.forName("com.github.weisj.jsvg.parser.SVGLoader");
                        Object loader = loaderCls.getDeclaredConstructor().newInstance();
                        Method loadMethod = loaderCls.getMethod("load", InputStream.class);
                        Object svgDoc = loadMethod.invoke(loader, is);
                        if (svgDoc != null) {
                            BufferedImage bi = new BufferedImage(size * 2, size * 2, BufferedImage.TYPE_INT_ARGB);
                            Graphics2D g2 = bi.createGraphics();
                            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                            g2.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BICUBIC);
                            Class<?> docCls = svgDoc.getClass();
                            Method sizeMethod = docCls.getMethod("size");
                            Object floatDim = sizeMethod.invoke(svgDoc);
                            double dw = ((Number) floatDim.getClass().getMethod("getWidth").invoke(floatDim)).doubleValue();
                            double dh = ((Number) floatDim.getClass().getMethod("getHeight").invoke(floatDim)).doubleValue();
                            double sc = Math.min((size * 2.0) / dw, (size * 2.0) / dh);
                            g2.scale(sc, sc);
                            Method renderMethod = docCls.getMethod("render", Component.class, Graphics2D.class);
                            renderMethod.invoke(svgDoc, null, g2);
                            g2.dispose();
                            Image scaled = bi.getScaledInstance(size, size, Image.SCALE_SMOOTH);
                            return new ImageIcon(scaled);
                        }
                    }
                }
            } catch (Throwable ignored) {}
        }
        if (fallbackPngEntry != null) {
            BufferedImage bi = loadJarBitmap(jarPath, fallbackPngEntry);
            if (bi != null) {
                if (bi.getWidth() != size || bi.getHeight() != size) {
                    return new ImageIcon(bi.getScaledInstance(size, size, Image.SCALE_SMOOTH));
                }
                return new ImageIcon(bi);
            }
        }
        return null;
    }

    private static Icon createCircleIcon(Color color, int size) {
        return new Icon() {
            public int getIconWidth() { return size; }
            public int getIconHeight() { return size; }
            public void paintIcon(Component c, Graphics g, int x, int y) {
                Graphics2D g2 = (Graphics2D) g.create();
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                g2.setColor(color);
                g2.fillOval(x + 2, y + 2, size - 4, size - 4);
                g2.setColor(color.darker());
                g2.drawOval(x + 2, y + 2, size - 4, size - 4);
                g2.dispose();
            }
        };
    }

    private static Icon createDiamondIcon(Color color, int size) {
        return new Icon() {
            public int getIconWidth() { return size; }
            public int getIconHeight() { return size; }
            public void paintIcon(Component c, Graphics g, int x, int y) {
                Graphics2D g2 = (Graphics2D) g.create();
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                g2.setColor(color);
                Polygon p = new Polygon();
                p.addPoint(x + size / 2, y + 2);
                p.addPoint(x + size - 2, y + size / 2);
                p.addPoint(x + size / 2, y + size - 2);
                p.addPoint(x + 2, y + size / 2);
                g2.fillPolygon(p);
                g2.setColor(color.darker());
                g2.drawPolygon(p);
                g2.dispose();
            }
        };
    }

    static class ErrorStripePanel extends JPanel {
        ErrorStripePanel() {
            setPreferredSize(new Dimension(14, 100));
            setBackground(new Color(0xF2, 0xF2, 0xF2));
        }

        @Override
        protected void paintComponent(Graphics g0) {
            super.paintComponent(g0);
            Graphics2D g = (Graphics2D) g0;
            g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            int w = getWidth();
            int h = getHeight();

            g.setColor(new Color(0xF2, 0xF2, 0xF2));
            g.fillRect(0, 0, w, h);
            g.setColor(new Color(0xE2, 0xE2, 0xE2));
            g.drawLine(0, 0, 0, h);

            // Top green status checkmark badge
            int bx = (w - 10) / 2;
            int by = 3;
            g.setColor(new Color(0x66, 0xBB, 0x6A));
            g.fillRoundRect(bx, by, 10, 10, 2, 2);
            g.setColor(new Color(0x43, 0xA0, 0x47));
            g.drawRoundRect(bx, by, 9, 9, 2, 2);

            g.setColor(Color.WHITE);
            g.drawLine(bx + 2, by + 5, bx + 4, by + 7);
            g.drawLine(bx + 4, by + 7, bx + 8, by + 3);
        }
    }

    static class EditorCanvas extends JPanel {
        private final String[] allLines;
        private final int[] lineStartOffsets;
        private final AnalysisResult ar;
        private final int startIdx;
        private final int endIdx;
        private final int activeLineIdx;
        private final int caretCol;
        private final boolean withCursor;
        private final boolean withMarginGuide;
        private final BufferedImage overrideBadge;
        private final BufferedImage warningBadge;

        private final Font fontPlain = new Font("Consolas", Font.PLAIN, 13);
        private final Font fontBold = new Font("Consolas", Font.BOLD, 13);
        private final Font fontItalic = new Font("Consolas", Font.ITALIC, 13);
        private final Font fontBoldItalic = new Font("Consolas", Font.BOLD | Font.ITALIC, 13);
        private final Font fontLineNum = new Font("Consolas", Font.PLAIN, 12);

        private final int lineHeight = 19;
        private final int gutterWidth;
        private final int codeLeftPad = 8;
        private final int topPad = 4;
        private final int maxCodeWidthPx;

        EditorCanvas(
            String code, AnalysisResult ar, int startLine, int endLine,
            int caretLine, int caretCol, boolean withCursor, boolean withMarginGuide,
            int jitterW, int jitterH, String nbHome, boolean isFullWindow
        ) {
            this.allLines = code.split("\n", -1);
            this.lineStartOffsets = new int[allLines.length];
            int off = 0;
            for (int i = 0; i < allLines.length; i++) {
                lineStartOffsets[i] = off;
                off += allLines[i].length() + 1;
            }
            this.ar = ar;
            this.startIdx = Math.max(0, startLine - 1);
            this.endIdx = (endLine <= 0 || endLine > allLines.length) ? allLines.length - 1 : endLine - 1;

            int targetLineIdx = caretLine - 1;
            this.activeLineIdx = Math.max(this.startIdx, Math.min(this.endIdx, targetLineIdx));
            this.caretCol = Math.max(1, caretCol);
            this.withCursor = withCursor;
            this.withMarginGuide = withMarginGuide;

            String javaEdJar = nbHome + "\\java\\modules\\org-netbeans-modules-java-editor.jar";
            this.overrideBadge = loadJarBitmap(javaEdJar, "org/netbeans/modules/java/editor/resources/override_badge.png");
            this.warningBadge = loadJarBitmap(javaEdJar, "org/netbeans/modules/java/editor/resources/warning_badge.gif");

            Canvas tmp = new Canvas();
            FontMetrics fmCode = tmp.getFontMetrics(fontPlain);
            FontMetrics fmLn = tmp.getFontMetrics(fontLineNum);
            int maxLnW = fmLn.stringWidth(String.valueOf(Math.max(10, this.endIdx + 1)));
            this.gutterWidth = Math.max(54, maxLnW + 34);

            int maxW = 280;
            for (int i = this.startIdx; i <= this.endIdx; i++) {
                String expanded = allLines[i].replace("\t", "    ");
                maxW = Math.max(maxW, fmCode.stringWidth(expanded));
            }
            this.maxCodeWidthPx = maxW;

            int visCount = Math.max(1, this.endIdx - this.startIdx + 1);
            int prefW = isFullWindow ? Math.max(680, gutterWidth + codeLeftPad + maxW + 40) : (gutterWidth + codeLeftPad + maxW + 40 + jitterW);
            int prefH = topPad + visCount * lineHeight + (isFullWindow ? 8 : jitterH);
            setPreferredSize(new Dimension(prefW, prefH));
            setBackground(COL_BG);
            setOpaque(true);
        }

        @Override
        protected void paintComponent(Graphics g0) {
            super.paintComponent(g0);
            Graphics2D g = (Graphics2D) g0;
            g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_LCD_HRGB);
            g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            g.setRenderingHint(RenderingHints.KEY_FRACTIONALMETRICS, RenderingHints.VALUE_FRACTIONALMETRICS_ON);

            int w = getWidth();
            int h = getHeight();

            g.setColor(COL_BG);
            g.fillRect(0, 0, w, h);

            // Active Caret Row highlight
            int activeVisRow = activeLineIdx - startIdx;
            if (activeVisRow >= 0 && activeVisRow <= (endIdx - startIdx)) {
                g.setColor(COL_CARET_ROW);
                g.fillRect(gutterWidth, topPad + activeVisRow * lineHeight, w - gutterWidth, lineHeight);
            }

            // Text Limit Guide Line at column 80
            FontMetrics fmCode = g.getFontMetrics(fontPlain);
            int spaceW = fmCode.charWidth(' ');
            if (withMarginGuide) {
                int limitX = gutterWidth + codeLeftPad + 80 * spaceW;
                if (limitX < w - 10) {
                    g.setColor(COL_TEXT_LIMIT);
                    g.drawLine(limitX, 0, limitX, h);
                }
            }

            // Gutter background & border
            g.setColor(COL_GUTTER_BG);
            g.fillRect(0, 0, gutterWidth, h);
            g.setColor(COL_GUTTER_BORDER);
            g.drawLine(gutterWidth - 1, 0, gutterWidth - 1, h);

            // Fold connector bars intersecting visible window
            int foldX = gutterWidth - 11;
            g.setColor(COL_FOLD_BAR);
            for (Map.Entry<Integer, Integer> fp : ar.foldPairs.entrySet()) {
                int sL = fp.getKey();
                int eL = fp.getValue();
                if (eL < startIdx || sL > endIdx) continue;
                int visStart = Math.max(sL, startIdx) - startIdx;
                int visEnd = Math.min(eL, endIdx) - startIdx;
                int y1 = (sL >= startIdx) ? (topPad + visStart * lineHeight + lineHeight / 2) : 0;
                int y2 = (eL <= endIdx) ? (topPad + visEnd * lineHeight + lineHeight / 2) : h;
                g.drawLine(foldX, y1, foldX, y2);
                if (eL <= endIdx) {
                    g.drawLine(foldX, y2, foldX + 4, y2);
                }
            }

            FontMetrics fmLn = g.getFontMetrics(fontLineNum);

            for (int lineIdx = startIdx; lineIdx <= endIdx; lineIdx++) {
                int visRow = lineIdx - startIdx;
                String line = allLines[lineIdx];
                int yTop = topPad + visRow * lineHeight;
                int yBaseline = yTop + fmCode.getAscent() + 2;

                // Line number
                g.setFont(fontLineNum);
                g.setColor(COL_LINE_NUM);
                String lnStr = String.valueOf(lineIdx + 1);
                int lnW = fmLn.stringWidth(lnStr);
                g.drawString(lnStr, gutterWidth - 32 - lnW, yBaseline);

                // Gutter Badge (Override or Warning)
                if (ar.overrideLines.contains(lineIdx) && overrideBadge != null) {
                    g.drawImage(overrideBadge, gutterWidth - 30, yTop + (lineHeight - 13) / 2, 12, 12, null);
                } else if (ar.warningLines.contains(lineIdx) && warningBadge != null) {
                    g.drawImage(warningBadge, gutterWidth - 30, yTop + (lineHeight - 13) / 2, 12, 12, null);
                }

                // Fold Box [-]
                if (ar.foldStartLines.contains(lineIdx)) {
                    int bx = foldX - 4;
                    int by = yTop + (lineHeight - 9) / 2;
                    g.setColor(Color.WHITE);
                    g.fillRect(bx, by, 8, 8);
                    g.setColor(COL_FOLD_BAR);
                    g.drawRect(bx, by, 8, 8);
                    g.drawLine(bx + 2, by + 4, bx + 6, by + 4);
                }

                // Indentation guide lines
                int leadingSpaces = 0;
                while (leadingSpaces < line.length() && (line.charAt(leadingSpaces) == ' ' || line.charAt(leadingSpaces) == '\t')) {
                    leadingSpaces += (line.charAt(leadingSpaces) == '\t') ? 4 : 1;
                }
                g.setColor(COL_INDENT_GUIDE);
                for (int sp = 4; sp < leadingSpaces; sp += 4) {
                    int gx = gutterWidth + codeLeftPad + sp * spaceW;
                    g.drawLine(gx, yTop, gx, yTop + lineHeight);
                }

                // Render styled runs
                int x = gutterWidth + codeLeftPad;
                int lineOff = lineStartOffsets[lineIdx];
                int i = 0;
                while (i < line.length()) {
                    if (line.charAt(i) == '\t') {
                        x += 4 * spaceW;
                        i++;
                        continue;
                    }
                    int absIdx = lineOff + i;
                    Color fg = absIdx < ar.fg.length ? ar.fg[absIdx] : COL_FG;
                    boolean b = absIdx < ar.bold.length && ar.bold[absIdx];
                    boolean it = absIdx < ar.italic.length && ar.italic[absIdx];

                    int j = i + 1;
                    while (j < line.length() && line.charAt(j) != '\t') {
                        int nAbs = lineOff + j;
                        Color nFg = nAbs < ar.fg.length ? ar.fg[nAbs] : COL_FG;
                        boolean nB = nAbs < ar.bold.length && ar.bold[nAbs];
                        boolean nIt = nAbs < ar.italic.length && ar.italic[nAbs];
                        if (!nFg.equals(fg) || nB != b || nIt != it) break;
                        j++;
                    }
                    String run = line.substring(i, j);
                    Font f = (b && it) ? fontBoldItalic : b ? fontBold : it ? fontItalic : fontPlain;
                    g.setFont(f);
                    g.setColor(fg);
                    g.drawString(run, x, yBaseline);
                    x += g.getFontMetrics(f).stringWidth(run);
                    i = j;
                }

                // Precise Caret drawing at caretCol on active line
                if (lineIdx == activeLineIdx && withCursor) {
                    int cursorX = gutterWidth + codeLeftPad;
                    int colCounter = 1;
                    for (int ci = 0; ci < line.length() && colCounter < caretCol; ci++) {
                        char ch = line.charAt(ci);
                        if (ch == '\t') {
                            int tabSp = 4 - ((colCounter - 1) % 4);
                            cursorX += tabSp * spaceW;
                            colCounter += tabSp;
                        } else {
                            cursorX += spaceW;
                            colCounter++;
                        }
                    }
                    while (colCounter < caretCol) {
                        cursorX += spaceW;
                        colCounter++;
                    }
                    g.setColor(Color.BLACK);
                    g.fillRect(cursorX, yTop + 2, 1, lineHeight - 4);
                }
            }
        }
    }

    private static void renderEditorOnly(
        String code, AnalysisResult ar, int startLine, int endLine,
        int caretLine, int caretCol, boolean withCursor, boolean withMarginGuide,
        double scale, int jitterW, int jitterH, String nbHome, File outFile
    ) throws Exception {
        EditorCanvas canvas = new EditorCanvas(code, ar, startLine, endLine, caretLine, caretCol, withCursor, withMarginGuide, jitterW, jitterH, nbHome, false);
        Dimension dim = canvas.getPreferredSize();
        canvas.setSize(dim);

        double effScale = scale > 0 ? scale : 1.5;
        BufferedImage img = new BufferedImage((int) Math.round(dim.width * effScale), (int) Math.round(dim.height * effScale), BufferedImage.TYPE_INT_RGB);
        Graphics2D g = img.createGraphics();
        if (effScale != 1.0) g.scale(effScale, effScale);
        canvas.paint(g);
        g.dispose();

        if (outFile.getParentFile() != null) outFile.getParentFile().mkdirs();
        ImageIO.write(img, "PNG", outFile);
    }

    private static void setupFlatLafLight() {
        try {
            Class<?> flatLaf = Class.forName("com.formdev.flatlaf.FlatLightLaf");
            Method setup = flatLaf.getMethod("setup");
            setup.invoke(null);
            // Match NetBeans 31 FlatLaf.properties overrides
            UIManager.put("TitlePane.menuBarEmbedded", Boolean.TRUE);
            UIManager.put("TitlePane.unifiedBackground", Boolean.TRUE);
            UIManager.put("MenuBar.background", new Color(0xF2, 0xF2, 0xF2));
            UIManager.put("TabbedPane.tabHeight", 28);
            UIManager.put("TabbedPane.tabType", "card");
            UIManager.put("TabbedPane.cardTabArc", 0);
            UIManager.put("TabbedPane.underlineHeight", 0);
            UIManager.put("TabbedPane.showTabSeparators", Boolean.TRUE);
            UIManager.put("EditorTab.underlineAtTop", Boolean.TRUE);
            UIManager.put("SplitPaneDivider.style", "plain");
            UIManager.put("Tree.paintLines", Boolean.FALSE);
        } catch (Throwable ignored) {}
    }

    private static void renderFullWindow(
        String code, AnalysisResult ar, String filename, String projectName, List<String> extraFiles,
        int startLine, int endLine, int caretLine, int caretCol, boolean withCursor, boolean withMarginGuide,
        boolean showBottomDock, boolean showNavigator, double scale, int jitterW, int jitterH, String nbHome, File outFile
    ) throws Exception {
        setupFlatLafLight();

        String nbCoreJar = nbHome + "\\nb\\core\\locale\\core_nb.jar";
        String projUiJar = nbHome + "\\ide\\modules\\org-netbeans-modules-projectui.jar";
        String javaProjUiJar = nbHome + "\\java\\modules\\org-netbeans-modules-java-project-ui.jar";
        String javaSrcJar = nbHome + "\\java\\modules\\org-netbeans-modules-java-source.jar";
        String mavenJar = nbHome + "\\java\\modules\\org-netbeans-modules-maven.jar";
        String dbgUiJar = nbHome + "\\ide\\modules\\org-netbeans-spi-debugger-ui.jar";
        String profilerJar = nbHome + "\\profiler\\modules\\org-netbeans-modules-profiler.jar";
        String usersGuideJar = nbHome + "\\ide\\modules\\docs\\org-netbeans-modules-usersguide.jar";
        String openideActJar = nbHome + "\\platform\\modules\\org-openide-actions.jar";
        String openideLoadJar = nbHome + "\\platform\\modules\\org-openide-loaders.jar";
        String javaNavJar = nbHome + "\\java\\modules\\org-netbeans-modules-java-navigation.jar";
        String editorJar = nbHome + "\\ide\\modules\\org-netbeans-modules-editor.jar";
        String multiViewJar = nbHome + "\\platform\\modules\\org-netbeans-core-multiview.jar";

        BufferedImage nbLogo = loadJarBitmap(nbCoreJar, "org/netbeans/core/startup/frame32_nb.gif");
        if (nbLogo == null) nbLogo = loadJarBitmap(nbCoreJar, "org/netbeans/core/startup/frame_nb.gif");

        Icon icNewProj = loadJarIcon(projUiJar, "org/netbeans/modules/project/ui/resources/newProject24.svg", "org/netbeans/modules/project/ui/resources/newProject24.png", 18);
        Icon icNewFile = loadJarIcon(projUiJar, "org/netbeans/modules/project/ui/resources/newFile24.svg", "org/netbeans/modules/project/ui/resources/newFile24.png", 18);
        Icon icOpenProj = loadJarIcon(projUiJar, "org/netbeans/modules/project/ui/resources/openProject24.svg", "org/netbeans/modules/project/ui/resources/openProject24.png", 18);
        Icon icSaveAll = loadJarIcon(openideLoadJar, "org/openide/loaders/saveAll24.svg", "org/openide/loaders/saveAll24.gif", 18);
        Icon icUndo = loadJarIcon(openideActJar, "org/openide/resources/actions/undo24.svg", "org/openide/resources/actions/undo24.gif", 18);
        Icon icRedo = loadJarIcon(openideActJar, "org/openide/resources/actions/redo24.svg", "org/openide/resources/actions/redo24.gif", 18);

        Icon icRunMainProj = loadJarIcon(projUiJar, "org/netbeans/modules/project/ui/resources/runCurrentProject.svg", "org/netbeans/modules/project/ui/resources/runCurrentProject24.gif", 18);
        Icon icBuild = loadJarIcon(projUiJar, "org/netbeans/modules/project/ui/resources/buildProject24.svg", "org/netbeans/modules/project/ui/resources/buildProject24.png", 18);
        Icon icCleanBuild = loadJarIcon(projUiJar, "org/netbeans/modules/project/ui/resources/rebuildProject24.svg", "org/netbeans/modules/project/ui/resources/rebuildProject24.png", 18);
        Icon icRun = loadJarIcon(projUiJar, "org/netbeans/modules/project/ui/resources/runProject24.svg", "org/netbeans/modules/project/ui/resources/runProject24.png", 18);
        Icon icDebug = loadJarIcon(dbgUiJar, "org/netbeans/modules/debugger/resources/debugProject.svg", "org/netbeans/modules/debugger/resources/debugProject24.png", 18);
        Icon icProfile = loadJarIcon(profilerJar, "org/netbeans/modules/profiler/impl/icons/start.svg", "org/netbeans/modules/profiler/impl/icons/start.png", 18);
        Icon icTrash = loadJarIcon(usersGuideJar, null, "org/netbeans/modules/usersguide/img/trash-icon.png", 14);

        Icon icMavenProj = loadJarIcon(mavenJar, "org/netbeans/modules/maven/resources/Maven2Icon.svg", "org/netbeans/modules/maven/resources/Maven2Icon.gif", 16);
        Icon icPackage = loadJarIcon(javaProjUiJar, "org/netbeans/spi/java/project/support/ui/package.svg", "org/netbeans/spi/java/project/support/ui/package.gif", 16);
        Icon icJavaFile = loadJarIcon(javaSrcJar, "org/netbeans/modules/java/resources/class.svg", "org/netbeans/modules/java/resources/class.png", 16);
        Icon icInterface = loadJarIcon(javaSrcJar, "org/netbeans/modules/java/resources/interface.svg", "org/netbeans/modules/java/resources/interface.png", 16);
        Icon icLibs = loadJarIcon(javaProjUiJar, "org/netbeans/modules/java/project/ui/resources/libraries.svg", "org/netbeans/modules/java/project/ui/resources/libraries.gif", 16);

        // Navigator icons
        Icon rawNavClass = loadJarIcon(javaSrcJar, "org/netbeans/modules/java/resources/class.svg", "org/netbeans/modules/java/resources/class.png", 16);
        final Icon icNavClass = rawNavClass != null ? rawNavClass : createCircleIcon(new Color(0x2E, 0x7D, 0x32), 16);
        Icon rawNavConstructor = loadJarIcon(javaSrcJar, "org/netbeans/modules/java/source/resources/icons/constructorPublic.svg", "org/netbeans/modules/java/source/resources/icons/constructorPublic.png", 16);
        final Icon icNavConstructor = rawNavConstructor != null ? rawNavConstructor : createDiamondIcon(new Color(0xE8, 0xA8, 0x38), 16);
        Icon rawNavMethod = loadJarIcon(javaSrcJar, "org/netbeans/modules/java/source/resources/icons/methodPublic.svg", "org/netbeans/modules/java/source/resources/icons/methodPublic.png", 16);
        final Icon icNavMethod = rawNavMethod != null ? rawNavMethod : createCircleIcon(new Color(0xE8, 0x60, 0x30), 16);
        Icon rawNavField = loadJarIcon(javaSrcJar, "org/netbeans/modules/java/source/resources/icons/fieldPublic.svg", "org/netbeans/modules/java/source/resources/icons/fieldPublic.png", 16);
        final Icon icNavField = rawNavField != null ? rawNavField : createCircleIcon(new Color(0x38, 0x80, 0xE8), 16);

        // Navigator filter button icons
        Icon icFilterFields = loadJarIcon(javaNavJar, null, "org/netbeans/modules/java/navigation/resources/filterHideFields.png", 14);
        Icon icFilterStatic = loadJarIcon(javaNavJar, null, "org/netbeans/modules/java/navigation/resources/filterHideStatic.png", 14);
        Icon icFilterNonPub = loadJarIcon(javaNavJar, null, "org/netbeans/modules/java/navigation/resources/filterHideNonPublic.png", 14);
        Icon icSortAlpha = loadJarIcon(javaNavJar, null, "org/netbeans/modules/java/navigation/resources/sortAlpha.png", 14);
        Icon icSortPos = loadJarIcon(javaNavJar, null, "org/netbeans/modules/java/navigation/resources/sortPosition.png", 14);
        Icon icHierarchy = loadJarIcon(javaNavJar, null, "org/netbeans/modules/java/navigation/resources/hierarchy_window.png", 14);
        Icon icRefresh = loadJarIcon(javaNavJar, null, "org/netbeans/modules/java/navigation/resources/hierarchy_refresh.png", 14);

        // Editor micro-toolbar icons
        Icon icNavBack = loadJarIcon(editorJar, null, "org/netbeans/modules/editor/resources/navigate_back_16.png", 14);
        Icon icNavFwd = loadJarIcon(editorJar, null, "org/netbeans/modules/editor/resources/navigate_forward_16.png", 14);
        Icon icMacroRec = loadJarIcon(editorJar, null, "org/netbeans/modules/editor/resources/start_macro_recording.png", 14);
        Icon icMacroStop = loadJarIcon(editorJar, null, "org/netbeans/modules/editor/resources/stop_macro_recording.png", 14);
        Icon icIndent = loadJarIcon(editorJar, null, "org/netbeans/modules/editor/resources/indentEngine.gif", 14);
        Icon icSplitView = loadJarIcon(multiViewJar, null, "org/netbeans/core/multiview/resources/splitview.png", 14);

        JPanel root = new JPanel(new BorderLayout());
        root.setBackground(new Color(0xF2, 0xF2, 0xF2));

        JPanel northWrap = new JPanel();
        northWrap.setLayout(new BoxLayout(northWrap, BoxLayout.Y_AXIS));
        northWrap.setBackground(new Color(0xF2, 0xF2, 0xF2));

        // ==========================================
        // FEATURE 1: Unified 30px FlatTitlePane
        // ==========================================
        JPanel titlePane = new JPanel(new BorderLayout());
        titlePane.setBackground(new Color(0xF2, 0xF2, 0xF2));
        titlePane.setPreferredSize(new Dimension(1024, 30));
        titlePane.setMaximumSize(new Dimension(Integer.MAX_VALUE, 30));
        titlePane.setBorder(new MatteBorder(0, 0, 1, 0, new Color(0xE5, 0xE5, 0xE5)));

        // WEST: NetBeans Cube Logo + 13 Menus
        JPanel titleLeft = new JPanel(new FlowLayout(FlowLayout.LEFT, 0, 0));
        titleLeft.setOpaque(false);

        JLabel logoLbl = new JLabel();
        if (nbLogo != null) {
            logoLbl.setIcon(new ImageIcon(nbLogo.getScaledInstance(16, 16, Image.SCALE_SMOOTH)));
        }
        logoLbl.setBorder(new EmptyBorder(7, 8, 7, 6));
        titleLeft.add(logoLbl);

        JMenuBar menuBar = new JMenuBar();
        menuBar.setOpaque(false);
        menuBar.setBorder(null);
        String[] menus = {"File", "Edit", "View", "Navigate", "Source", "Refactor", "Run", "Debug", "Profile", "Team", "Tools", "Window", "Help"};
        for (String m : menus) {
            JMenu menu = new JMenu(m);
            menu.setFont(new Font("Segoe UI", Font.PLAIN, 12));
            menu.setOpaque(false);
            menu.setBorder(new EmptyBorder(3, 4, 3, 4));
            menuBar.add(menu);
        }
        titleLeft.add(menuBar);
        titlePane.add(titleLeft, BorderLayout.WEST);

        // CENTER: Centered Window Title
        String windowTitle = projectName + " - Apache NetBeans IDE 31";
        JLabel titleLabel = new JLabel(windowTitle, SwingConstants.CENTER);
        titleLabel.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        titleLabel.setForeground(new Color(0x33, 0x33, 0x33));
        titlePane.add(titleLabel, BorderLayout.CENTER);

        // EAST: Search Box + Windows 11 Captions
        JPanel titleRight = new JPanel(new FlowLayout(FlowLayout.RIGHT, 0, 0));
        titleRight.setOpaque(false);

        JTextField searchField = new JTextField();
        searchField.putClientProperty("JTextField.placeholderText", "Search (Ctrl+I)");
        searchField.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        searchField.setPreferredSize(new Dimension(145, 22));
        searchField.setMaximumSize(new Dimension(145, 22));
        searchField.setBorder(new CompoundBorder(
            new LineBorder(new Color(0xC8, 0xC8, 0xC8), 1, true),
            new EmptyBorder(1, 6, 1, 6)
        ));

        JPanel searchPad = new JPanel(new FlowLayout(FlowLayout.CENTER, 6, 4));
        searchPad.setOpaque(false);
        searchPad.add(searchField);
        titleRight.add(searchPad);

        JPanel winBtns = new JPanel() {
            @Override
            public Dimension getPreferredSize() { return new Dimension(138, 30); }
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                Graphics2D g2 = (Graphics2D) g;
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                g2.setColor(new Color(0x33, 0x33, 0x33));
                // Minimize
                g2.drawLine(18, 15, 28, 15);
                // Maximize
                g2.drawRect(64, 10, 9, 9);
                // Close
                g2.drawLine(110, 10, 119, 19);
                g2.drawLine(119, 10, 110, 19);
            }
        };
        winBtns.setOpaque(false);
        titleRight.add(winBtns);
        titlePane.add(titleRight, BorderLayout.EAST);

        northWrap.add(titlePane);

        // ==========================================
        // FEATURE 2: Main Toolbar Parity
        // ==========================================
        JToolBar tb = new JToolBar();
        tb.setFloatable(false);
        tb.setBackground(new Color(0xF2, 0xF2, 0xF2));
        tb.setPreferredSize(new Dimension(1024, 36));
        tb.setMaximumSize(new Dimension(Integer.MAX_VALUE, 36));
        tb.setBorder(new CompoundBorder(
            new MatteBorder(0, 0, 1, 0, new Color(0xD8, 0xD8, 0xD8)),
            new EmptyBorder(2, 6, 2, 8)
        ));

        // Group 1: New File, New Project, Open Project, Save All
        Icon[] grp1 = {icNewFile, icNewProj, icOpenProj, icSaveAll};
        for (Icon ic : grp1) {
            JButton btn = new JButton(ic);
            btn.setFocusable(false);
            btn.setOpaque(false);
            btn.setBorder(new EmptyBorder(3, 4, 3, 4));
            tb.add(btn);
        }

        tb.addSeparator(new Dimension(8, 20));

        // Group 2: Undo, Redo
        Icon[] grp2 = {icUndo, icRedo};
        for (Icon ic : grp2) {
            JButton btn = new JButton(ic);
            btn.setFocusable(false);
            btn.setOpaque(false);
            btn.setBorder(new EmptyBorder(3, 4, 3, 4));
            tb.add(btn);
        }

        tb.addSeparator(new Dimension(8, 20));

        // Group 3: <default config> Dropdown
        JComboBox<String> configCombo = new JComboBox<>(new String[]{"<default config>"});
        configCombo.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        configCombo.setPreferredSize(new Dimension(125, 23));
        configCombo.setMaximumSize(new Dimension(135, 23));
        configCombo.setBackground(Color.WHITE);
        configCombo.setFocusable(false);
        tb.add(configCombo);

        tb.add(Box.createHorizontalStrut(6));

        // Group 4: Run Main, Build, CleanBuild, Run, Debug, Profile
        Icon[] grp4 = {icRunMainProj, icBuild, icCleanBuild, icRun, icDebug, icProfile};
        for (Icon ic : grp4) {
            JButton btn = new JButton(ic);
            btn.setFocusable(false);
            btn.setOpaque(false);
            btn.setBorder(new EmptyBorder(3, 4, 3, 4));
            tb.add(btn);
        }

        tb.add(Box.createHorizontalGlue());

        // Group 5: Heap Meter Component ("580,8/864,0MB") + Trash button
        JPanel heapPanel = new JPanel(new BorderLayout(4, 0)) {
            @Override
            public Dimension getPreferredSize() { return new Dimension(145, 22); }
            @Override
            public Dimension getMaximumSize() { return new Dimension(145, 22); }
        };
        heapPanel.setOpaque(false);

        JComponent heapGauge = new JComponent() {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                Graphics2D g2 = (Graphics2D) g.create();
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                int w = getWidth();
                int h = getHeight();

                // Background
                g2.setColor(new Color(0xCE, 0xE3, 0xE6));
                g2.fillRoundRect(0, 1, w - 1, h - 3, 4, 4);

                // Progress fill: 580.8 / 864.0 = ~67.2%
                int fillW = (int) Math.round((w - 2) * (580.8 / 864.0));
                g2.setColor(new Color(0x3B, 0x82, 0xF6));
                g2.setClip(new RoundRectangle2D.Float(0, 1, w - 1, h - 3, 4, 4));
                g2.fillRect(1, 2, fillW, h - 4);
                g2.setClip(null);

                // Outline
                g2.setColor(new Color(0x9E, 0xB4, 0xCE));
                g2.drawRoundRect(0, 1, w - 1, h - 3, 4, 4);

                // Text
                String text = "580,8/864,0MB";
                g2.setFont(new Font("Segoe UI", Font.PLAIN, 10));
                FontMetrics fm = g2.getFontMetrics();
                int tx = (w - fm.stringWidth(text)) / 2;
                int ty = (h - fm.getHeight()) / 2 + fm.getAscent();
                g2.setColor(new Color(0x22, 0x22, 0x22));
                g2.drawString(text, tx, ty);
                g2.dispose();
            }
        };
        heapPanel.add(heapGauge, BorderLayout.CENTER);

        JButton gcBtn = new JButton();
        if (icTrash != null) {
            gcBtn.setIcon(icTrash);
        } else {
            gcBtn.setIcon(new Icon() {
                public int getIconWidth() { return 12; }
                public int getIconHeight() { return 12; }
                public void paintIcon(Component c, Graphics g, int x, int y) {
                    Graphics2D g2 = (Graphics2D) g;
                    g2.setColor(new Color(0x66, 0x66, 0x66));
                    g2.drawRect(x + 2, y + 3, 7, 7);
                    g2.drawLine(x + 1, y + 2, x + 9, y + 2);
                    g2.drawLine(x + 4, y + 1, x + 6, y + 1);
                }
            });
        }
        gcBtn.setToolTipText("Click to force garbage collection");
        gcBtn.setFocusable(false);
        gcBtn.setOpaque(false);
        gcBtn.setBorder(new EmptyBorder(1, 2, 1, 2));
        heapPanel.add(gcBtn, BorderLayout.EAST);

        tb.add(heapPanel);
        northWrap.add(tb);

        root.add(northWrap, BorderLayout.NORTH);

        // ==============================================================
        // FEATURE 3: Left Explorer Vertical Split & Package Tree & Navigator
        // ==============================================================
        DefaultMutableTreeNode treeRoot = new DefaultMutableTreeNode("Projects");
        DefaultMutableTreeNode projNode = new DefaultMutableTreeNode(projectName);
        DefaultMutableTreeNode srcPkgNode = new DefaultMutableTreeNode("Source Packages");

        // Subpackage categorization for nested package hierarchy
        Map<String, List<String>> pkgMap = new LinkedHashMap<>();
        for (String ef : extraFiles) {
            String pkgName;
            String baseName = new File(ef).getName();
            if (ef.contains("/") || ef.contains("\\")) {
                String normalized = ef.replace("\\", "/");
                int lastSlash = normalized.lastIndexOf('/');
                pkgName = normalized.substring(0, lastSlash).replace("/", ".");
            } else {
                if (baseName.contains("Controller")) {
                    pkgName = "controller";
                } else if (baseName.equals("Main.java")) {
                    pkgName = "main";
                } else if (baseName.contains("View")) {
                    pkgName = "view";
                } else if (!ar.packageName.isEmpty()) {
                    pkgName = ar.packageName;
                } else {
                    pkgName = "model";
                }
            }
            pkgMap.computeIfAbsent(pkgName, k -> new ArrayList<>()).add(baseName);
        }

        DefaultMutableTreeNode selectedFileNode = null;
        for (Map.Entry<String, List<String>> entry : pkgMap.entrySet()) {
            DefaultMutableTreeNode pkgFolder = new DefaultMutableTreeNode(entry.getKey());
            for (String fileInPkg : entry.getValue()) {
                DefaultMutableTreeNode fNode = new DefaultMutableTreeNode(fileInPkg);
                pkgFolder.add(fNode);
                if (fileInPkg.equals(filename) || fileInPkg.equals(new File(filename).getName())) {
                    selectedFileNode = fNode;
                }
            }
            srcPkgNode.add(pkgFolder);
        }

        projNode.add(srcPkgNode);
        projNode.add(new DefaultMutableTreeNode("Dependencies"));
        projNode.add(new DefaultMutableTreeNode("Java Dependencies"));
        projNode.add(new DefaultMutableTreeNode("Project Files"));
        treeRoot.add(projNode);

        JTree projTree = new JTree(treeRoot);
        projTree.setRootVisible(false);
        projTree.setShowsRootHandles(true);
        projTree.setRowHeight(21);
        projTree.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        for (int r = 0; r < projTree.getRowCount(); r++) projTree.expandRow(r);
        if (selectedFileNode != null) {
            projTree.setSelectionPath(new javax.swing.tree.TreePath(selectedFileNode.getPath()));
        }
        projTree.setCellRenderer(new DefaultTreeCellRenderer() {
            @Override
            public Component getTreeCellRendererComponent(JTree tree, Object value, boolean sel, boolean expanded, boolean leaf, int row, boolean hasFocus) {
                super.getTreeCellRendererComponent(tree, value, sel, expanded, leaf, row, hasFocus);
                String text = String.valueOf(value);
                if (text.equals(projectName) && icMavenProj != null) setIcon(icMavenProj);
                else if (text.equals("Source Packages") || pkgMap.containsKey(text)) {
                    if (icPackage != null) setIcon(icPackage);
                } else if (text.endsWith(".java")) {
                    if (text.startsWith("I") || text.contains("Interface")) {
                        setIcon(icInterface != null ? icInterface : icJavaFile);
                    } else if (icJavaFile != null) {
                        setIcon(icJavaFile);
                    }
                } else if ((text.equals("Dependencies") || text.equals("Java Dependencies")) && icLibs != null) {
                    setIcon(icLibs);
                } else if (text.equals("Project Files")) {
                    Icon closed = UIManager.getIcon("Tree.closedIcon");
                    if (closed != null) setIcon(closed);
                }
                if (text.equals(projectName)) setFont(getFont().deriveFont(Font.BOLD));
                else setFont(getFont().deriveFont(Font.PLAIN));
                return this;
            }
        });

        JTabbedPane leftTopTabs = new JTabbedPane(JTabbedPane.TOP);
        leftTopTabs.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        JScrollPane treeScroll = new JScrollPane(projTree);
        treeScroll.setBorder(BorderFactory.createEmptyBorder());
        leftTopTabs.addTab("Projects   \u00D7", treeScroll);
        leftTopTabs.addTab("Files", new JPanel());
        leftTopTabs.addTab("Favorites", new JPanel());
        leftTopTabs.addTab("Services", new JPanel());

        // Navigator Pane
        JPanel navPanel = new JPanel(new BorderLayout());
        navPanel.setBackground(Color.WHITE);

        JTabbedPane navTabs = new JTabbedPane(JTabbedPane.TOP);
        navTabs.setFont(new Font("Segoe UI", Font.PLAIN, 12));

        JPanel navInner = new JPanel(new BorderLayout());
        navInner.setBackground(Color.WHITE);

        // Control strip: Members dropdown + Filter text
        JPanel navCtrl = new JPanel(new BorderLayout(4, 0));
        navCtrl.setBackground(new Color(0xF2, 0xF2, 0xF2));
        navCtrl.setBorder(new EmptyBorder(3, 4, 3, 4));

        JComboBox<String> navCombo = new JComboBox<>(new String[]{"Members"});
        navCombo.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        navCombo.setPreferredSize(new Dimension(110, 22));
        navCombo.setBackground(Color.WHITE);
        navCombo.setFocusable(false);
        navCtrl.add(navCombo, BorderLayout.WEST);

        JTextField navFilter = new JTextField("<empty>");
        navFilter.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        navFilter.setForeground(new Color(0x88, 0x88, 0x88));
        navFilter.setPreferredSize(new Dimension(80, 22));
        navCtrl.add(navFilter, BorderLayout.CENTER);

        navInner.add(navCtrl, BorderLayout.NORTH);

        // Navigator Members Tree
        DefaultMutableTreeNode navRoot = new DefaultMutableTreeNode("NavRoot");
        String activeClsName = ar.className.isEmpty() ? (filename.endsWith(".java") ? filename.substring(0, filename.length() - 5) : filename) : ar.className;
        DefaultMutableTreeNode clsNode = new DefaultMutableTreeNode(activeClsName);
        navRoot.add(clsNode);

        for (MemberItem m : ar.members) {
            if (m.kind != MemberItem.Kind.CLASS) {
                clsNode.add(new DefaultMutableTreeNode(m));
            }
        }

        JTree navTree = new JTree(navRoot);
        navTree.setRootVisible(false);
        navTree.setShowsRootHandles(true);
        navTree.setRowHeight(20);
        navTree.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        for (int r = 0; r < navTree.getRowCount(); r++) navTree.expandRow(r);

        navTree.setCellRenderer(new DefaultTreeCellRenderer() {
            @Override
            public Component getTreeCellRendererComponent(JTree tree, Object value, boolean sel, boolean expanded, boolean leaf, int row, boolean hasFocus) {
                super.getTreeCellRendererComponent(tree, value, sel, expanded, leaf, row, hasFocus);
                if (value instanceof DefaultMutableTreeNode dmt) {
                    Object userObj = dmt.getUserObject();
                    if (userObj instanceof MemberItem m) {
                        setText(m.getDisplayLabel());
                        if (m.kind == MemberItem.Kind.CONSTRUCTOR) {
                            setIcon(icNavConstructor);
                        } else if (m.kind == MemberItem.Kind.METHOD) {
                            setIcon(icNavMethod);
                        } else if (m.kind == MemberItem.Kind.FIELD) {
                            setIcon(icNavField);
                        }
                    } else if (userObj.equals(activeClsName)) {
                        setText(activeClsName);
                        setIcon(icNavClass);
                    }
                }
                return this;
            }
        });

        JScrollPane navScroll = new JScrollPane(navTree);
        navScroll.setBorder(BorderFactory.createEmptyBorder());
        navInner.add(navScroll, BorderLayout.CENTER);

        // Navigator bottom micro toolbar (7 filter buttons)
        JPanel navBottomBar = new JPanel(new FlowLayout(FlowLayout.LEFT, 2, 2));
        navBottomBar.setBackground(new Color(0xF2, 0xF2, 0xF2));
        navBottomBar.setBorder(new MatteBorder(1, 0, 0, 0, new Color(0xE0, 0xE0, 0xE0)));
        Icon[] navIcons = {icFilterFields, icFilterStatic, icFilterNonPub, icSortAlpha, icSortPos, icHierarchy, icRefresh};
        for (Icon ni : navIcons) {
            JButton nbBtn = new JButton(ni);
            nbBtn.setFocusable(false);
            nbBtn.setOpaque(false);
            nbBtn.setPreferredSize(new Dimension(20, 20));
            nbBtn.setBorder(new EmptyBorder(1, 1, 1, 1));
            navBottomBar.add(nbBtn);
        }
        navInner.add(navBottomBar, BorderLayout.SOUTH);

        navTabs.addTab(filename + " - Navigator   \u00D7", navInner);
        navPanel.add(navTabs, BorderLayout.CENTER);

        JComponent leftComponent;
        if (showNavigator) {
            JSplitPane leftSplit = new JSplitPane(JSplitPane.VERTICAL_SPLIT, leftTopTabs, navPanel);
            leftSplit.setDividerLocation(245);
            leftSplit.setDividerSize(4);
            leftSplit.setBorder(BorderFactory.createEmptyBorder());
            leftComponent = leftSplit;
        } else {
            leftComponent = leftTopTabs;
        }
        leftComponent.setPreferredSize(new Dimension(285, 420));

        // ==============================================================
        // FEATURE 4 & 5: Editor Multi-Tab, Overline, Micro-Toolbar & Canvas
        // ==============================================================
        EditorCanvas edCanvas = new EditorCanvas(
            code, ar, startLine, endLine, caretLine, caretCol,
            withCursor, withMarginGuide, jitterW, jitterH, nbHome, true
        );
        Dimension edDim = edCanvas.getPreferredSize();
        int totalW = Math.max(1024, 290 + edDim.width + 16);
        int totalH = Math.max(575, 120 + edDim.height + (showBottomDock ? 140 : 0));

        JPanel editorWrapper = new JPanel(new BorderLayout());
        editorWrapper.setBackground(Color.WHITE);

        // Micro-toolbar strip directly below tabs
        JPanel edToolbar = new JPanel(new BorderLayout());
        edToolbar.setBackground(new Color(0xF6, 0xF6, 0xF6));
        edToolbar.setBorder(new MatteBorder(0, 0, 1, 0, new Color(0xDF, 0xDF, 0xDF)));
        edToolbar.setPreferredSize(new Dimension(100, 26));

        JPanel edToolLeft = new JPanel(new FlowLayout(FlowLayout.LEFT, 3, 2));
        edToolLeft.setOpaque(false);

        JToggleButton btnSource = new JToggleButton("Source", true);
        btnSource.setFont(new Font("Segoe UI", Font.BOLD, 11));
        btnSource.setBackground(Color.WHITE);
        btnSource.setBorder(new CompoundBorder(new LineBorder(new Color(0xC5, 0xC5, 0xC5)), new EmptyBorder(1, 6, 1, 6)));
        btnSource.setFocusable(false);

        JToggleButton btnHistory = new JToggleButton("History", false);
        btnHistory.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        btnHistory.setOpaque(false);
        btnHistory.setBorder(new EmptyBorder(1, 6, 1, 6));
        btnHistory.setFocusable(false);

        edToolLeft.add(btnSource);
        edToolLeft.add(btnHistory);

        // Action icons on micro toolbar
        Icon[] microIcons = {icNavBack, icNavFwd, icIndent, icMacroRec, icMacroStop};
        for (Icon mi : microIcons) {
            if (mi != null) {
                JButton mb = new JButton(mi);
                mb.setFocusable(false);
                mb.setOpaque(false);
                mb.setBorder(new EmptyBorder(2, 3, 2, 3));
                edToolLeft.add(mb);
            }
        }
        edToolbar.add(edToolLeft, BorderLayout.WEST);

        if (icSplitView != null) {
            JPanel edToolRight = new JPanel(new FlowLayout(FlowLayout.RIGHT, 4, 2));
            edToolRight.setOpaque(false);
            JButton svBtn = new JButton(icSplitView);
            svBtn.setFocusable(false);
            svBtn.setOpaque(false);
            svBtn.setBorder(new EmptyBorder(2, 3, 2, 3));
            edToolRight.add(svBtn);
            edToolbar.add(edToolRight, BorderLayout.EAST);
        }

        editorWrapper.add(edToolbar, BorderLayout.NORTH);

        // Center: Code Canvas + Right Error Stripe Scrollbar
        JPanel centerCodePanel = new JPanel(new BorderLayout());
        centerCodePanel.add(edCanvas, BorderLayout.CENTER);
        centerCodePanel.add(new ErrorStripePanel(), BorderLayout.EAST);
        editorWrapper.add(centerCodePanel, BorderLayout.CENTER);

        // Breadcrumb bar at bottom of editor
        JPanel breadcrumb = new JPanel(new BorderLayout());
        breadcrumb.setBackground(new Color(0xF8, 0xF8, 0xF8));
        breadcrumb.setBorder(new CompoundBorder(new MatteBorder(1, 0, 0, 0, new Color(0xE2, 0xE2, 0xE2)), new EmptyBorder(2, 8, 2, 8)));
        String bcTxt = (ar.packageName.isEmpty() ? "" : ar.packageName + "  >  ") + (ar.className.isEmpty() ? filename.replace(".java", "") : ar.className);
        JLabel bcLbl = new JLabel(bcTxt);
        bcLbl.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        bcLbl.setForeground(new Color(0x55, 0x55, 0x55));
        breadcrumb.add(bcLbl, BorderLayout.CENTER);
        editorWrapper.add(breadcrumb, BorderLayout.SOUTH);

        // Editor Multi-Tab Pane with Blue Top Overline
        JTabbedPane edTabs = new JTabbedPane(JTabbedPane.TOP) {
            @Override
            public void paint(Graphics g) {
                super.paint(g);
                int sel = getSelectedIndex();
                if (sel >= 0) {
                    Rectangle r = getBoundsAt(sel);
                    if (r != null) {
                        Graphics2D g2 = (Graphics2D) g.create();
                        g2.setColor(new Color(0x16, 0x83, 0xFB));
                        g2.fillRect(r.x, r.y, r.width, 3);
                        g2.dispose();
                    }
                }
            }
        };
        edTabs.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        edTabs.setTabLayoutPolicy(JTabbedPane.SCROLL_TAB_LAYOUT);

        for (String ef : extraFiles) {
            String tabName = new File(ef).getName();
            Icon tIcon = (tabName.startsWith("I") || tabName.contains("Interface")) ? icInterface : icJavaFile;
            if (ef.equals(filename) || tabName.equals(filename) || tabName.equals(new File(filename).getName())) {
                edTabs.addTab(tabName + "   \u00D7", tIcon, editorWrapper);
                edTabs.setSelectedComponent(editorWrapper);
            } else {
                JPanel dummy = new JPanel();
                dummy.setBackground(Color.WHITE);
                edTabs.addTab(tabName + "   \u00D7", tIcon, dummy);
            }
        }

        // Tab trailing navigation controls
        JPanel tabControls = new JPanel(new FlowLayout(FlowLayout.RIGHT, 2, 2)) {
            @Override
            public Dimension getPreferredSize() { return new Dimension(68, 26); }
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                Graphics2D g2 = (Graphics2D) g;
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                g2.setColor(new Color(0x70, 0x70, 0x70));
                // Scroll left <
                g2.drawLine(12, 13, 16, 9);
                g2.drawLine(12, 13, 16, 17);
                // Scroll right >
                g2.drawLine(28, 9, 32, 13);
                g2.drawLine(28, 17, 32, 13);
                // Dropdown v
                g2.drawLine(42, 11, 46, 15);
                g2.drawLine(46, 15, 50, 11);
                // Maximize []
                g2.drawRect(56, 9, 8, 8);
            }
        };
        tabControls.setOpaque(false);
        edTabs.putClientProperty("JTabbedPane.trailingComponent", tabControls);

        // ==============================================================
        // FEATURE 6: Bottom Output Dock
        // ==============================================================
        JPanel outputDock = new JPanel(new BorderLayout());
        outputDock.setBackground(Color.WHITE);

        JTabbedPane outputTabs = new JTabbedPane(JTabbedPane.TOP);
        outputTabs.setFont(new Font("Segoe UI", Font.PLAIN, 12));

        JPanel consoleWrap = new JPanel(new BorderLayout());
        consoleWrap.setBackground(Color.WHITE);
        consoleWrap.setBorder(new EmptyBorder(4, 6, 4, 6));

        JTextArea consoleText = new JTextArea();
        consoleText.setFont(new Font("Consolas", Font.PLAIN, 12));
        consoleText.setEditable(false);
        consoleText.setBackground(Color.WHITE);
        consoleText.setForeground(new Color(0x33, 0x33, 0x33));

        String mvnLog =
            "cd " + (projectName.contains(":") || projectName.contains("\\") ? projectName : "C:\\Users\\fritz\\Desktop\\" + projectName) + "; \"JAVA_HOME=C:\\\\Program Files\\\\Java\\\\jdk-21\" cmd /c \"\"\"C:\\\\Program Files\\\\Apache NetBeans\\\\java\\\\maven\\\\bin\\\\mvn.cmd\"\" -Dexec.vmArgs= \"\"-Dexec.args=-classpath %classpath " + (ar.packageName.isEmpty() ? "" : ar.packageName + ".") + (ar.className.isEmpty() ? "Main" : ar.className) + "\"\" -Dexec.appArgs= -Dexec.mainClass=" + (ar.packageName.isEmpty() ? "" : ar.packageName + ".") + (ar.className.isEmpty() ? "Main" : ar.className) + " -Dexec.executable=\"\"C:\\\\Program Files\\\\Java\\\\jdk-21\\\\bin\\\\java.exe\"\" process-classes org.codehaus.mojo:exec-maven-plugin:3.1.0:exec\"\n" +
            "Scanning for projects...\n\n" +
            "-----------------------< " + (ar.packageName.isEmpty() ? "com.mycompany" : ar.packageName) + ":" + projectName.toLowerCase().replace(" ", "-") + " >------------------------\n" +
            "Building " + projectName + " 1.0-SNAPSHOT\n" +
            "  from pom.xml\n" +
            "--------------------------------[ jar ]---------------------------------\n";

        consoleText.setText(mvnLog);
        consoleWrap.add(consoleText, BorderLayout.CENTER);
        outputTabs.addTab("Output   \u00D7", consoleWrap);

        JPanel dockControls = new JPanel(new FlowLayout(FlowLayout.RIGHT, 4, 2)) {
            @Override
            public Dimension getPreferredSize() { return new Dimension(48, 24); }
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                Graphics2D g2 = (Graphics2D) g;
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                g2.setColor(new Color(0x60, 0x60, 0x60));
                // Minimize (-)
                g2.drawLine(8, 14, 16, 14);
                // Maximize/Popout
                g2.drawRect(28, 7, 8, 8);
                g2.drawLine(28, 9, 36, 9);
            }
        };
        dockControls.setOpaque(false);
        outputTabs.putClientProperty("JTabbedPane.trailingComponent", dockControls);
        outputDock.add(outputTabs, BorderLayout.CENTER);
        outputDock.setPreferredSize(new Dimension(600, 140));

        JComponent rightComponent;
        if (showBottomDock) {
            int centerH = totalH - 86;
            JSplitPane rightSplit = new JSplitPane(JSplitPane.VERTICAL_SPLIT, edTabs, outputDock);
            rightSplit.setDividerLocation(Math.max(200, centerH - 145));
            rightSplit.setDividerSize(4);
            rightSplit.setBorder(BorderFactory.createEmptyBorder());
            rightComponent = rightSplit;
        } else {
            rightComponent = edTabs;
        }

        JSplitPane centerSplit = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, leftComponent, rightComponent);
        centerSplit.setDividerLocation(285);
        centerSplit.setDividerSize(4);
        centerSplit.setBorder(new EmptyBorder(2, 4, 2, 4));
        root.add(centerSplit, BorderLayout.CENTER);

        // ==============================================================
        // FEATURE 7: Segmented Status Bar
        // ==============================================================
        JPanel statusBar = new JPanel(new BorderLayout());
        statusBar.setBackground(new Color(0xF2, 0xF2, 0xF2));
        statusBar.setBorder(new CompoundBorder(
            new MatteBorder(1, 0, 0, 0, new Color(0xC6, 0xC6, 0xC6)),
            new EmptyBorder(1, 8, 1, 8)
        ));
        statusBar.setPreferredSize(new Dimension(100, 20));

        JLabel statusLeft = new JLabel("  Ready");
        statusLeft.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        statusLeft.setForeground(new Color(0x55, 0x55, 0x55));
        statusBar.add(statusLeft, BorderLayout.WEST);

        JPanel statusRight = new JPanel(new FlowLayout(FlowLayout.RIGHT, 0, 0));
        statusRight.setOpaque(false);

        Font fontStatus = new Font("Segoe UI", Font.PLAIN, 11);
        Color colStatusText = new Color(0x38, 0x38, 0x38);
        Border cellBorder = new CompoundBorder(
            new MatteBorder(0, 1, 0, 0, new Color(0xD0, 0xD0, 0xD0)),
            new EmptyBorder(0, 8, 0, 8)
        );

        JLabel cellPos = new JLabel(caretLine + ":" + caretCol);
        cellPos.setFont(fontStatus);
        cellPos.setForeground(colStatusText);
        cellPos.setBorder(cellBorder);
        statusRight.add(cellPos);

        JLabel cellIns = new JLabel("INS");
        cellIns.setFont(fontStatus);
        cellIns.setForeground(colStatusText);
        cellIns.setBorder(cellBorder);
        statusRight.add(cellIns);

        boolean isCrLf = code.contains("\r\n");
        JLabel cellEnding = new JLabel(isCrLf ? "Windows (CRLF)" : "Unix (LF)");
        cellEnding.setFont(fontStatus);
        cellEnding.setForeground(colStatusText);
        cellEnding.setBorder(cellBorder);
        statusRight.add(cellEnding);

        JLabel cellEncoding = new JLabel("UTF-8");
        cellEncoding.setFont(fontStatus);
        cellEncoding.setForeground(colStatusText);
        cellEncoding.setBorder(new CompoundBorder(
            new MatteBorder(0, 1, 0, 0, new Color(0xD0, 0xD0, 0xD0)),
            new EmptyBorder(0, 8, 0, 4)
        ));
        statusRight.add(cellEncoding);

        statusBar.add(statusRight, BorderLayout.EAST);
        root.add(statusBar, BorderLayout.SOUTH);

        // ==============================================================
        // FEATURE 8: Raster Scale
        // ==============================================================
        root.setSize(totalW, totalH);
        layoutRecursive(root);

        double effScale = scale > 0 ? scale : 1.0;
        BufferedImage img = new BufferedImage((int) Math.round(totalW * effScale), (int) Math.round(totalH * effScale), BufferedImage.TYPE_INT_RGB);
        Graphics2D g = img.createGraphics();
        if (effScale != 1.0) {
            g.scale(effScale, effScale);
        }
        root.paint(g);
        g.dispose();

        if (outFile.getParentFile() != null) outFile.getParentFile().mkdirs();
        ImageIO.write(img, "PNG", outFile);
    }

    private static void layoutRecursive(Container c) {
        c.doLayout();
        for (Component child : c.getComponents()) {
            if (child instanceof Container cc) {
                layoutRecursive(cc);
            }
        }
    }
}
