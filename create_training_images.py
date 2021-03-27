from os import walk, path, rename, mkdir
from shutil import move, rmtree, copy2
from PIL import Image 
from random import randint
from time import sleep

"""
The goal of this script is to create training data from banknote images.
Each banknote will be input multiple times with some variations such as
lighting, paper condition, and folded parts, etc . 

Then each input image will be merged into a backgorund so that it looks
like the banknote image was captured in many different locations.   
"""


def sliceVertical(imagePath, percentage, outPath="imgs_tmp"):
    """
    Slices an input image vertically to a number of pieces. Each piece
    will have the same percenatge of the width of the image. For example
    if the percentage is 0.5, the image will be sliced vertically into
    two pieces and each piece is half the width of the original image 

    @param image: the image handle returned from Image.Open()
    @param percentage: the image will be sliced into pieces, the width
        of each piece = (image width * percentage).
    @param outPath: The path to generate the sliced images 
    """

    # Opens the image in RGB mode 
    image = Image.open(imagePath)
    imageName = getNameWithoutExtension(imagePath)

    # Size of the image in pixels (size of orginal image)
    width, height = image.size

    left = 0
    right = width * percentage
    slicedImagesCount = int(1/percentage + 1)
    for i in range(1, slicedImagesCount):

        # Crop the input image (left, top, right, bottom)  
        im1 = image.crop((left, 0, right, height)) 

        # increment the crop margins
        left = left + width * percentage
        right = right + width * percentage
        
        # Save the image
        im1.save("{}/{}_v-{}-{}.jpg".format(outPath, imageName, percentage, i))


def sliceHorizontal(imagePath, percentage, outPath="imgs_tmp"):
    """
    Slices an input image horizontally to a number of pieces. Each piece
    will have the same percenatge of the height of the image. For example
    if the percentage is 0.5, the image will be sliced horizontally into
    two pieces and each piece is half the height of the original image 

    @param: the image handle returned from Image.Open()
    @percentage: the image will be sliced into pieces, the height of
        each piece = (image height * percentage).  
    """

    # Opens the image in RGB mode 
    image = Image.open(imagePath)
    imageName = getNameWithoutExtension(imagePath)

    # Size of the image in pixels (size of orginal image)
    width, height = image.size

    top = 0
    bottom = height * percentage
    slicedImagesCount = int(1/percentage + 1)
    for i in range(1, slicedImagesCount):

        # Crop the input image (left, top, right, bottom)  
        im1 = image.crop((0, top, width, bottom)) 

        # increment the crop margins
        top = top + height * percentage
        bottom = bottom + height * percentage
        
        # Save the image
        im1.save("{}/{}_h-{}-{}.jpg".format(outPath, imageName, percentage, i))

def sliceFromCenter(imagePath, outPath="imgs_tmp"):
    """
    Slice the input image into 4 quarters around its center pixel
    """

    # Opens the image in RGB mode 
    image = Image.open(imagePath)
    imageName = getNameWithoutExtension(imagePath)

    # Size of the image in pixels (size of orginal image)
    width, height = image.size

    # Top left quarter
    im1 = image.crop((0, 0, width / 2, height / 2)) 
    im1.save("{}/{}_c-0.25-1.jpg".format(outPath, imageName))

    # Top right quarter
    im1 = image.crop((width / 2, 0, width, height / 2)) 
    im1.save("{}/{}_c-0.25-2.jpg".format(outPath, imageName))

    # bottom left quarter
    im1 = image.crop((0, height / 2, width / 2, height)) 
    im1.save("{}/{}_c-0.25-3.jpg".format(outPath, imageName))

    # bottom right quarter
    im1 = image.crop((width / 2, height / 2, width, height)) 
    im1.save("{}/{}_c-0.25-4.jpg".format(outPath, imageName))

def addHoldingHnad(imagePath1, imagePath2, outPath="imgs_tmp"):
    """
    """
    #foreground = Image.open(imagePath1)
    #background = Image.open(imagePath2)

    layer1 = Image.open(imagePath1)
    layer1 = layer1.convert("RGBA")
    
    blended = Image.new("RGBA", layer1.size)
    blended = Image.alpha_composite(blended, layer1)
    
    layer2 = Image.open(imagePath2)
    layer2 = layer2.resize(blended.size)
    layer2 = layer2.convert("RGBA")

    blended = Image.alpha_composite(blended, layer2)
    
    # Save the image with a name combinig both images names
    imageName1 = getNameWithoutExtension(imagePath1)
    imageName2 = getNameWithoutExtension(imagePath2)
    blended = blended.convert("RGB")
    blended.save("{}/{}_{}.jpg".format(outPath, imageName1, imageName2))


def addBackground(backgroundPath, foregroundPath, scale=1, shift=(0,0), angle=0, outPath="imgs_tmp"):
    """
    Takes a background image and a foreground image add merge them.
    The foreground image can be scaled and be rotated. It can also 
    be put at an aribttatry location (x,y). 
    """
    
    img1 = Image.open(backgroundPath).convert('RGBA')
    img2 = Image.open(foregroundPath).convert('RGBA')
    
    w = int(img2.width * scale)
    h = int(img2.height * scale)
    img2 = img2.resize((w, h))

    img2 = img2.rotate(angle, expand=True)

    # paste img1 on top of img2
    shift1 = (0, 0)
    shift2 = shift
    blended = Image.new('RGBA', size=(512, 512), color=(0, 0, 0, 0))
    blended.paste(img1, shift1)
    blended.paste(img2, shift2, img2)

    # Save the image with a name combinig both images names
    imageName1 = getNameWithoutExtension(backgroundPath)
    imageName2 = getNameWithoutExtension(foregroundPath)
    blended = blended.convert("RGB")
    blended.save("{}/{}_{}.jpg".format(outPath, imageName2, imageName1))


def addBackgroundTransparent(backgroundPath, foregroundPath, scale=1, shift=(0,0), angle=0, outPath="imgs_tmp"):
    """
    Takes a background image and a foreground image add merge them.
    The foreground image can be scaled and be rotated. It can also 
    be put at an aribttatry location (x,y). 
    """
    
    layer1 = Image.open(backgroundPath)
    layer1 = layer1.convert("RGBA")
    
    blended = Image.new("RGBA", layer1.size)
    blended = Image.alpha_composite(blended, layer1)
    
    layer2 = Image.open(foregroundPath)
    w = int(layer2.width * scale)
    h = int(layer2.height * scale)
    layer2 = layer2.resize((w, h))
    layer2 = layer2.rotate(angle, expand=True)
#    layer2 = layer2.resize(blended.size)
    layer2 = layer2.convert("RGBA")

    # paste layer2 on top of layer1
    shift1 = (0, 0)
    shift2 = shift
    blended = Image.new('RGBA', size=(512, 512), color=(0, 0, 0, 0))
    blended.paste(layer1, shift1)
    blended.paste(layer2, shift2, layer2)

    # Save the image with a name combinig both images names
    imageName1 = getNameWithoutExtension(backgroundPath)
    imageName2 = getNameWithoutExtension(foregroundPath)
    blended = blended.convert("RGB")
    blended.save("{}/{}_{}.jpg".format(outPath, imageName2, imageName1))


def getImages(searchDir):
    """
    Returns a list with the paths of all images found in the given path
    """

    imagesPaths = []

    for root, directories, files in walk(searchDir):
        for file in files:
           if ('.jpg' in file) or ('.png' in file):
                imagesPaths.append(path.join(root, file))
    
    print("Found images in '{}' = {}".format(searchDir, len(imagesPaths)))
    return imagesPaths

def categorizeClasses(searchDir, outputDir):
    """
    Organize the training folder such that each class has exactly
    one folder, e.g. five egyptian pound "eg_00005", fifty saudi
    rial "sa_00050"
    """

    imagesPaths = getImages(searchDir)
    
    classCount = 0
    classNames = []
    for image in imagesPaths:
        imageName = getNameWithoutExtension(image)
        if imageName[0:8] not in classNames:
            classNames.append(imageName[0:8])
            classCount = classCount + 1

    # Create a directory for each class
    print("Found classes in {} = {}".format(searchDir, classCount))
    for className in classNames:
        mkdir(path.join(outputDir, className))

    # Move each image to its corresponding class folder
    for imagePath in imagesPaths:
        imageName = getNameWithoutExtension(imagePath)
        className = imageName[0:8]
        move(imagePath, path.join(outputDir,className))


def getNameWithoutExtension(imagePath):
        name = path.basename(imagePath)
        return path.splitext(name)[0]


def renameAllImages(searchDir):
    """
    For debug only: This function can be used to rename all files
    whenever a new name scheme  is needed
    """

    for root, directories, files in walk(searchDir):
        for file in files:
            if ('.jpg' in file) or ('.png' in file):
                # here you can enter the new name scheme
                newName = file[0:3]+file[5:-4]+file[2:4]+file[-4:]
                rename(path.join(root, file), path.join(root, newName) )


def cleanOutputDirectories(directories):
    """
    Delete all images in the output directories
    """

    print("Deleting all previously generated directories")
    for directory in directories:
        if path.exists(directory):
            rmtree(directory)

    # it takes a while to delete all directories    
    sleep(3)

    for directory in directories:
        mkdir(directory)


##############################################################################
###                         The Main Program                               ###
##############################################################################
if __name__ == "__main__":
    
    
    TRAIN_DIR_IN = "images/banknotes_in_resized/train/train_eg"
    TRAIN_DIR_OUT = "images/imgs_out/train/"
    TRAIN_DIR_TEMP = "images/imgs_tmp/train"
    VALIDATION_DIR_IN = "images/imgs_in/validation"
    VALIDATION_DIR_OUT = "images/imgs_out/validation"
    VALIDATION_DIR_TEMP = "images/imgs_tmp/validation"
    BACKGROUNDS_DIR = "images/backgrounds"
    
    # Delete all previously generated images
    cleanOutputDirectories([
        TRAIN_DIR_OUT, TRAIN_DIR_TEMP,
        VALIDATION_DIR_OUT, VALIDATION_DIR_TEMP
        ])

    # Get a list of all bankonte images within the specified path
    imagesPaths = getImages(TRAIN_DIR_IN)

    # Get a list of all backgrounds images within the specified path
    backgroundPaths = getImages(BACKGROUNDS_DIR)

    background_index = 1 
    for imagePath in imagesPaths:

        print("Working on {}".format(path.basename(imagePath)))
        
        for i in range(300):
            # Add the selected banknote image to many backgrounds        
            background = backgroundPaths[background_index]
            x = randint(0, 100)
            y = randint(0, 100)
            theta = randint(0, 270)
            addBackgroundTransparent(background, imagePath, scale=0.9, shift=(x,y), angle=theta, outPath=TRAIN_DIR_TEMP)

            background_index = background_index + 1


    # Group the images of one class into 1 folder
    categorizeClasses(TRAIN_DIR_TEMP, TRAIN_DIR_OUT)
