# Python 3
from PIL import Image, ImageFilter
from pathlib import Path
import sys

# couldn't figure out how to convert terminal input into the PIL... image type that is 'zophie.png'
# Build another function that does this conversion btwn types? how? a special method to convert?
# Update: problem was because treatment_choice was a str and not referring to the functions _1 _2 and _3.

# User guide: trigger program as usual and provide your selected image file. 
# Note: make sure your image file is in the same location as Hw_FiltImage.py


def get_path(): 
    if len(sys.argv) < 2: # if the terminal user input is less than two words...
        print('How to Use: [Hw_FiltImage.py] [existingfile.png]')
        sys.exit()


    path = ' '.join(sys.argv[1:]) 

    path = Path(path)

    ''' 
    cwd = pathlib.Path().absolute()
    # now we construct the full path
    path = cwd + str(os.path.sep) + user_png
    # .getcwd()
    >>>> didn't need to go through all this
    '''
    #return path, user_png 
    return path

def filter_selection_hub(user_choice,copied_image):

    if user_choice == "1":

        product = treatment_1(copied_image)

    elif user_choice == "2":

        product = treatment_2(copied_image)

    elif user_choice == "3":

        product = treatment_3(copied_image)
    
    else:

        print('Input was invalid.')
        product = None
    
    return product



# Open an Image given a path 'zophie.png'
def open_image(path):
    newImage = Image.open(path)
    #original.close()
    return newImage


# create an empty canvas (this will be where our final product is displayed)
def create_image(i,j):
    image = Image.new("RGB", (i,j), "white")
    return image


# 1st Filter
# applies the sharpen and emboss filter, and rotates the image
def treatment_1(newImage):

    filtering = newImage.rotate(180)
    filtering = filtering.filter(ImageFilter.SHARPEN)
    product = filtering.filter(ImageFilter.EMBOSS)

    return product

# 2nd Filter
# sharpens the image & applies sephia filter
def treatment_2(newImage):
    
    sephia = convert_sephia(newImage) # calls upon funct that converts to sephia
    product = sephia.filter(ImageFilter.SHARPEN)

    return product

# 3rd Filter
# takes the image, minimizes its dimensions and copy/pastes them over the white canvas that we created in earlier function. (then rotate at end)
def treatment_3(newImage):

    width, height = newImage.size # saves width and height of user given image

    new = create_image(width,height) # saved a blank white canvas image
    
    resized = newImage.resize((int(width/18), int(height/18)))

    width, height = new.size
    width1, height1 = resized.size


    for left in range(0, width, width1):
            
        for top in range(0, height, height1):

            new.paste(resized,(left,top))

    new = new.rotate(180)

    return new #which is newImage
    
# making sure we stay within the rgb value range
def get_max(value):

    if value > 255:
        return 255

    return int(value)

# takes the pixels of our image that we are filtering
def get_pixel(image,i,j):
    # Work within bounds of image
    width, height = image.size
    if i > width or j > height:
        # if you want me to return the width of i ... or if you want me to return the height of j...
        return None
    pixel = image.getpixel( (i,j) )
    return pixel

# uses get_max
# taking the image pixels and recoloring them by selected values
def get_sepia_pixel(red, green, blue, alpha):
    # filter type
    value = 0
    # This is a really popular implementation
    tRed = get_max((0.759 * red) + (0.398 * green) + (0.194 * blue))
    tGreen = get_max((0.676 * red) + (0.354 * green) + (0.173 * blue))
    tBlue = get_max((0.524 * red) + (0.277 * green) + (0.136 * blue))

    if value == 1:
        tRed = get_max((0.759 * red) + (0.398 * green) + (0.194 * blue))
        tGreen = get_max((0.524 * red) + (0.277 * green) + (0.136 * blue))
        tBlue = get_max((0.676 * red) + (0.354 * green) + (0.173 * blue))
    
    if value == 2:
        tRed = get_max((0.676 * red) + (0.354 * green) + (0.173 * blue))
        tGreen = get_max((0.524 * red) + (0.277 * green) + (0.136 * blue))
        tBlue = get_max((0.524 * red) + (0.277 * green) + (0.136 * blue))

    return tRed, tGreen, tBlue, alpha

# converting pixels filter, to become sephia
# implements previous three functions
def convert_sephia(image):
    # Get the size
    width, height = image.size

    # Create a new image & get it read for manipulation
    new = create_image(width,height) # one of our premade functions
    pixels = new.load() # Basically grabs/saves an array of the rgb values for those pixels that make it up
    #aka an empty Pixel Map yet to be filled in


    # Convert
    for i in range(0, width, 1):
        for j in range(0, height, 1):
            p = get_pixel(image,i,j) # example) go to coordinate 0,0 : fetch the pixel there : save it for me
            # Take pixels from original image and put it in empty pixel map after sepia filter

            pixels[i,j] = get_sepia_pixel( p[0] , p[1] , p[2] , 255 )
            # in this line above, we take the original pixels, process it through filter, and save it
            # p[#] means the 

    # Return the new image
    return new





# Save Image (the final product after treating)
# originally the empty canvas
def save_image(image,path):
    image.save(path,'png') #appends png to the path




def main():
    
    path = get_path()
    
    #print(path)
    #original = open_image(path)

    original = open_image(path)

    copied_image = original.copy()
    
    msg4user = ''' Please make a filter selection by typing one of these numbers: 1 , 2 , 3 \n Your Selection: '''

    user_choice = input(msg4user)

    product = filter_selection_hub(user_choice, copied_image)

    '''
    print(type(open_image('zophie.png')))
    print(type(user_choice))
    print(type(copied_image))
    '''

    #treatment_choice = 'treatment_%s' %(user_choice)
    
    
    if product == None:
        quit

    else:
        save_image(product , 'Filtered_Image.png')
    

    
    


main()

