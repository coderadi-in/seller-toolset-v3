"""coderadi &bull; Tools routing for the project."""

# ? IMPORTS
from flask import Blueprint, render_template, request, send_file, redirect, url_for
from pypdf import PdfReader, PdfWriter
from io import BytesIO
import time

# ! INITIALIZING TOOLS ROUTER
tools = Blueprint("tools", __name__, url_prefix="/tools")

# & PDF CROPPER ROUTE
@tools.route("/pdf-cropper/")
def pdf_cropper():
    return render_template("pages/pdf_cropper.html")

# | PDF CROP HANDLER ROUTE
@tools.route("/pdf-cropper/crop", methods=["POST"])
def crop_pdf_route():
    start = time.time()
    # ACCESSING FORM DATA
    pdf_file = request.files.get("fileUpload")
    platform = request.form.get("platformSelect")

    # VALIDATION
    if (not pdf_file.read()):
        return redirect(url_for('tools.pdf_cropper'))
    
    # INITIALIZING PDF MANAGEMENT
    reader = PdfReader(pdf_file)
    writer = PdfWriter()
    output = BytesIO()

    # ITERATING OVER THE PDF FILE
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

    end = time.time()
    print("Cropped {} pages in {} seconds".format(len(reader.pages), end - start))

    # RETURN FILE
    return send_file(
        output,
        as_attachment=True,
        download_name="cropped_label.pdf",
        mimetype="application/pdf",
    )


# & CR CALCULATOR ROUTE
@tools.route("/cr-calculator/")
def cr_calculator():
    return render_template("pages/cr_calculator.html")


# & PRICE CALCULATOR ROUTE
@tools.route("/price-calculator/")
def price_calculator():
    return render_template("pages/price_calculator.html")