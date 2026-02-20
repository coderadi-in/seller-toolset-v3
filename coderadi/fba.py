'''
coderadi &bull; Manages all FBA generation functions
'''

# ? IMPORTS
from io import BytesIO

import barcode
from barcode.writer import ImageWriter

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

# * FUNCTION TO GENERATE BARCODE
def generate_barcode(code: str) -> BytesIO:
    '''
    Generates barcode image in memory

    :param code: The code to encode in barcode.
    :rtype: io.BytesIo
    '''

    buffer = BytesIO()

    barcode_class = barcode.get_barcode_class("code128")
    generated_barcode = barcode_class(code, writer=ImageWriter())

    generated_barcode.write(buffer)
    buffer.seek(0)

    return buffer

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO


class LabelGridPDFService:

    COLS = 4
    ROWS = 10

    def build_sheet(self, labels: list[dict]) -> BytesIO:
        """
        labels = [
            {"code": "ABC123", "lines": ["Product A", "₹99"]},
            ...
        ]
        """

        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=A4)

        page_width, page_height = A4

        cell_w = page_width / self.COLS
        cell_h = page_height / self.ROWS

        for i, label in enumerate(labels):
            col = i % self.COLS
            row = i // self.COLS

            if row >= self.ROWS:
                break  # max 40

            x = col * cell_w
            y = page_height - ((row + 1) * cell_h)

            self._draw_single_label(c, x, y, cell_w, cell_h, label)

        c.showPage()
        c.save()

        pdf_buffer.seek(0)
        return pdf_buffer


    def _draw_single_label(self, c, x, y, w, h, label):
        padding = 10
        c.rect(x, y, w, h)

        # -------------------------
        # BARCODE AT TOP
        # -------------------------
        barcode_height = 40

        barcode_img = ImageReader(label["barcode"])

        c.drawImage(
            barcode_img,
            x + padding,
            y + h - barcode_height - padding,
            width=w - 2 * padding,
            height=barcode_height,
            preserveAspectRatio=True
        )

        # -------------------------
        # TEXT BELOW BARCODE
        # -------------------------
        text_y = y + h - barcode_height - 10

        c.setFont("Helvetica", 9)

        for line in label["lines"]:
            c.drawString(x + padding, text_y, line)
            text_y -= 12