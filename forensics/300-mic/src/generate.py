from PIL import Image, ImageDraw, ImageFont
import random, numpy, sys, math

# define variables here
flag = 'BSidesPDX{d0t}' # max 16 bytes
number_of_papers = 100

matrix_size = (8, 15) # was 15
matrix_ratio = 2.5

dot_diameter = 1 / 250

date = (18, 9, 22) # y / m / d
time = (18, 30)
serial = (13, 37, random.randint(0, 64), random.randint(0, 64))
unknown = 108

# size definition variables
paper_width = 8.5 # inches
paper_height = 11.0 # inches
paper_margins = 0.5 # inches

# open the paper image
default_paper_image = Image.open('paper.png')
default_paper = numpy.asarray(default_paper_image)

# 1024 random samples of color from the paper
choices = [tuple(random.choice(random.choice(default_paper))) for x in range(1024)]

# returns an automatically generated image of a paper
def getPaper():
    # create the default image
    size_x, size_y = (int(paper_width / dot_diameter / matrix_ratio), int(paper_height / dot_diameter / matrix_ratio)) # img.size
    img = Image.new("RGB", (size_x, size_y))

    # get an array of pixels
    pixels = img.load()

    # randomize all of the pixels using the `choices` array from earlier
    for x in range(size_x):
        for y in range(size_y):
            pixels[x, y] = random.choice(choices)

        # write a pretty status message to console
        percentage = x / size_x
        length = 40
        sys.stdout.write('\r[%s>%s] %s%s' % ('=' * round(percentage * length), ' ' * (length - round(percentage * length)), round(x / size_x * 100), '%'))
        sys.stdout.flush()

    # draw 5 random lines (red herring)
    draw = ImageDraw.Draw(img)
    for i in range(5):
        draw.line((random.choice(range(size_x)), random.choice(range(size_y)), random.choice(range(size_x)), random.choice(range(size_y))), fill = 128)

    # draw heading
    draw.text((10, 10), "BSidesPDX CTF - 2018", font = ImageFont.truetype("arial.ttf"), fill = (0, 0, 0))

    # write a newline after status message
    sys.stdout.write('\n')
    sys.stdout.flush()

    return img

# create dot matrix
matrix_height, matrix_width = matrix_size
matrix = []

# fills in the column at `index` with `array`
def fillHeight(index, array):
    for i in range(len(array)):
        matrix[i + 1][index + 1] = (True if array[i] == '1' else False) # 1 offset because of parity bit

# converts an int to an array of strings of binary digits
def toBinary(number, zfill = 7):
    return list(str(bin(number))[2:].zfill(zfill))

# creates an empty matrix
def resetMatrix():
    for y in range(matrix_height):
        matrix.append([False for x in range(matrix_width)])

# adds parity to a matrix
def calculateParity():
    # row parity
    for row in matrix:
        if row.count(True) % 2 == 0:
            row[0] = True

    # column parity
    for x in range(1, matrix_width):
        bit = True

        for y in range(matrix_height):
            if matrix[y][x]:
                bit = not bit

        if bit:
            matrix[0][x] = True


    # [0, 0] parity
    matrix[0][0] = True

# fill matrix with default data
def getDefaultMatrix():
    resetMatrix()

    fillHeight(0, toBinary(time[1])) # col 2: time in seconds
    fillHeight(3, toBinary(time[0])) # col 5: time in hours

    fillHeight(4, toBinary(date[2])) # col 6: date in days
    fillHeight(5, toBinary(date[1])) # col 7: date in months
    fillHeight(6, toBinary(date[0])) # col 8: date in years

    fillHeight(8, list('1' * 7)) # col 10: separator

    fillHeight(9, toBinary(serial[3])) # col 11: serial digit group
    fillHeight(10, toBinary(serial[2])) # col 12: serial digit group
    fillHeight(11, toBinary(serial[1])) # col 13: serial digit group
    fillHeight(12, toBinary(serial[0])) # col 14: serial digit group

    fillHeight(13, toBinary(unknown)) # col 15: unknown

    calculateParity()

    return matrix

# fill matrix with flag data
def getFlagMatrix():
    resetMatrix()

    # convert flag to an array of ints (ascii)
    binary_flag = [ord(x) for x in list(flag)]

    # fill out matrix
    for i in range(len(binary_flag)):
        fillHeight(i, toBinary(binary_flag[i]))

    calculateParity()

    return matrix

# print out matrix
def printMatrix(matrix):
    print('\n'.join([''.join([('X' if b else ' ') for b in a]) for a in matrix]))

# choose a paper to embed flag in
flag_paper = random.randint(0, number_of_papers - 1)

# add a little hint
with open('.hint', 'w') as f:
    f.write('- ignore the lines on the images\n- if you are completely lost: what was the title of the challenge again?')

# generate all papers
for i in range(number_of_papers):
    serial = (13, 37, random.randint(0, 64), random.randint(0, 64))

    # generate dot matrix
    type = 'dummy'
    if flag_paper == i:
        type = 'flag'
        matrix = getFlagMatrix()
    else:
        matrix = getDefaultMatrix()

    # print status info
    print('Generating %s paper (%s/%s)...' % (type, i + 1, number_of_papers))

    # create a new randomized paper image
    paper = getPaper()
    pixels = paper.load()

    # size definition variables
    image_width, image_height = paper.size # pixels

    # useful unit conversion functions
    toInches = lambda pixels : paper_width / image_width * pixels
    toPixels = lambda inches : image_width / paper_width * inches

    # define yellow dot size and position variables in pixels
    yellow_dot_diameter = toPixels(dot_diameter) # pixels
    yellow_dot_spacing = int(toPixels(3 / 64)) # pixels
    yellow_dot_padding = toPixels(1 / 2) # pixels

    # matrix dimensions
    dot_matrix_size = (matrix_size[1] * (yellow_dot_diameter + yellow_dot_spacing) + yellow_dot_padding, matrix_size[0] * (yellow_dot_diameter + yellow_dot_spacing) + yellow_dot_padding)

    # add yellow dots
    for x in range(math.floor((toPixels(paper_width) - (1 * toPixels(paper_margins))) / dot_matrix_size[0])):
        for y in range(math.floor((toPixels(paper_height) - (1 * toPixels(paper_margins))) / dot_matrix_size[1])):
            # define upper left corner of the dot matrix
            position = ((x * dot_matrix_size[0]) + toPixels(paper_margins), (y * dot_matrix_size[1]) + toPixels(paper_margins))

            # set positions
            for row in range(matrix_width):
                for col in range(matrix_height):
                    if matrix[col][row]:
                        pixels[round(position[0] + (yellow_dot_spacing * row)), round(position[1] + (yellow_dot_spacing * col))] = (0xFF, 0xFF, random.randint(0x77, 0x88))

    paper.save('scan%s.png' % i)

    # extra newline
    print()
