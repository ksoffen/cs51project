from PIL import Image 

# useful PIL handbook
# http://www.pythonware.com/media/data/pil-handbook.pdf

# from http://stackoverflow.com/questions/9506841/using-python-pil-to-turn-a-rgb-image-into-a-pure-black-and-white-image
# CONVERT TO BLACK AND WHITE
'''im = Image.open("paragraph.png") # open colour image
im = im.convert('1') # convert image to black and white
im.save('paragraph-bw.png')'''

# by Amna
# from http://stackoverflow.com/questions/1109422/getting-list-of-pixel-values-from-pil
'''im = Image.open("testimage3.png")
pixels = im.load() # this is not a list, nor is it list()'able
width, height = im.size
all_pixels = []
    for x in range(width):
        for y in range(height):
            cpixel = pixels[x, y]
            all_pixels.append(cpixel)
print all_pixels'''

# remove entire rows of black pixels
# from http://stackoverflow.com/questions/12770218/using-pil-or-a-numpy-array-how-can-i-remove-entire-rows-from-an-image
'''
from PIL import Image

def find_rows_with_color(pixels, width, height, color):
    rows_found=[]
    for y in xrange(height):
        for x in xrange(width):
            if pixels[x, y] != color:
                break
        else:
            rows_found.append(y)
    return rows_found

old_im = Image.open("path/to/old/image.png")
if old_im.mode != 'RGB':
    old_im = old_im.convert('RGB')
pixels = old_im.load()
width, height = old_im.size[0], old_im.size[1]

rows_to_remove = find_rows_with_color(pixels, width, height, (0, 0, 0)) #Remove black rows
new_im = Image.new('RGB', (width, height - len(rows_to_remove)))
pixels_new = new_im.load()

rows_removed = 0
for y in xrange(old_im.size[1]):
    if y not in rows_to_remove:
        for x in xrange(new_im.size[0]):
            pixels_new[x, y - rows_removed] = pixels[x, y]
    else:
        rows_removed += 1
        
new_im.save("path/to/new/image.png")
'''

class ProcessedImage(object):
    def __init__(self, file, font_size):
        self.image = Image.open(file).convert('1')
        self.pixels = self.image.load()
        self.width, self.height = self.image.size
        self.space = Image.new('1', size = (30,30), color = 255)
        self.font_size = font_size
        
    '''def crop_margins(self):
        def col_blank(x):
            for y in range (self.height):
                #print "y: " + str(y)
                if self.pixels[x,y] != 255:
                    return False
            return True
        
        left, right = None, None
        
        #print "L E F T ! ! ! ! !"
        for x in range(self.width):
            #print "x: " + str(x)
            if not col_blank(x):
                left = x
                break
                
                
        #print "R I G H T ! ! ! ! !"
        for x in range(self.width):
            #print "x: " + str(self.width - x - 1)
            if not col_blank(self.width - x - 1):
                right = x
                break
        
        #print "CROPPING: (" + str(left) + ", 0, " + str(self.width - right) + ", " + str(self.height) + ")"
        self.image = im.crop((left, 0, self.width - right, self.height))
        self.pixels = self.image.load()
        self.width = self.width - left - right'''
    
    # returns an array of the lines of text in a scanned document
    def get_lines(self):
        # determines whether a row has only white pixels
        def row_blank(y):
            for x in range(self.width):
                if self.pixels[x,y] != 255:
                    return False
            return True
    
        lower, upper = None, None
        prev_blank = True
        lines = []
        
        for y in range(self.height):
            if row_blank(y):
                if not prev_blank:
                    lower = y
                prev_blank = True
            else:
                if prev_blank:
                    upper = y
                    saved = False
                prev_blank = False
            if lower > upper and not saved:
                box = (0, upper, self.width, lower)
                copy = self.image.crop(box)
                lines.append(copy)
                saved = True
        return lines
    
    # returns an array of the characters in a scanned document

    # returns an array of the characters in a split document
    # T0D0: pull out space characters


    def get_chars(self):
        # determines whether a column has only white pixels
        def col_blank(x, height, pixels):
            for y in range(height):
                if (pixels[x,y] != 255) and (pixels[x-1,y] != 255):
                    return False
            return True
        
        def copy(left, top, right, bottom):
            box = (left, top, right, bottom)
            return line.crop(box)
        
        # splits a line of text into separate characters
        def split_line(line):
            left, right = None, None
            width, height = line.size
            blanks = 0
            prev_blank = True
            chars = []
            for x in range(width):
                if col_blank(x, height, line.load()):
                    if not prev_blank:
                        right = x
                    prev_blank = True
                    blanks += 1
                else:
                    if prev_blank:
                        left = x
                        copied = False
                    prev_blank = False
                    if blanks > self.font_size:
                        chars.append(self.space)
                    blanks = 0
                if right > left and not copied:
                    chars.append(copy(left, 0, right, height))
                    copied = True
                
            return chars
    
        lines = self.get_lines()
        '''print len(lines)'''
        chars = []
        
        # iterates through every line, splits into chars, builds flat list of chars
        for line in lines:
            line_chars = split_line(line)
            for char in line_chars:
                '''print len(line_chars)'''
                chars.append(char)
    	return chars

    # returns array of character images resized to 30 by 30 pixel invariant
    def resize(self):
    	resizedchars = []
    # from http://stackoverflow.com/questions/1572691/in-python-python-image-library-1-1-6-how-can-i-expand-the-canvas-without-resiz
        # iterates through flat list of chars
        chars = self.get_chars()
        for x in chars:
        	newsize = 30.0
        	old_w, old_h = x.size
        	if old_w > old_h:
        		newwidth = int(newsize)
        		newheight = int(old_h * (newsize / old_w))
        		new = x.resize((newwidth, newheight), Image.ANTIALIAS)
        	else:
        		newwidth = int(old_w * (newsize / old_h))
        		newheight = int(newsize)
        		new = x.resize((newwidth, newheight), Image.ANTIALIAS)
        	newImage = Image.new('1', size = (30,30), color=255)
        	if old_w > old_h:
        		newImage.paste(new, (0, int((newsize-old_h) / 2)))
        	else:
        		newImage.paste(new, (int((newsize - old_w) / 2), 0))
        	resizedchars.append(newImage)
        return resizedchars

# testing above code on paragraph.png
test = ProcessedImage('paragraph.png', 12)
chars = test.get_chars()
chars2 = test.resize()


'''count = 1
for line in lines:
    line.save('line' + str(count) + '.png')
    count += 1'''

count = 1
for x in chars2:
    x.save('letters/resizedchar' + str(count) + '.png')
    count += 1
