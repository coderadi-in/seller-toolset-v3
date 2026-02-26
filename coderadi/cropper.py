'''
coderadi &bull; Manages all cropping functions
'''

# ? IMPORTS
from pypdf import PdfReader, PdfWriter
from io import BytesIO
from reportlab.pdfgen import canvas
import re

# & SHIPPING LABEL CROPPING SERVICE
class ShippingLabelCropper:
    # * FUNCTION TO CROP FLIPKART PDF
    def crop_flipkart(pdf_file):
        '''
        Crops flipkart shipping label
        
        :param pdf_file: The pdf file containing all invoices
        '''

        # INITIALIZING PDF PROCESSORS
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        output = BytesIO()

        # CROPPING PAGES
        for page in reader.pages:
            # SETTING FIRST RATIO
            page.mediabox.upper_right = (
                page.mediabox.width * 0.7,
                page.mediabox.height - page.mediabox.height * 0.03
            )

            # SETTING SECOND RATIO
            page.mediabox.lower_left = (
                page.mediabox.width * 0.43,
                page.mediabox.height * 0.55
            )

            # ADDING UPDATED RATIO IN PDF WRITER
            writer.add_page(page)
        
        # WRITING NEW PDF
        writer.write(output)
        output.seek(0)
        return output

    # * FUNCTION TO CROP SHOPSY PDF
    def crop_shopsy(pdf_file):
        '''
        Crops shopsy shipping label
        
        :param pdf_file: The pdf file containing all invoices
        '''

        # INITIALIZING PDF PROCESSORS
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        output = BytesIO()

        # CROPPING PAGES
        for page in reader.pages:
            # SETTING FIRST RATIO
            page.mediabox.upper_right = (
                page.mediabox.width * 0.7,
                page.mediabox.height - page.mediabox.height * 0.03
            )

            # SETTING SECOND RATIO
            page.mediabox.lower_left = (
                page.mediabox.width * 0.43,
                page.mediabox.height * 0.55
            )

            # ADDING UPDATE RATIO IN PDF WRITER
            writer.add_page(page)
        
        # WRITING NEW PDF
        writer.write(output)
        output.seek(0)
        return output

    # * FUNCTION TO CROP MEESHO PDF
    def crop_meesho(pdf_file):
        '''
        Crops meesho shipping label
        
        :param pdf_file: The pdf file containing all invoices
        '''
        
        # INITIALIZING PDF PROCESSORS
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        output = BytesIO()

        # CROPPING PAGES
        for page in reader.pages:
            page.mediabox.lower_left = (
                0,
                page.mediabox.height - page.mediabox.height * 0.45
            )

            # ADDING UPDATE RATIO IN PDF WRITER
            writer.add_page(page)
        
        # WRITING NEW PDF
        writer.write(output)
        output.seek(0)
        return output

    # * FUNCTION TO PROCESS AMAZON INVOICES
    def process_amazon(pdf_file):
        '''
        Processes amazon invoices
        
        :param pdf_file: The pdf file containing amazon invoices
        '''

        # INITIALIZING PDF PROCESSORS
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        stamped_writer = PdfWriter()
        output = BytesIO()
        item_index = 0

        # INITIALIZE TEXT EXTRACTION PROCESSORS
        code_pattern = re.compile(r"\|\s*B0[A-Z0-9]+\s*\(\s*([^)]+?)\s*\)")
        qty_pattern = re.compile(r"₹[\d,.]+\s+(\d+)\s+₹")
        results = []

        # EXTRACT PRODUCT_CODE & QUANTITY AND TAKE OUT SHIPPING LABELS IN DIFFERENT PDF
        for (idx, page) in enumerate(reader.pages):
            text = page.extract_text() or ""

            if ("Tax Invoice" not in text):
                writer.add_page(page)
                continue

            code_match = code_pattern.search(text)
            code = code_match.group(1).strip() if (code_match) else None

            qty_match = qty_pattern.search(text)
            qty = qty_match.group(1).strip() if (qty_match) else None

            if (code) and (qty):
                results.append({
                    'idx': idx,
                    'code': code,
                    'qty': qty
                })

        # STAMPING DATA ON SHIPPING LABELS
        for page in writer.pages:
            # ACCESS DIMENSIONS
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            
            # INITIALIZE STAMP TEXT
            item = results[item_index]
            stamp = f"({item['code']}) (Qty: {item['qty']})"
            
            # CREATE PAGE WITH STAMP
            packet = BytesIO()
            c = canvas.Canvas(packet, (width, height))

            # STAMP TEXT ON PDF
            c.setFont("Helvetica-Bold", 10)
            c.drawString(60.0, 150.0, stamp)
            c.save()
            packet.seek(0)

            overlay_page = PdfReader(packet).pages[0]
            page.merge_page(overlay_page)
            
            stamped_writer.add_page(page)
            item_index += 1

        stamped_writer.write(output)
        output.seek(0)
        return output
    
# & INVOICE CROPPING SERVICE
class InvoiceCropper:
    # * FUNCTION TO CROP FLIPKART INVOICE
    def crop_flipkart(pdf_file):
        '''
        Crops flipkart invoice

        :param pdf_file: The pdf file containing all invoices
        '''

        # INITIALIZE PDF PROCESSORS
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        output = BytesIO()

        # CROP PAGES
        for page in reader.pages:
            # SET FIRST RATIO
            page.mediabox.upper_right = (
                page.mediabox.width,
                page.mediabox.height * 0.55
            )

            # ADD UPDATED RATIO IN PDF WRITER
            writer.add_page(page)

        # PROCESS AND RETURN OUTPUT
        writer.write(output)
        output.seek(0)
        return output

    # * FUNCTION TO CROP SHOPSY INVOICE
    def crop_shopsy(pdf_file):
        '''
        Crops shopsy invoice
        
        :param pdf_file: The pdf file containing all invoices
        '''

        # INITIALIZE PDF PROCESSORS
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        output = BytesIO()

        # CROP PAGES
        for page in reader.pages:
            # SET FIRST RATIO
            page.mediabox.upper_right = (
                page.mediabox.width,
                page.mediabox.height * 0.55
            )

            # ADD UPDATED RATIO IN PDF WRITER
            writer.add_page(page)

        # PROCESS AND RETURN OUTPUT
        writer.write(output)
        output.seek(0)
        return output

    # * FUNCTION TO CROP MEESHO INVOICE
    def crop_meesho(pdf_file):
        '''
        Crops meesho invoice
        
        :param pdf_file: The pdf file containing all invoices
        '''
        
        # INITIALIZING PDF PROCESSORS
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        output = BytesIO()

        # CROP PAGES
        for page in reader.pages:
            page.mediabox.upper_right = (
                page.mediabox.width,
                page.mediabox.height - page.mediabox.height * 0.41
            )

            # ADD UPDATED RATIO IN PDF WRITER
            writer.add_page(page)

        # PROCESS AND RETURN OUTPUT
        writer.write(output)
        output.seek(0)
        return output

    # * FUNCTION TO SPLIT-OUT AMAZON INVOICE
    def crop_amazon(pdf_file):
        '''
        Splits-out amazon invoice

        :param pdf_file: The pdf file containing amazon invoices
        '''

        # INITIALIZE PDF PROCESSORS
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        output = BytesIO()

        # SPLIT-OUT INVOICES
        for page in reader.pages:
            text = page.extract_text() or ""

            if ("Tax Invoice" in text):
                writer.add_page(page)
                continue

        # PROCESS AND RETURN OUTPUT
        writer.write(output)
        output.seek(0)
        return output