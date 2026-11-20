from byuimage import Image

# ============================================================
# BASIC IMAGE HELPERS
# ============================================================
def load_image(filename):
    """Load image"""
    return Image(filename)
def resize_image(img, new_w, new_h):
    """Makes them the same size"""
    resized = Image.blank(new_w, new_h)
    for y in range(new_h):
        for x in range(new_w):
            src_x = int(x * img.width / new_w)
            src_y = int(y * img.height / new_h)
            src_pixel = img.get_pixel(src_x, src_y)
            dst_pixel = resized.get_pixel(x, y)
            dst_pixel.red = src_pixel.red
            dst_pixel.green = src_pixel.green
            dst_pixel.blue = src_pixel.blue
    return resized
def grayscale(filename):
    """Make it gray"""
    img = load_image(filename)
    for pixel in img:
        avg = (pixel.red + pixel.green + pixel.blue) // 3
        pixel.red = pixel.green = pixel.blue = avg
    return img
def build_horizontal_row(file1, file2, file3, file4, border):
    """Makes row collage """
    img1 = load_image(file1)
    img2 = load_image(file2)
    img3 = load_image(file3)
    img4 = load_image(file4)
    w, h = img1.width, img1.height
    final_width = (w * 4) + (border * 5)
    final_height = h + (border * 2)
    row_canvas = Image.blank(final_width, final_height)
    for pixel in row_canvas:
        pixel.red = pixel.green = pixel.blue = 0
    def paste(src, dest, off_x, off_y):
        for y in range(src.height):
            for x in range(src.width):
                s = src.get_pixel(x, y)
                d = dest.get_pixel(x + off_x, y + off_y)
                d.red = s.red
                d.green = s.green
                d.blue = s.blue
    paste(img1, row_canvas, border, border)
    paste(img2, row_canvas, w + (border * 2), border)
    paste(img3, row_canvas, (w * 2) + (border * 3), border)
    paste(img4, row_canvas, (w * 3) + (border * 4), border)
    return row_canvas
# ============================================================
# PORTRAIT PROCESSING
# ============================================================
STANDARD_SIZE = 225  
def make_eliminated_portrait(pilot):
    """Grays out image if eliminated"""
    src = pilot.portrait_path
    out = pilot.portrait_gray_path
    img = grayscale(src)
    img = resize_image(img, STANDARD_SIZE, STANDARD_SIZE)
    img.save(out)
    return out
def make_active_portrait(pilot):
    """Adjust winner image"""
    src = pilot.portrait_path
    out = src.replace(".png", "_resized_temp.png")
    img = load_image(src)
    img = resize_image(img, STANDARD_SIZE, STANDARD_SIZE)
    img.save(out)
    return out
# ============================================================
# FINAL TOURNAMENT COLLAGE (2×4 grid panorama)
# ============================================================
def combine_two_collages(top, bottom, border):
    """Merge collages"""
    w, h = top.width, top.height
    final_width = w
    final_height = (h * 2) + border
    final = Image.blank(final_width, final_height)
    for pixel in final:
        pixel.red = pixel.green = pixel.blue = 0
    for y in range(top.height):
        for x in range(top.width):
            s = top.get_pixel(x, y)
            d = final.get_pixel(x, y)
            d.red = s.red
            d.green = s.green
            d.blue = s.blue
    for y in range(bottom.height):
        for x in range(bottom.width):
            s = bottom.get_pixel(x, y)
            d = final.get_pixel(x, y + top.height + border)
            d.red = s.red
            d.green = s.green
            d.blue = s.blue
    return final
def build_final_collage(pilots, champion, border=10):
    """Callage made based off results"""
    processed = []
    for p in pilots:
        if p == champion:
            processed.append(make_active_portrait(p))
        else:
            processed.append(make_eliminated_portrait(p))
    top = build_horizontal_row(processed[0], processed[1], processed[2], processed[3], border)
    bottom = build_horizontal_row(processed[4], processed[5], processed[6], processed[7], border)
    final = combine_two_collages(top, bottom, border)
    final.save("tournament_final.png")
    final.show()
    return final