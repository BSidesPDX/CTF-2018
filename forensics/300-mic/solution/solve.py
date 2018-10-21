from PIL import Image, ImageDraw, ImageFont
import numpy

def decodePaper(file, path = '../distFiles/'):
    # load in the file and get its pixels as a 2d array
    paper_image = Image.open(path + file)
    paper = numpy.asarray(paper_image)

    color_threshold = 0x88
    corner = (50, 50) # upper left corner of any matrix
    matrix_size = (15, 8)
    matrix_spacing = 4

    # skip the first row / column since it is just parity
    text = ''
    for column in range(1, matrix_size[0]):
        # sum up the bits for the column
        sum = 0
        for row in range(1, matrix_size[1]):
            # get the pixel at the given location
            pixel = paper[corner[1] + (row * matrix_spacing), corner[0] + (column * matrix_spacing)]

            # if the blue portion of the rgb color for the pixel in the row being tested is less than the threshold, and the other two octets are 0xFF, then the pixel is part of the mic
            if pixel[0] == 0xFF and pixel[1] == 0xFF and pixel[2] <= color_threshold:
                sum += 2 ** (matrix_size[1] - row - 1)

        text += chr(sum)

    return text

number_of_papers = 100

for paper_index in range(number_of_papers):
    decoded = decodePaper('scan%s.png' % paper_index, '../src/workspace/')

    if 'BSidesPDX' in decoded:
        print('Found flag (scan%s.png): %s' % (paper_index, decoded))
        exit()

print('Failed to find flag.')
