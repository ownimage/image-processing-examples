from PIL import Image, ImageDraw, ImageFont, ImageFilter
import operator

def create_slide(filename, title_text, date_text):
# Load the image
    HD_Size = (1920, 1080)

    image = Image.open(filename).convert('RGB')
    image.thumbnail(HD_Size)

    offset = tuple(int(i/2) for i in tuple(map(operator.sub,HD_Size, image.size)))
    background = Image.new(mode = "RGBA", size = HD_Size, color = (0, 0, 0))
    background.paste(image, offset)

    # Define the text properties
    title_font = ImageFont.truetype('Filmotype Lasalle.ttf', 120)
    date_font  = ImageFont.truetype('Seven Segment.ttf', 46.67)

    # calc title size
    ts_image = Image.new('RGBA', background.size)
    ts_draw = ImageDraw.Draw(ts_image)
    _, _, w, h = ts_draw.textbbox((0,0), title_text, font=title_font)

    title_position = (1860-w, h-50)
    date_position = (50, 980)

    # Create a title drawing context
    title_blurred = background.copy() # Image.new('RGBA', background.size) #
    title_draw = ImageDraw.Draw(title_blurred)

    # Add white title text to the image and blur
    title_draw.rectangle(((0,0), HD_Size), fill=(0,0,0,0))
    title_draw.text(title_position, title_text, fill='#ffffff', font=title_font, stroke_width=9, stroke_fill="white")
    title_blurred = title_blurred.filter(ImageFilter.GaussianBlur(4))

    # Add black title
    title_draw = ImageDraw.Draw(title_blurred)
    title_draw.text(title_position, title_text, font=title_font, fill='#000000')

    # Paste title to background
    background.paste(title_blurred, title_blurred)

    # Create a title drawing context
    date_blurred = Image.new('RGBA', background.size)
    date_draw = ImageDraw.Draw(date_blurred)

    # Add white title text to the image and blur
    date_draw.text(date_position, date_text, fill='#ffffff', font=date_font, stroke_width=5, stroke_fill="white")
    date_blurred = date_blurred.filter(ImageFilter.GaussianBlur(2))

    # Add black title
    date_draw = ImageDraw.Draw(date_blurred)
    date_draw.text(date_position, date_text, font=date_font, fill='#000000')

    # Paste title to background
    background.paste(date_blurred, date_blurred)

    # Save or display the modified image
    background.convert('RGB').save(filename)