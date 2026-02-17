"""coderadi &bull; Tools routing for the project."""

# ? IMPORTS
from flask import Blueprint, render_template, request, send_file, redirect, url_for
import coderadi.cropper as cropper
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
    
    if (platform == 'flipkart'):
        output = cropper.crop_flipkart(pdf_file)

    elif (platform == 'shopsy'):
        output = cropper.crop_shopsy(pdf_file)

    elif (platform == 'meesho'):
        output = cropper.crop_meesho(pdf_file)

    elif (platform  == 'amazon'):
        output = cropper.process_amazon(pdf_file)

    end = time.time()
    print("Cropped in {} seconds".format(end - start))

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