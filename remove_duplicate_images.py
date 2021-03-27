# import the necessary packages
from imutils import paths
import numpy as np
import argparse
import cv2
import os

"""
The code is downloaded from
https://www.pyimagesearch.com/2020/04/20/detect-and-remove-duplicate-images-from-a-dataset-for-deep-learning/

This is an example of the dictionary which we are going to create.
The key of each item is the has of an image, and the value is a list
which contains all paths of the images with the same hash
{
	7054210665732718398: ['dataset/00000005.jpg', 'dataset/00000071.jpg', 'dataset/00000869.jpg'],
	8687501631902372966: ['dataset/00000011.jpg'],
	1321903443018050217: ['dataset/00000777.jpg'],
}

"""

def dhash(image, hashSize=4):
	# convert the image to grayscale and resize the grayscale image,
	# adding a single column (width) so we can compute the horizontal
	# gradient
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	resized = cv2.resize(gray, (hashSize + 1, hashSize))

	# compute the (relative) horizontal gradient between adjacent
	# column pixels
	diff = resized[:, 1:] > resized[:, :-1]

	# convert the difference image to a hash and return it
	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to input dataset")
ap.add_argument("-r", "--remove", type=int, default=-1,
	help="whether or not duplicates should be removed (i.e., dry run)")
args = vars(ap.parse_args())


# grab the paths to all images in our input dataset directory and
# then initialize our hashes dictionary
print("[INFO] computing image hashes...")
imagePaths = list(paths.list_images(args["dataset"]))
hashes = {}

# loop over our image paths
for imagePath in imagePaths:
	# load the input image and compute the hash
	image = cv2.imread(imagePath)
	h = dhash(image)
	
	# grab the list of images' paths with that hash 
	p = hashes.get(h, [])

	# Add the current image path to that list
	p.append(imagePath)
	
	# store the list back in the hashes dictionary
	hashes[h] = p


print("Found images: " + str(len(imagePaths)))

#####################################################################
# Detect and remove duplicate images from a dataset for deep learning
#####################################################################

# loop over the image hashes
for (h, hashedPaths) in hashes.items():

	print(str(h) + "<--->" + str(hashedPaths))

	# check to see if there is more than one image with the same hash
	#if 0:
	if len(hashedPaths) > 1:
		# check to see if this is a dry run
		if args["remove"] <= 0:
			# initialize a montage to store all images with the same
			# hash
			montage = None

			# loop over all image paths with the same hash
			for p in hashedPaths:
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
			print("[INFO] hash: {}".format(h))
			cv2.imshow("Montage", montage)
			cv2.waitKey(0)

        # otherwise, we'll be removing the duplicate images
		else:
			# loop over all image paths with the same hash *except*
			# for the first image in the list (since we want to keep
			# one, and only one, of the duplicate images)
			removed_images = 0
			for p in hashedPaths[1:]:
				os.remove(p)
				removed_images = removed_images + 1
			
			print("Removed images: " + str(removed_images))