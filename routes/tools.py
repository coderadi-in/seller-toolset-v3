"""coderadi &bull; Tools routing for the project."""

# ? IMPORTS
from flask import Blueprint, render_template, request, send_file, redirect, url_for
import coderadi.cropper as cropper
from coderadi.fba import generate_barcode
from coderadi.fba import LabelGridPDFService as LabelGenerator

# ! INITIALIZING TOOLS ROUTER & PLUGINS
tools = Blueprint("tools", __name__, url_prefix="/tools")
label_generator = LabelGenerator()

# & PDF CROPPER ROUTE
@tools.route("/pdf-cropper/")
def pdf_cropper():
    return render_template("pages/pdf_cropper.html")

# | PDF CROP HANDLER ROUTE
@tools.route("/pdf-cropper/crop", methods=["POST"])
def crop_pdf_route():
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

# & ROI CALCULATOR ROUTE
@tools.route('/roi-calculator/')
def roi_calculator():
    return render_template("pages/roi_calculator.html")

# & FBA GENERATOR ROUTE
@tools.route('/fba-generator/')
def fba_generator():
    return render_template("pages/fba_generator.html")

# | FBA GENERATE HANDLER ROUTE
@tools.route('/fba-generator/generate', methods=['POST'])
def generate_fba():
    # ACCESSING FORM DATA
    product_code = request.form.get('productCode')
    product_name = request.form.get('productName')
    product_price = request.form.get('productPrice')
    seller_credential = request.form.get('sellerCredential')

    # BEAUTIFY PRODUCT PRICE
    product_price = f"MRP {product_price}"

    # FORM VALIDATION
    if (not product_code) or (not product_name) or (not product_price) or (not seller_credential):
        return redirect(url_for('tools.fba_generator'))
    

    # GENERATE BARCODE & LABEL
    barcode = generate_barcode(product_code)
    pdf = label_generator.build_sheet([
        {
            "barcode": barcode,
            "lines": [
                product_price,
                product_name,
                seller_credential,
            ]
        } for _ in range(40)
    ])

    # RETURN OUTPUT
    return send_file(
        pdf,
        as_attachment=True,
        download_name="fba_label.pdf",
        mimetype="application/pdf"
    )