import argparse
import time
import cv2
import os
import sys
from imutils import paths

def initArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a" , "--haystack" , required=True , help="Directory of images to search through")
    parser.add_argument("-n" , "--needles" , required=True , help="Images to search for")
    args = vars(parser.parse_args())
    return args

def dhash(image , hashsize = 8):
    resized = cv2.resize(image , (hashsize+1 , hashsize))
    diff = resized[: , 1:] > resized[: , :-1]
    return sum([2 ** i for (i,v) in enumerate(diff.flatten()) if v])

def populate(hpaths , haystack):
    start = time.time()
    for p in hpaths:
        img = cv2.imread(p)

        if img is None:
            continue

        img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
        imghash = dhash(img)

        l = haystack.get(imghash , [])
        l.append(p)
        haystack[imghash] = l
    print("[INFO] Processed {} images in {:.2f} secs".format(len(haystack) , time.time()-start))

def find(npaths , haystack):
    for p in npaths:
        image = cv2.imread(p)
        if image is None:
            continue

        image = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
        imagehash = dhash(image)
        matches = haystack.get(imagehash , [])
        return matches


if __name__ == "__main__":

    args = initArgs()

    print("[INFO] Computing hashes")
    hpaths = list(paths.list_images(args["haystack"]))
    npaths = list(paths.list_images(args["needles"]))

    if sys.platform != "win32":
        hpaths = [p.replace("\\" , "") for p in hpaths]
        npaths = [p.replace("\\" , "") for p in npaths]

    haystack = {}

    populate(hpaths , haystack)
    matches = find(npaths , haystack)

    for match in matches:
            os.remove(match)

            print("Removed: {}".format(match))