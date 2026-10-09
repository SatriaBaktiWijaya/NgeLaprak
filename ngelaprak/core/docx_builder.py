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

    def add_section_heading(self, text, style='Heading 1', align=WD_ALIGN_PARAGRAPH.JUSTIFY):
        p = self.doc.add_paragraph()
        p.style = style
        p.alignment = align
        r = p.add_run(text)
        r.font.size = Pt(11)
        r.font.name = 'Times New Roman'
        return p

    def add_paragraph_text(self, text, style='Heading 1', align=WD_ALIGN_PARAGRAPH.JUSTIFY):
        p = self.doc.add_paragraph()
        p.style = style
        p.alignment = align
        r = p.add_run(text)
        r.font.size = Pt(11)
        r.font.name = 'Times New Roman'
        return p

    def add_code_item(self, item_title, image_paths, explanation_text, img_width=Inches(5.4)):
        """
        Appends a code task item:
        - Title (e.g. 1.) TestJDBC.java)
        - 'Kode'
        - Embedded screenshots
        - 'Penjelasan'
        - Explanation text
        """
        self.add_section_heading(item_title)
        self.add_paragraph_text("Kode")

        w = img_width if img_width is not None else Inches(5.2)
        for img_path in image_paths:
            if os.path.exists(img_path):
                p_img = self.doc.add_paragraph()
                p_img.style = 'Heading 1'
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.add_run().add_picture(img_path, width=w)

        self.add_paragraph_text("Penjelasan")
        self.add_paragraph_text(explanation_text)
        
        # Blank space
        p_blank = self.doc.add_paragraph()
        p_blank.style = 'Heading 1'

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
                p_img = self.doc.add_paragraph()
                p_img.style = 'Heading 1'
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.add_run().add_picture(img_path, width=w)

    def save(self, output_path):
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        self.doc.save(output_path)
        return output_path
