# import the necessary packages
from imutils import paths
import numpy as np
import argparse
import cv2
import os

"""
When I download images in batches, I get two versions of each image.
For example "img1__340.jpg" and "img1__480.jpg". The goal of this script
is to remove all similar images with the lower resolution. 

This is an example of the dictionary which we are going to create.
If an image has two paths which differ only in resoolution, keep only one 
of them
{
	img1: ['dataset/img1__340.jpg', 'dataset/img1__480.jpg'],
	img2: ['dataset/img2__340.jpg', 'dataset/img2__480.jpg',
	img3: ['dataset/img3__340.jpg'], 
}

"""


# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to input dataset")
ap.add_argument("-r", "--remove", type=int, default=-1,
	help="whether or not duplicates should be removed (i.e., dry run)")
args = vars(ap.parse_args())


# grab the paths to all images in our input dataset directory and
# then initialize our hashes dictionary
print("[INFO] Getting paths of all images...")
imagePaths = list(paths.list_images(args["dataset"]))
images = {}

# loop over our image paths
for imagePath in imagePaths:
	
	imageName = os.path.basename(imagePath)
	key = imageName[:-9]

	# grab the list of images' paths with that hash 
	p = images.get(key, [])

	# Add the current image path to that list
	p.append(imagePath)
	
	# store the list back in the images dictionary
	images[key] = p


print("Found images: " + str(len(imagePaths)))

#####################################################################
# Detect and remove duplicate images from a dataset for deep learning
#####################################################################

removed_images = 0

# loop over the image hashes
for (key, similarPaths) in images.items():

	print(str(key) + "<--->" + str(similarPaths))

	# check to see if there is more than one image with the same hash
	#if 0:
	if len(similarPaths) > 1:
		# check to see if this is a dry run
		if args["remove"] <= 0:
			# initialize a montage to store all images with the same
			# hash
			montage = None

			# loop over all image paths with the same hash
			for p in similarPaths:
				# load the input image and resize it to a fixed width
				# and heightG
				image = cv2.imread(p)
				image = cv2.resize(image, (150, 150))

				# if our montage is None, initialize it
				if montage is None:
					montage = image

				# otherwise, horizontally stack the images
				else:
					montage = np.hstack([montage, image])

			# show the montage for the hash
			cv2.imshow("Montage", montage)
			cv2.waitKey(0)

        # otherwise, we'll be removing the duplicate images
		else:
			# loop over all image paths with the same hash *except*
			# for the first image in the list (since we want to keep
			# one, and only one, of the duplicate images)
			
			for p in similarPaths[:1]:
				os.remove(p)
				removed_images = removed_images + 1
			
print("Removed images: " + str(removed_images))