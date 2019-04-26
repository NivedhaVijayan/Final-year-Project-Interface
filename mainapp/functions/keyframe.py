# USAGE
# python main.py -v video_file -t threshold_value
# import the necessary packages
from shutil import copy2, copyfile
from scipy.spatial import distance as dist
# import matplotlib
from progress.bar import Bar
import redis
import os
import cv2
import argparse
import re
import pickle
import imutils
# matplotlib.use('pdf')
from fyp_final.settings import MEDIA_ROOT, BASE_DIR
r = redis.Redis(host='localhost', port=6379, db=0)
model1 = pickle.loads(r.get("model1"))
model2 = pickle.loads(r.get("model2"))
from mainapp.functions import ocr
from mainapp.models import Frame, Video


def extract_all_frames(video_path: str) -> str:
    vidcap = cv2.VideoCapture(video_path)
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    success, image = vidcap.read()
    if success:
        print(" ---> Video has been successfully detected.")
    else:
        print(" ---> Cannot find video in the given path.")
    count = 0
    i = 1
    if not os.path.exists(MEDIA_ROOT+"/SlideExtraction/frames"):
        os.makedirs(MEDIA_ROOT+"/SlideExtraction/frames")
    print(" ---> Created directory to store all the frames.")
    print(" ---> Extracting all the frames from the video.")
    max_frames = (int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))/fps) + 1
    extraction_bar = Bar('Extracting', max=int(max_frames))
    while success:
        if count % 30 == 0:
            timestamp = vidcap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            cv2.imwrite(MEDIA_ROOT + '/SlideExtraction/frames/' + 'frame%d.jpg' % int(timestamp), image)
            # print('Extracted Frame no %d of Time %d ' % (count, timestamp))
            i += 1
            extraction_bar.next()
        success, image = vidcap.read()
        count += 1
    extraction_bar.finish()
    return MEDIA_ROOT+'/SlideExtraction/frames'


def image_to_feature_vector(image, size=(32, 32)):
    return cv2.resize(image, size).flatten()


def extract_color_histogram(image, bins=(8, 8, 8)):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256])

    if imutils.is_cv2():
        hist = cv2.normalize(hist)
    else:
        cv2.normalize(hist, hist)
    return hist.flatten()


def getfiles(dirpath="/Users/balajidr/Developer/FYP_TEMP/SlideExtraction/frames"):
    a = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    b = [dirpath+"/"+x for x in a]
    return b


def predict(imgpath):
    image = cv2.imread(imgpath)
    # change to histogram as feature if needed
    histogram = extract_color_histogram(image)
    prediction = model2.predict([histogram])
    # pixels = image_to_feature_vector(image)
    # prediction = model1.predict([pixels])
    print(" === Predicted keyframe is -> ", str(prediction[0]).upper())
    return str(prediction[0]).upper()


def start_function(video_path, threshold=0.5):

    print(" ---> Path of the video is %s" % video_path)
    if threshold:
        print(" ---> Given threshold value is %f" % threshold)
    else:
        # print(" ---> No threshold value was provided. Taking the pre-calculated threshold value.")
        threshold = 0.5

    frame_directory = extract_all_frames(video_path=video_path)
    print(" ---> Successfully extracted all the frames from the given video.")
    index = {}
    images = {}
    name_and_hist = []
    all_frames = getfiles(dirpath=frame_directory)

    print(" ---> Extracted frames are being processed to find keyframes.")
    processing_bar = Bar('Processing frames', max=len(all_frames))
    for imagePath in all_frames:
        temp = dict()
        filename = imagePath[imagePath.rfind("/") + 1:]
        image = cv2.imread(imagePath)
        images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()

        # adds img info to the temp dict and append to array
        temp["filename"] = filename
        temp["hist"] = hist
        name_and_hist.append(temp)

        # populate the index dixt
        index[filename] = hist
        processing_bar.next()
    processing_bar.finish()


    SCIPY_METHODS = (
        ("Euclidean", dist.euclidean),
        ("Manhattan", dist.cityblock),
        ("Chebysev", dist.chebyshev))

    print(" ---> Applying Euclidean method to find the distance between two frames.")

    # # loop over the comparison methods
    for (methodName, method) in SCIPY_METHODS:
        results = list()
        distance_bar = Bar('Applying Euclidean distance', max=len(name_and_hist))
        for i, img_info in enumerate(name_and_hist):
            if i == 0:
                temp = {}
                # print("comparing", name_and_hist[0].get("filename"), name_and_hist[0].get("filename"))
                d = method(name_and_hist[0].get("hist"), name_and_hist[0].get("hist"))
                temp["filename1"] = name_and_hist[i].get("filename")
                temp["filename2"] = name_and_hist[i].get("filename")
                # temp["hist"] = name_and_hist[i].get("hist")
                temp["distance"] = d
                results.append(temp)
                distance_bar.next()
            if i > 0:
                temp = dict()
                # print("comparing", name_and_hist[i-1].get("filename"), name_and_hist[i].get("filename"))
                d = method(name_and_hist[i-1].get("hist"), name_and_hist[i].get("hist"))
                temp["filename1"] = name_and_hist[i-1].get("filename")
                temp["filename2"] = name_and_hist[i].get("filename")
                # temp["hist"] = name_and_hist[i].get("hist")
                temp["distance"] = d
                results.append(temp)
                distance_bar.next()
        distance_bar.finish()

        if not os.path.exists(MEDIA_ROOT + "/SlideExtraction/keyframes"):
            os.makedirs(MEDIA_ROOT + "/SlideExtraction/keyframes")
        print(" ---> Created intermediate directory to store all the keyframes.")

        if not os.path.exists(MEDIA_ROOT+"/SlideExtraction/output/Slides"):
            os.makedirs(MEDIA_ROOT+"/SlideExtraction/output/Slides")
        if not os.path.exists(MEDIA_ROOT + "/SlideExtraction/output/NonSlides"):
            os.makedirs(MEDIA_ROOT + "/SlideExtraction/output/NonSlides")
        print(" ---> Output directory created for storing Slide and NonSlide keyframes.")

        prediction_bar = Bar('Predicting keyframes', max=len(results))
        for each in results:
            # print("comparing %s with %s -> %0.10f" % (each["filename1"], each["filename2"], each["distance"]))
            if each["distance"] > threshold:
                copy2(frame_directory + "/" + each["filename2"], MEDIA_ROOT + "/SlideExtraction/keyframes")
                label = predict(imgpath=MEDIA_ROOT + "/SlideExtraction/keyframes/" + each["filename2"])
                if label == "SLIDE":
                    copyfile(src=MEDIA_ROOT + "/SlideExtraction/keyframes/" + each["filename2"],
                             dst=MEDIA_ROOT + "/SlideExtraction/output/Slides/" + each["filename2"])
                    f_number = int(re.search(r'\d+', each["filename2"]).group())
                    video = Video.objects.get(name=os.path.basename(os.path.normpath(video_path)))
                    content = ocr.extract_text(image_path=MEDIA_ROOT + "/SlideExtraction/output/Slides/" + each["filename2"])
                    f = Frame(name=each["filename2"], f_number=f_number, f_type="SLIDE", timestamp=f_number,
                              image=MEDIA_ROOT + "/SlideExtraction/output/Slides/" + each["filename2"],
                              video=video, content=content)
                    f.save()
                elif label == "NONSLIDE":
                    copyfile(src=MEDIA_ROOT + "/SlideExtraction/keyframes/" + each["filename2"],
                             dst=MEDIA_ROOT + "/SlideExtraction/output/NonSlides/" + each["filename2"])
                    f_number = int(re.search(r'\d+', each["filename2"]).group())
                    video = Video.objects.get(name=os.path.basename(os.path.normpath(video_path)))
                    f = Frame(name=each["filename2"], f_number=f_number, f_type="NON-SLIDE", timestamp=f_number,
                              image=MEDIA_ROOT + "/SlideExtraction/output/Slides/" + each["filename2"],
                              video=video)
                    f.save()
            prediction_bar.next()
        prediction_bar.finish()
        print(" ---> Script successfully executed.")

        break
