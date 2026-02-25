"""coderadi &bull; Tools routing for the project."""

# ==================================================
# IMPORTS
# ==================================================

# ? IMPORTS
from flask import Blueprint, render_template, request, send_file, redirect, url_for
from datetime import datetime
from coderadi.refiner import refine
from coderadi.cropper import ShippingLabelCropper, InvoiceCropper
from coderadi.sheets import generate_barcode
from coderadi.sheets import LabelGridPDFService as LabelGenerator

# ==================================================
# INITIALIZATIONS
# ==================================================

# ! INITIALIZING TOOLS ROUTER & PLUGINS
tools = Blueprint("tools", __name__, url_prefix="/tools")
label_generator = LabelGenerator()

# ==================================================
# PDF CROPPER
# ==================================================

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
        output = ShippingLabelCropper.crop_flipkart(pdf_file)

    elif (platform == 'shopsy'):
        output = ShippingLabelCropper.crop_shopsy(pdf_file)

    elif (platform == 'meesho'):
        output = ShippingLabelCropper.crop_meesho(pdf_file)

    elif (platform  == 'amazon'):
        output = ShippingLabelCropper.process_amazon(pdf_file)

    # RETURN FILE
    return send_file(
        output,
        as_attachment=True,
        download_name="cropped_invoice.pdf",
        mimetype="application/pdf",
    )

# ==================================================
# INVOICE CROPPER
# ==================================================

# & INVOICE CROPPER ROUTE
@tools.route("/invoice-cropper/")
def invoice_cropper():
    return render_template("pages/invoice_cropper.html")

# | INVOICE CROP HANDLER ROUTE
@tools.route("/invoice-cropper/crop", methods=["POST"])
def crop_invoice_route():
    # ACCESS FORM DATA
    pdf_file = request.files.get('fileUpload')
    platform = request.form.get('platformSelect')

    # VALIDATION
    if (not pdf_file.read()):
        return redirect(url_for('tools.invoice_cropper'))
    
    if (platform == 'flipkart'):
        output = InvoiceCropper.crop_flipkart(pdf_file)

    elif (platform == 'shopsy'):
        output = InvoiceCropper.crop_shopsy(pdf_file)

    elif (platform == 'meesho'):
        output = InvoiceCropper.crop_meesho(pdf_file)

    elif (platform  == 'amazon'):
        output = InvoiceCropper.crop_amazon(pdf_file)

    # RETURN FILE
    return send_file(
        output,
        as_attachment=True,
        download_name="cropped_label.pdf",
        mimetype="application/pdf",
    )

# ==================================================
# SINGLE-ROUTED TOOLS
# ==================================================

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

# ==================================================
# FBA GENERATION
# ==================================================

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
    pdf = label_generator.build_sheet(label_type="fba", labels=[
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

# ==================================================
# BATCH GENERATION
# ==================================================

# & BATCH-GENERATOR ROUTE
@tools.route('/batch-generator/')
def batch_generator():
    return render_template('pages/batch_generator.html')

# | BATCH-GENERATION HANDLING ROUTE
@tools.route('/batch-generator/generate', methods=['POST'])
def generate_batch():
    # ACCESS FORM DATA
    product_code = request.form.get('productCode')
    product_variant = request.form.get('productVariant')
    product_price = request.form.get('productPrice')
    manufacture_date = request.form.get('manufactureDate')
    expiry_date = request.form.get('expiryDate')
    batch_number = request.form.get('batchNumber')

    # DATE FORMATION
    manufacture_date_obj = datetime.strptime(manufacture_date, "%Y-%m-%d")
    expiry_date_obj = datetime.strptime(expiry_date, "%Y-%m-%d")
    formatted_manufacture_date = manufacture_date_obj.strftime("%d/%m/%Y")
    formatted_expiry_date = expiry_date_obj.strftime("%d/%m/%Y")

    # BEAUTIFICATION
    product_price = f"M.R.P.: {product_price}"
    manufacture_date = f"M.F.G.: {formatted_manufacture_date}"
    expiry_date = f"E.X.P: Best before {formatted_expiry_date}"
    batch_number = f"Batch no.: {batch_number}"

    # GENERATE BARCODE & LABEL
    barcode = generate_barcode(product_code, with_label=False)
    pdf = label_generator.build_sheet(label_type="batch", labels=[
        {
            "barcode": barcode,
            "lines": {
                "id": product_code,
                "variant": product_variant,
                "price": product_price,
                "batch": batch_number,
                "mfd": manufacture_date,
                "exp": expiry_date
            }
        } for _ in range(36)
    ], grid=(9, 3))

    # RETURN OUTPUT
    return send_file(
        pdf,
        as_attachment=True,
        download_name="batch_label.pdf",
        mimetype="application/pdf"
    )

# ==================================================
# IMAGE REFINING
# ==================================================

# & IMAGE REFINING ROUTE
@tools.route('/image-refiner/')
def image_refiner():
    return render_template("pages/image_refiner.html")

# | IMAGE REFINE HANDLER ROUTE
@tools.route('/image-refiner/refine', methods=['POST'])
def refine_image():
    # ACCESS FORM DATA
    input_image = request.files.get('fileUpload')

    # VALIDATION
    if (not input_image.read()):
        return redirect(url_for('tools.image_refiner'))
    
    # REFINE IMAGE
    refined_bytes = refine(input_image)

    # RETURN OUTPUT
    return send_file(
        refined_bytes,
        as_attachment=True,
        download_name="refined_image.jpg",
        mimetype="image/jpeg",
    )