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
    private static final Color COL_TEXT_LIMIT = new Color(0xFF, 0xD4, 0xD4);

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
    }

    public static void main(String[] args) throws Exception {
        Map<String, String> opts = parseArgs(args);
        String filePath = opts.get("file");
        String outPath = opts.getOrDefault("out", "netbeans_shot.png");
        String filename = opts.getOrDefault("filename", filePath != null ? new File(filePath).getName() : "Main.java");
        int startLine = Integer.parseInt(opts.getOrDefault("start", "1"));
        int endLine = Integer.parseInt(opts.getOrDefault("end", "-1"));
        int activeOffset = Integer.parseInt(opts.getOrDefault("active-offset", "-1"));
        boolean withCursor = Boolean.parseBoolean(opts.getOrDefault("cursor", "true"));
        boolean withMarginGuide = Boolean.parseBoolean(opts.getOrDefault("margin-guide", "true"));
        String view = opts.getOrDefault("view", "editor");
        String projectName = opts.getOrDefault("project", "ProjekPraktikum");
        String sourcePath = opts.getOrDefault("sourcepath", "");
        String extraFilesRaw = opts.getOrDefault("extra-files", "");
        String nbHome = opts.getOrDefault("nb-home", DEFAULT_NB_HOME);
        int jitterW = Integer.parseInt(opts.getOrDefault("jitter-w", "32"));
        int jitterH = Integer.parseInt(opts.getOrDefault("jitter-h", "6"));

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
            renderFullWindow(code, ar, filename, projectName, extraFiles, startLine, endLine, activeOffset, withCursor, withMarginGuide, jitterW, jitterH, nbHome, new File(outPath));
        } else {
            renderEditorOnly(code, ar, startLine, endLine, activeOffset, withCursor, withMarginGuide, jitterW, jitterH, nbHome, new File(outPath));
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

                // Collect declared fields & static methods first as fallback for unresolved types
                for (CompilationUnitTree cu : asts) {
                    if (cu.getPackageName() != null) {
                        ar.packageName = cu.getPackageName().toString();
                    }
                    new TreeScanner<Void, Void>() {
                        @Override
                        public Void visitVariable(VariableTree node, Void p) {
                            // Handled inside TreePathScanner
                            return super.visitVariable(node, p);
                        }
                    }.scan(cu, null);
                }

                for (CompilationUnitTree cu : asts) {
                    LineMap lineMap = cu.getLineMap();
                    SourcePositions pos = trees.getSourcePositions();

                    // First pass: collect class-level fields and static methods
                    new TreePathScanner<Void, Void>() {
                        @Override
                        public Void visitClass(ClassTree node, Void p) {
                            if (ar.className.isEmpty()) ar.className = node.getSimpleName().toString();
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
                        private void styleDeclarationName(Tree node, String name, Color fg, boolean bold, boolean italic) {
                            if (name == null || name.isEmpty() || name.equals("<init>")) return;
                            long start = pos.getStartPosition(cu, node);
                            long end = pos.getEndPosition(cu, node);
                            if (start < 0 || end < 0 || start >= len) return;
                            String slice = code.substring((int) start, (int) Math.min(end, len));
                            int rel = slice.indexOf(name);
                            if (rel >= 0) {
                                int s = (int) start + rel;
                                int e = s + name.length();
                                for (int k = s; k < e; k++) {
                                    if (fg != null) ar.fg[k] = fg;
                                    if (bold) ar.bold[k] = true;
                                    if (italic) ar.italic[k] = true;
                                }
                            }
                        }

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
                            styleDeclarationName(node, node.getSimpleName().toString(), null, true, false);
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
                                    // Place override badge on the method signature line
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
                                if (parent instanceof ClassTree ct) {
                                    name = ct.getSimpleName().toString();
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
                                    // Heuristic fallback for unresolved static ClassName.method() calls
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
        // Try SVG via com.github.weisj.jsvg.parser.SVGLoader using reflection
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

    static class EditorCanvas extends JPanel {
        private final String[] allLines;
        private final int[] lineStartOffsets;
        private final AnalysisResult ar;
        private final int startIdx;
        private final int endIdx;
        private final int activeLineIdx;
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

        EditorCanvas(String code, AnalysisResult ar, int startLine, int endLine, int activeOffset, boolean withCursor, boolean withMarginGuide, int jitterW, int jitterH, String nbHome, boolean isFullWindow) {
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
            int visCount = Math.max(1, this.endIdx - this.startIdx + 1);
            this.activeLineIdx = (activeOffset >= 0 && activeOffset < visCount) ? (this.startIdx + activeOffset) : this.endIdx;
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

            int prefW = isFullWindow ? Math.max(700, gutterWidth + codeLeftPad + maxW + 60) : (gutterWidth + codeLeftPad + maxW + 40 + jitterW);
            int prefH = topPad + visCount * lineHeight + (isFullWindow ? 12 : jitterH);
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
            if (activeVisRow >= 0) {
                g.setColor(COL_CARET_ROW);
                g.fillRect(gutterWidth, topPad + activeVisRow * lineHeight, w - gutterWidth, lineHeight);
            }

            // Text Limit Guide Line at column 80
            FontMetrics fmCode = g.getFontMetrics(fontPlain);
            int charW = fmCode.charWidth('M');
            if (withMarginGuide) {
                int limitX = gutterWidth + codeLeftPad + 80 * charW;
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
            int spaceW = fmCode.charWidth(' ');

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

                if (lineIdx == activeLineIdx && withCursor) {
                    g.setColor(Color.BLACK);
                    g.fillRect(x + 1, yTop + 2, 2, lineHeight - 4);
                }
            }
        }
    }

    private static void renderEditorOnly(String code, AnalysisResult ar, int startLine, int endLine, int activeOffset, boolean withCursor, boolean withMarginGuide, int jitterW, int jitterH, String nbHome, File outFile) throws Exception {
        EditorCanvas canvas = new EditorCanvas(code, ar, startLine, endLine, activeOffset, withCursor, withMarginGuide, jitterW, jitterH, nbHome, false);
        Dimension dim = canvas.getPreferredSize();
        canvas.setSize(dim);

        double scale = 1.5;
        BufferedImage img = new BufferedImage((int) Math.round(dim.width * scale), (int) Math.round(dim.height * scale), BufferedImage.TYPE_INT_RGB);
        Graphics2D g = img.createGraphics();
        g.scale(scale, scale);
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
            UIManager.put("TabbedPane.tabHeight", 28);
            UIManager.put("TabbedPane.tabType", "card");
            UIManager.put("TabbedPane.cardTabArc", 0);
            UIManager.put("TabbedPane.underlineColor", new Color(0x46, 0x7A, 0xD0));
            UIManager.put("TabbedPane.showTabSeparators", Boolean.TRUE);
            UIManager.put("SplitPaneDivider.style", "plain");
            UIManager.put("Tree.paintLines", Boolean.FALSE);
        } catch (Throwable ignored) {}
    }

    private static void renderFullWindow(
            String code, AnalysisResult ar, String filename, String projectName, List<String> extraFiles,
            int startLine, int endLine, int activeOffset, boolean withCursor, boolean withMarginGuide,
            int jitterW, int jitterH, String nbHome, File outFile
    ) throws Exception {
        setupFlatLafLight();

        String nbCoreJar = nbHome + "\\nb\\core\\locale\\core_nb.jar";
        String projUiJar = nbHome + "\\ide\\modules\\org-netbeans-modules-projectui.jar";
        String javaProjUiJar = nbHome + "\\java\\modules\\org-netbeans-modules-java-project-ui.jar";
        String javaSrcJar = nbHome + "\\java\\modules\\org-netbeans-modules-java-source.jar";
        String mavenJar = nbHome + "\\java\\modules\\org-netbeans-modules-maven.jar";
        String dbgUiJar = nbHome + "\\ide\\modules\\org-netbeans-spi-debugger-ui.jar";
        String openideActJar = nbHome + "\\platform\\modules\\org-openide-actions.jar";
        String openideLoadJar = nbHome + "\\platform\\modules\\org-openide-loaders.jar";

        BufferedImage nbLogo = loadJarBitmap(nbCoreJar, "org/netbeans/core/startup/frame32_nb.gif");
        if (nbLogo == null) nbLogo = loadJarBitmap(nbCoreJar, "org/netbeans/core/startup/frame_nb.gif");
        Icon icNewFile = loadJarIcon(projUiJar, "org/netbeans/modules/project/ui/resources/newFile24.svg", "org/netbeans/modules/project/ui/resources/newFile24.png", 20);
        Icon icNewProj = loadJarIcon(projUiJar, "org/netbeans/modules/project/ui/resources/newProject24.svg", "org/netbeans/modules/project/ui/resources/newProject24.png", 20);
        Icon icOpenProj = loadJarIcon(projUiJar, "org/netbeans/modules/project/ui/resources/openProject24.svg", "org/netbeans/modules/project/ui/resources/openProject24.png", 20);
        Icon icSaveAll = loadJarIcon(openideLoadJar, null, "org/openide/loaders/saveAll24.gif", 20);
        Icon icUndo = loadJarIcon(openideActJar, null, "org/openide/resources/actions/undo24.gif", 20);
        Icon icRedo = loadJarIcon(openideActJar, null, "org/openide/resources/actions/redo24.gif", 20);
        Icon icBuild = loadJarIcon(projUiJar, "org/netbeans/modules/project/ui/resources/buildProject24.svg", "org/netbeans/modules/project/ui/resources/buildProject24.png", 20);
        Icon icCleanBuild = loadJarIcon(projUiJar, "org/netbeans/modules/project/ui/resources/rebuildProject24.svg", "org/netbeans/modules/project/ui/resources/rebuildProject24.png", 20);
        Icon icRun = loadJarIcon(projUiJar, null, "org/netbeans/modules/project/ui/resources/runProject24.png", 20);
        Icon icDebug = loadJarIcon(dbgUiJar, null, "org/netbeans/modules/debugger/resources/debugProject24.png", 20);

        Icon icProjTab = loadJarIcon(projUiJar, "org/netbeans/modules/project/ui/resources/projectTab.svg", "org/netbeans/modules/project/ui/resources/projectTab.png", 14);
        Icon icFilesTab = loadJarIcon(projUiJar, "org/netbeans/modules/project/ui/resources/filesTab.svg", "org/netbeans/modules/project/ui/resources/filesTab.png", 14);

        Icon icMavenProj = loadJarIcon(mavenJar, "org/netbeans/modules/maven/resources/Maven2Icon.svg", "org/netbeans/modules/maven/resources/Maven2Icon.gif", 16);
        Icon icPackage = loadJarIcon(javaProjUiJar, "org/netbeans/spi/java/project/support/ui/package.svg", "org/netbeans/spi/java/project/support/ui/package.gif", 16);
        Icon icJavaFile = loadJarIcon(javaSrcJar, "org/netbeans/modules/java/resources/class.svg", "org/netbeans/modules/java/resources/class.png", 16);
        Icon icLibs = loadJarIcon(javaProjUiJar, "org/netbeans/modules/java/project/ui/resources/libraries.svg", "org/netbeans/modules/java/project/ui/resources/libraries.gif", 16);

        JPanel root = new JPanel(new BorderLayout());
        root.setBackground(new Color(0xF2, 0xF2, 0xF2));

        // Top section: Windows 11 Title bar + Menu bar + Main Toolbar
        JPanel northWrap = new JPanel();
        northWrap.setLayout(new BoxLayout(northWrap, BoxLayout.Y_AXIS));

        // 1. Title bar
        JPanel titleBar = new JPanel(new BorderLayout()) {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                Graphics2D g2 = (Graphics2D) g;
                g2.setColor(new Color(0xE0, 0xE0, 0xE0));
                g2.drawLine(0, getHeight() - 1, getWidth(), getHeight() - 1);
            }
        };
        titleBar.setBackground(Color.WHITE);
        titleBar.setPreferredSize(new Dimension(100, 30));
        JPanel titleLeft = new JPanel(new BorderLayout(8, 0));
        titleLeft.setOpaque(false);
        titleLeft.setBorder(new EmptyBorder(4, 10, 4, 8));
        if (nbLogo != null) {
            titleLeft.add(new JLabel(new ImageIcon(nbLogo.getScaledInstance(16, 16, Image.SCALE_SMOOTH))), BorderLayout.WEST);
        }
        JLabel titleLbl = new JLabel(projectName + " - Apache NetBeans IDE 31");
        titleLbl.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        titleLbl.setForeground(new Color(0x1E, 0x1E, 0x1E));
        titleLeft.add(titleLbl, BorderLayout.CENTER);
        titleBar.add(titleLeft, BorderLayout.CENTER);

        // Windows 11 caption buttons
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
        titleBar.add(winBtns, BorderLayout.EAST);
        northWrap.add(titleBar);

        // 2. Menu Bar
        JMenuBar menuBar = new JMenuBar();
        menuBar.setBackground(new Color(0xF7, 0xF7, 0xF7));
        menuBar.setBorder(new MatteBorder(0, 0, 1, 0, new Color(0xE2, 0xE2, 0xE2)));
        String[] menus = {"File", "Edit", "View", "Navigate", "Source", "Refactor", "Run", "Debug", "Profile", "Team", "Tools", "Window", "Help"};
        for (String m : menus) {
            JMenu jm = new JMenu(m);
            jm.setFont(new Font("Segoe UI", Font.PLAIN, 12));
            menuBar.add(jm);
        }
        JPanel menuWrap = new JPanel(new BorderLayout());
        menuWrap.add(menuBar, BorderLayout.CENTER);
        northWrap.add(menuWrap);

        // 3. Main Toolbar
        JToolBar tb = new JToolBar();
        tb.setFloatable(false);
        tb.setBackground(new Color(0xF5, 0xF5, 0xF5));
        tb.setBorder(new CompoundBorder(new MatteBorder(0, 0, 1, 0, new Color(0xD9, 0xD9, 0xD9)), new EmptyBorder(3, 6, 3, 8)));
        Icon[] tbIcons = {icNewFile, icNewProj, icOpenProj, icSaveAll, null, icUndo, icRedo, null, icBuild, icCleanBuild, icRun, icDebug};
        String[] tbFallback = {"New", "NewProj", "Open", "Save", null, "Undo", "Redo", null, "Build", "Clean", "Run", "Debug"};
        for (int i = 0; i < tbIcons.length; i++) {
            if (tbIcons[i] == null) {
                tb.addSeparator(new Dimension(10, 22));
            } else {
                JButton btn = new JButton(tbIcons[i]);
                btn.setFocusable(false);
                btn.setOpaque(false);
                btn.setBorder(new EmptyBorder(3, 4, 3, 4));
                if (btn.getIcon() == null) btn.setText(tbFallback[i]);
                tb.add(btn);
            }
        }
        tb.add(Box.createHorizontalGlue());
        JTextField searchBox = new JTextField("Search (Ctrl+I)");
        searchBox.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        searchBox.setForeground(new Color(0x88, 0x88, 0x88));
        searchBox.setMaximumSize(new Dimension(160, 24));
        searchBox.setPreferredSize(new Dimension(160, 24));
        tb.add(searchBox);
        northWrap.add(tb);

        root.add(northWrap, BorderLayout.NORTH);

        // 4. Center SplitPane (Left Explorer + Right Editor)
        DefaultMutableTreeNode treeRoot = new DefaultMutableTreeNode("Projects");
        DefaultMutableTreeNode projNode = new DefaultMutableTreeNode(projectName);
        DefaultMutableTreeNode srcPkgNode = new DefaultMutableTreeNode("Source Packages");
        String pkgLabel = ar.packageName.isEmpty() ? "<default package>" : ar.packageName;
        DefaultMutableTreeNode pkgNode = new DefaultMutableTreeNode(pkgLabel);
        DefaultMutableTreeNode selectedFileNode = null;
        for (String ef : extraFiles) {
            DefaultMutableTreeNode fnNode = new DefaultMutableTreeNode(ef);
            pkgNode.add(fnNode);
            if (ef.equals(filename)) selectedFileNode = fnNode;
        }
        srcPkgNode.add(pkgNode);
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
                else if ((text.equals("Source Packages") || text.equals(pkgLabel)) && icPackage != null) setIcon(icPackage);
                else if (text.endsWith(".java") && icJavaFile != null) setIcon(icJavaFile);
                else if ((text.equals("Dependencies") || text.equals("Java Dependencies")) && icLibs != null) setIcon(icLibs);
                else if (text.equals("Project Files")) {
                    Icon closed = UIManager.getIcon("Tree.closedIcon");
                    if (closed != null) setIcon(closed);
                }
                if (text.equals(projectName)) setFont(getFont().deriveFont(Font.BOLD));
                else setFont(getFont().deriveFont(Font.PLAIN));
                return this;
            }
        });

        JTabbedPane leftTabs = new JTabbedPane(JTabbedPane.TOP);
        leftTabs.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        JScrollPane treeScroll = new JScrollPane(projTree);
        treeScroll.setBorder(BorderFactory.createEmptyBorder());
        leftTabs.addTab("Projects", icProjTab, treeScroll);
        leftTabs.addTab("Files", icFilesTab, new JPanel());
        leftTabs.addTab("Services", null, new JPanel());
        leftTabs.setPreferredSize(new Dimension(245, 420));

        // Right Editor TabbedPane + Source|History Toolbar + EditorCanvas
        EditorCanvas edCanvas = new EditorCanvas(code, ar, startLine, endLine, activeOffset, withCursor, withMarginGuide, jitterW, jitterH, nbHome, true);
        JPanel editorWrapper = new JPanel(new BorderLayout());
        editorWrapper.setBackground(Color.WHITE);

        // Thin Editor Source|History bar
        JPanel edToolbar = new JPanel(new FlowLayout(FlowLayout.LEFT, 4, 2));
        edToolbar.setBackground(new Color(0xF6, 0xF6, 0xF6));
        edToolbar.setBorder(new MatteBorder(0, 0, 1, 0, new Color(0xDF, 0xDF, 0xDF)));
        JToggleButton btnSource = new JToggleButton("Source", true);
        JToggleButton btnHistory = new JToggleButton("History", false);
        btnSource.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        btnHistory.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        btnSource.setMargin(new Insets(1, 7, 1, 7));
        btnHistory.setMargin(new Insets(1, 7, 1, 7));
        edToolbar.add(btnSource);
        edToolbar.add(btnHistory);

        editorWrapper.add(edToolbar, BorderLayout.NORTH);
        editorWrapper.add(edCanvas, BorderLayout.CENTER);

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

        JTabbedPane edTabs = new JTabbedPane(JTabbedPane.TOP);
        edTabs.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        edTabs.addTab(filename + "   \u00D7", icJavaFile, editorWrapper);

        JSplitPane split = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, leftTabs, edTabs);
        split.setDividerLocation(245);
        split.setDividerSize(4);
        split.setBorder(new EmptyBorder(4, 4, 2, 4));
        root.add(split, BorderLayout.CENTER);

        // 5. Bottom Status Bar
        JPanel statusBar = new JPanel(new BorderLayout());
        statusBar.setBackground(new Color(0xF2, 0xF2, 0xF2));
        statusBar.setBorder(new CompoundBorder(new MatteBorder(1, 0, 0, 0, new Color(0xD8, 0xD8, 0xD8)), new EmptyBorder(2, 10, 2, 12)));
        JLabel statusLeft = new JLabel(" ");
        statusLeft.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        String[] codeLines = code.split("\n", -1);
        int visStart = Math.max(1, startLine);
        int visEnd = (endLine <= 0 || endLine > codeLines.length) ? codeLines.length : endLine;
        int visCount = Math.max(1, visEnd - visStart + 1);
        int activeIdx = (activeOffset >= 0 && activeOffset < visCount) ? (visStart - 1 + activeOffset) : (visEnd - 1);
        int activeCol = (activeIdx >= 0 && activeIdx < codeLines.length) ? (codeLines[activeIdx].length() + 1) : 1;
        JLabel statusRight = new JLabel("Line " + (activeIdx + 1) + ", Col " + activeCol + "    |    INS");
        statusRight.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        statusRight.setForeground(new Color(0x40, 0x40, 0x40));
        statusRight.setHorizontalAlignment(SwingConstants.RIGHT);
        statusBar.add(statusLeft, BorderLayout.WEST);
        statusBar.add(statusRight, BorderLayout.CENTER);
        root.add(statusBar, BorderLayout.SOUTH);

        Dimension edDim = edCanvas.getPreferredSize();
        int totalW = Math.max(1020, 260 + edDim.width);
        int totalH = Math.max(620, 215 + edDim.height);
        root.setSize(totalW, totalH);
        layoutRecursive(root);

        double scale = 1.25;
        BufferedImage img = new BufferedImage((int) Math.round(totalW * scale), (int) Math.round(totalH * scale), BufferedImage.TYPE_INT_RGB);
        Graphics2D g = img.createGraphics();
        g.scale(scale, scale);
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
