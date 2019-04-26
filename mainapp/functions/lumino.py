from luminoth import Detector, read_image, vis_objects
detector = Detector(checkpoint='b9bdfe47f743')


def predict_anchor(image_path="/Users/balajidr/Developer/fyp_final/mainapp/functions/RCNN/testimages/slide-Table.jpg"):
    image = read_image(image_path)

    # If no checkpoint specified, will assume `accurate` by default. In this case,
    # we want to use our traffic checkpoint. The Detector can also take a config
    # object.
    # Returns a dictionary with the detections.
    objects = detector.predict(image)
    print(objects)
    vis_objects(image, objects).save('traffic-out.png')
    return objects
