import os
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

class LaprakDocxBuilder:
    def __init__(self, template_path=None):
        self.template_path = template_path
        if template_path and os.path.exists(template_path):
            self.doc = docx.Document(template_path)
        else:
            self.doc = docx.Document()
            self._setup_default_styles()

    def _setup_default_styles(self):
        # Configure standard 1-inch margins
        for section in self.doc.sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)

    def set_cover_title(self, pertemuan_text, modul_title_text):
        if len(self.doc.paragraphs) > 2:
            self.doc.paragraphs[1].text = pertemuan_text
            self.doc.paragraphs[2].text = f"“{modul_title_text}”"

    def clear_guided_section(self, keep_until_p_index=35):
        """Clears existing guided paragraphs in a template to rebuild fresh."""
        while len(self.doc.paragraphs) > keep_until_p_index:
            p = self.doc.paragraphs[-1]
            p._element.getparent().remove(p._element)

    def add_section_heading(self, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
        p = self.doc.add_paragraph(style='Normal')
        p.alignment = align
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.font.bold = True
        return p

    def add_label(self, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
        p = self.doc.add_paragraph(style='Normal')
        p.alignment = align
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.font.bold = True
        return p

    def add_explanation_paragraph(self, text, indent=Inches(0.4), align=WD_ALIGN_PARAGRAPH.JUSTIFY):
        """
        Adds an indented explanation paragraph with normal non-bold Times New Roman font.
        """
        p = self.doc.add_paragraph(style='Normal')
        p.alignment = align
        p.paragraph_format.first_line_indent = indent
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.font.bold = False
        return p

    def add_paragraph_text(self, text, bold=False, indent=None, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
        p = self.doc.add_paragraph(style='Normal')
        p.alignment = align
        if indent:
            p.paragraph_format.first_line_indent = indent
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.font.bold = bold
        return p

    def add_code_item(self, item_title, image_paths, explanation_text, img_width=Inches(5.2)):
        """
        Appends a code task item:
        - Title (e.g. 1.) TestJDBC.java)
        - 'Kode'
        - Embedded screenshots
        - 'Penjelasan'
        - Indented non-bold explanation paragraph
        """
        self.add_section_heading(item_title)
        self.add_label("Kode")

        w = img_width if img_width is not None else Inches(5.2)
        for img_path in image_paths:
            if os.path.exists(img_path):
                p_img = self.doc.add_paragraph(style='Normal')
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(4)
                p_img.paragraph_format.space_after = Pt(6)
                p_img.add_run().add_picture(img_path, width=w)

        self.add_label("Penjelasan")
        self.add_explanation_paragraph(explanation_text)

        # Subtle blank space
        p_blank = self.doc.add_paragraph(style='Normal')
        p_blank.paragraph_format.space_before = Pt(2)
        p_blank.paragraph_format.space_after = Pt(2)

    def add_output_section(self, output_images, default_width=Inches(4.8)):
        """
        Appends the Output section with screenshots.
        """
        self.add_section_heading("Output")
        for item in output_images:
            if isinstance(item, tuple):
                img_path, w = item
            else:
                img_path, w = item, default_width

            if os.path.exists(img_path):
                p_img = self.doc.add_paragraph(style='Normal')
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(4)
                p_img.paragraph_format.space_after = Pt(6)
                p_img.add_run().add_picture(img_path, width=w)

    def save(self, output_path):
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        self.doc.save(output_path)
        return output_path
