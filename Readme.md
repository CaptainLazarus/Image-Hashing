# Image Hashing Notes

* Image hashing allows us to hash images so that we can find identical or similar images. 

* The reason that image hashing isn't the same as cryptographic hashing is that even a slight change in the latter gives a wildly different hash. Since we want similar images to have similar hashes, we use a different method called dhash.

* dhash steps
    1. Convert image to grayscale (can perform in color but its more intensive and hash is **3x** bigger)
    2. Reduce image dimensions (usually to 9x8)
    3. Do a difference equation (See the ocde. Will make more sense). Essentially, we want a 64 bit *difference* hash. So use a consistent operation. Doesn't matter what just, has to be consistent. 
    4. If **P[x] > P[x+1]**
        * 1
        * else 0

* dmap.py has 2 main functions you can call. 
    1. populate(list_of_paths , empty_dic)
        * Populates the dictionary with hashes of the images
    2. find(list_of_paths , dictionary)
        * Returns the list of images that are already present.