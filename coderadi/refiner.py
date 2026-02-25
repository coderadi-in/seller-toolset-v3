import io
import numpy as np
from PIL import Image

# * FUNCTION TO REFINE IMAGE
def refine(file_stream: io.BytesIO, canvas_size: int = 1000, quality: int = 75):
    """
    file_stream: file-like object (request.files['image'])
    returns: io.BytesIO (optimized image)
    """

    img = Image.open(file_stream).convert("RGBA")

    # ---------- remove metadata ----------
    data = np.array(img)

    # ---------- tight crop ----------
    alpha = data[:, :, 3]
    coords = np.argwhere(alpha > 0)

    if coords.size:
        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0)
        img = img.crop((x0, y0, x1, y1))

    # ---------- resize to square canvas ----------
    img.thumbnail((canvas_size - 100, canvas_size - 100))

    canvas = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 255))

    w, h = img.size
    canvas.paste(img, ((canvas_size - w) // 2, (canvas_size - h) // 2))

    # ---------- compress ----------
    output = io.BytesIO()
    canvas.convert("RGB").save(
        output,
        format="JPEG",
        quality=quality,
        optimize=True
    )

    output.seek(0)
    return output

# * FUNCTION TO CONVERT IMAGE TO OTHER FORMATS
def convert(image_file: io.BytesIO, output_format: str = 'jpeg') -> io.BytesIO:
    '''
    Converts image format to another format

    :param image_file: The image file to convert.
    :param output_format: The output format for the file.
    '''

    # INITIALIZE IMAGE PROCESSORS
    image = Image.open(image_file)
    buffer = io.BytesIO()

    # REFINE JPEG COMPATIBILITY
    if (image.mode == 'RGBA') and (output_format == 'jpeg'):
        image = image.convert('RGB')

    # SAVE IMAGE TO BUFFER
    image.save(buffer, output_format)
    buffer.seek(0)
    return buffer