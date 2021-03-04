import re
import math
import random
import time

import spiral

from collections import Counter
from itertools import cycle
from PIL import Image, ImageDraw, ImageFont, ImageStat

#----------------------------------------------------------------------------------------#

def process_image(wordlist):

    MAXSIZE = 100
    MAXCOUNT = Counter(wordlist).most_common()[0][1]
    MINCOUNT = Counter(wordlist).most_common()[-1][1]

    def calc_size (count):
        denominator = MAXCOUNT - MINCOUNT
        if(denominator == 0): denominator = 1
        wordsize = MAXSIZE * ((count - MINCOUNT)/denominator)
        return math.log(math.e+wordsize)

    counted_wordlist = Counter(wordlist).most_common()
    sized_wordlist = [(x[0], calc_size(x[1])) for x in counted_wordlist]

    #----------------------------------------------------------------------------------------#

    im = Image.new('L', (1024, 1024))

    def check_box(point, size, image):
        box = (point.x, point.y, point.x + size[0], point.y + size[1])
        crop = im.crop(box)
        stats = ImageStat.Stat(crop)
        alpha = stats.extrema[0]

        if (not(0 < point.x < im.size[0] - size[0])) or (not(0 < point.y < im.size[1] - size[1])):
            return False
        
        if (alpha[1] == 0):
            return True

        return False

    completed_words = 0
    angle_iterator = cycle([90, -90])

    for word in sized_wordlist:
        fnt = ImageFont.truetype("./fonts/Questrial-Regular.ttf", round(25*word[1]))
        im = im.rotate(next(angle_iterator))
        draw = ImageDraw.Draw(im)

        wordsize = draw.textsize(word[0], font=fnt)
        ranpos = (random.randrange(0, round(im.size[0]-wordsize[0])), random.randrange(0, round(im.size[1]-wordsize[1])))
        point = spiral.Point(ranpos[0], ranpos[1])

        while(True):
            t = time.time()
            if(check_box(point, wordsize, im.convert('L'))):
                draw.text((point.x, point.y), word[0], font=fnt, fill='white')
                completed_words += 1
                break
            else:
                point.inc(0.05)

            if(time.time() - t > 60):
                completed_words += 1
                break

        print(100*(completed_words/len(sized_wordlist)), '%')

    #im.show()
    return im

def process_text (text):
    _text = text.lower()
    ftext = re.sub('[",.?!\'0-9]', '', _text)
    return ftext.split()