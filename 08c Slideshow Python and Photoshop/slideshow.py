from photoshop import Session
import os
from PIL import Image
import operator


def resize(filename):
    HD_Size = (1920, 1080)

    image = Image.open(filename).convert('RGB')
    if image.size == HD_Size:  # shortcut return
        return

    image.thumbnail(HD_Size)

    offset = tuple(int(i / 2) for i in tuple(map(operator.sub, HD_Size, image.size)))
    background = Image.new(mode="RGB", size=HD_Size, color=(0, 0, 0))
    background.paste(image, offset)

    background.save(filename, dpi=(300, 300), quality=100)


def apply_template(template, filename, date, title):
    with Session(template, action='open', auto_close=True) as ps:
        doc = ps.active_document

        # apply title
        title_layer = doc.ArtLayers['Title']
        title_text_item = title_layer.TextItem
        title_text_item.contents = title

        # apply date
        date_layer = doc.ArtLayers['Date']
        date_text_item = date_layer.TextItem
        date_text_item.contents = date

        # import image
        doc.activeLayer = doc.ArtLayers['Image']
        replace_contents = ps.app.stringIDToTypeID("placedLayerReplaceContents")
        desc = ps.ActionDescriptor
        idnull = ps.app.charIDToTypeID("null")
        desc.putPath(idnull, filename)
        ps.app.executeAction(replace_contents, desc)

        # save
        ps.active_document.saveAs(filename, ps.JPEGSaveOptions(quality=10))


def create_slide(filename, title, date):
    template = os.path.join(os.getcwd(), 'template.psd')
    resize(filename)
    apply_template(template, filename, date, title)
