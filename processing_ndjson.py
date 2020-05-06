from PIL import Image
import ndjson

def create_image(image, filename):
    img = Image.new('RGBA', (256,256), (255, 255, 255, 0))
    pixels = img.load()

    x = -1
    y = -1
    weight =  5

    for stroke in image:
        for i in range(len(stroke[0])):
            if x != -1: 
                for point in get_line(stroke[0][i], stroke[1][i], x, y):
                    pixels[point[0],point[1]] = (0, 0, 0)
                    
                    for w1 in range(weight):
                        for w2 in range(weight):
                            pixels[min(point[0] + w1, 255),point[1]] = (0, 0, 0)
                            pixels[point[0],min(point[1] + w1, 255)] = (0, 0, 0)
                            pixels[min(point[0] + w1, 255),min(point[1] + w2, 255)] = (0, 0, 0)
                            pixels[max(point[0] - w1, 0), point[1]] = (0, 0, 0)
                            pixels[point[0] ,max(point[1] - w1, 0)] = (0, 0, 0)
                            pixels[max(point[0] - w1, 0), max(point[1] - w2, 0)] = (0, 0, 0)
                            pixels[min(point[0] + w1, 255), max(point[1] - w2, 0)] = (0, 0, 0)
                            pixels[max(point[0] - w1, 0), min(point[1] + w2, 255)] = (0, 0, 0)
                    
                    
                    
                    
            pixels[stroke[0][i],stroke[1][i]] = (0, 0, 0)
            x = stroke[0][i]
            y = stroke[1][i]
        x = -1
        y = -1
    img.save(filename, "PNG")

def get_line(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points
    
    


with open('raw_ndjson/full_simplified_smiley face.ndjson', 'r') as f:
    smiley_dict = ndjson.load(f)
count = 0
for smiles in smiley_dict:
    create_image(smiles['drawing'], "out_ndjson/" + str(count)+ ".png")
    count += 1
