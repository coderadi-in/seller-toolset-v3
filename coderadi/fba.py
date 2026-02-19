'''
coderadi &bull; Manages all FBA generation functions
'''

# ? IMPORTS
from io import BytesIO
import barcode
from barcode.writer import ImageWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
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

# & LABEL GRID GENERATION SERVICE
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
        """
        Draws ONE label inside its cell
        """

        padding = 10

        # Optional border (great for debugging layout)
        c.rect(x, y, w, h)

        # ---- Text ----
        text_y = y + h - 20

        c.setFont("Helvetica", 9)

        for line in label["lines"]:
            c.drawString(x + padding, text_y, line)
            text_y -= 12

        # ---- Barcode ----
        barcode_img = ImageReader(label["barcode"])

        c.drawImage(
            barcode_img,
            x + padding + 20,
            y + 10,
            width=w - 2 * padding,
            height=35,
            preserveAspectRatio=True
        )

# * FUNCTION TO GENERATE FBA LABEL
def generate_fba_label(content: list[str], barcode: BytesIO) -> BytesIO:
    '''
    Generates FBA label PDF

    :param content: A list of texts to add in FBA label.
    :param barcode: The barcode to add in text.
    :rtype: io.BytesIO
    '''

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # TEXT
    y = height - 50
    for line in content:
        c.drawString(50, y, line)
        y -= 20

    # BARCODE
    barcode_image = ImageReader(barcode)
    c.drawImage(
        barcode_image, 50, y- 120,
        width=300, height=80
    )

    c.showPage()
    c.save()

    buffer.seek(0)

    return buffer