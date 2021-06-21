import pathlib
import struct
import shutil
import os
from tqdm import tqdm


from PIL import Image, ImageEnhance, ImageStat

def brightness( im_file, isObject = False ):

    if isObject:
        im = im_file.convert('L')
    else:
        im = Image.open(im_file).convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]


## Helpers

def isNight(filename):
    return (22 <= int(filename[8:10]) or int(filename[8:10]) <= 7)

def isJunk(filename):
    return int(filename[:10]) < 2021052819


#Business logic

def getPhotoNames():
    files=[]
    for path in (pathlib.Path("photos").iterdir()):
        photoPath = "photos/" + path.stem + ".jpg"
        if path.is_file():
            if isNight(path.stem):
                continue
            if isJunk(path.stem):
                continue
            files.append(path.stem)


    return files


def renamePhotos(files):
    basePath = "./sequence"
    if not os.path.isdir(basePath):
        os.mkdir(basePath)
    idx = 0

    for file in tqdm(files):
        photoPath = "./sequence/"+str(idx).zfill(4)+".jpg"
        shutil.copy("./photos/"+file+".jpg", photoPath)

        idx +=1

def imageManipulation(files):
    basePath = "./sequence"
    idx = 0

    for file in tqdm(files):
        photoPath = "./sequence/"+str(idx).zfill(4)+".jpg"

        b = brightness(photoPath)
        c = 0
        img = Image.open(photoPath)
        while ((b < 112) or (114 < b)):
            filter = ImageEnhance.Brightness(img)
            if b < 112:
                img = filter.enhance(1.01)
            else:
                img = filter.enhance(0.99)
            b = brightness(img, True)
            c+=1
            if 10 < c:
                break

        img.save(photoPath)
        b2 = brightness(photoPath)
        #print(str(b) + " : " + str(b2) + " : " + path.stem)

        idx +=1


def main():

    print("Filter bad photos based on time")
    files = getPhotoNames()
    files.sort()
    print("Number of photos: " + str(len(files)))
    print("Rename photos to sequence")
    renamePhotos(files)
    print("Apply image equalizer")
    imageManipulation(files)
    os.system("ffmpeg -pattern_type glob -i './sequence/*.jpg' -y ./video.mp4")


    print("Done")

main()
