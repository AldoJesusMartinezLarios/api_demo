from PIL import Image
im = Image.open("images.jpg")
# im.show()

print(im.format, im.size, im.mode)

box = (0, 0, 400, 400)
region = im.crop(box)
region.save("recorte.jpg")

r, g, b = region.split()
region = Image.merge("RGB", (b, g, r))
region.save("cambio.jpg")

out = region.rotate(45)
out.save("giro.jpg")