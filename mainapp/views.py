from django.shortcuts import render, redirect
from django.views.generic.base import View
from fyp_final.settings import MEDIA_ROOT, BASE_DIR
from mainapp.models import Video, Frame
from mainapp.functions import topic
from mainapp.functions import keyframe
from mainapp.functions import lumino
import shutil

class Index(View):

    @staticmethod
    def get(request):
        all_videos = Video.objects.all()
        videos = list()
        for each in all_videos:
            v_dict = {}
            v_dict["name"] = each.name
            v_dict["length"] = each.v_length
            v_dict["topic"] = each.topic
            v_dict["path"] = each.video
            v_dict["is_processed"] = each.is_processed
            videos.append(v_dict)
        return render(request=request, template_name="main.html", context={"videos": videos})


class UpdateVideo(View):

    @staticmethod
    def get(request):
        from os import listdir
        from os.path import isfile, join
        files = [f for f in listdir(MEDIA_ROOT + "/videos") if isfile(join(MEDIA_ROOT + "/videos", f))]
        for each in files:
            if each.endswith(".mp4") and each not in [x.name for x in Video.objects.all()]:
                v = Video(name=each, video="/videos/" + each)
                v.save()
        return render(request=request, template_name="update_videos.html", context={})


class Process(View):

    @staticmethod
    def get(request, video_name):
        # UNIQUE FRAMES EXTRACTION
        keyframe.start_function(video_path=MEDIA_ROOT+"/videos/" + video_name)




        f = topic.topic_model()
        v = Video.objects.get(name="sample.mp4")
        v.navigation = f
        v.is_processed = True
        v.save()

        slides = Frame.objects.filter(f_type="SLIDE").order_by('id').all()
        anchors = []
        for each in slides:
            objects = lumino.predict_anchor(image_path=MEDIA_ROOT + "/SlideExtraction/output/Slides/" + each.name)
            if len(objects) > 0:
                e = Frame.objects.get(name=each.name)
                print(e)
                e.is_anchor = True
                e.anchor_label = objects[0]["label"]
                e.save()
                anchors.append(objects)

        return redirect(to="index")


class Topic(View):

    @staticmethod
    def get(request):
        f = topic.topic_model()
        v = Video.objects.get(name="sample.mp4")
        v.navigation = f
        v.save()
        return render(request=request, template_name="video_page.html", context={"topics": f})


class Anchor(View):

    @staticmethod
    def get(request):
        slides = Frame.objects.filter(f_type="SLIDE").order_by('id').all()
        anchors = []
        for each in slides:
            anchors.append(lumino.predict_anchor(image_path=MEDIA_ROOT + "/SlideExtraction/output/Slides/" + each.name))

        print(anchors)
        return render(request=request, template_name="video_page.html", context={"anchors": anchors})


class Navigation(View):

    @staticmethod
    def get(request):

        v = Video.objects.get(name="sample.mp4")
        topics = v.navigation
        final_topics = []

        t_topics = [{k: v for k, v in d.items() if k != 'timestamp'} for d in topics]
        print(t_topics)

        new_l = []
        for each in t_topics:
            if each not in new_l:
                new_l.append(each)

        for each in new_l:
            for foo in topics:
                if foo["topic"] == each["topic"] and "timestamp" not in each.keys():
                    each["timestamp"] = foo["timestamp"]


        print(new_l)



        anchor_list = []
        f = Frame.objects.filter(is_anchor=True).all()
        for each in f:
            temp = {}
            temp["type"] = each.anchor_label
            temp["image"] = each.name
            temp["timestamp"] = each.timestamp
            anchor_list.append(temp)



        return render(request=request, template_name="video_page.html", context={
            "topics": new_l,
            "anchor_list": anchor_list
        })


class DeleteVideo(View):

    @staticmethod
    def get(request):
        Frame.objects.all().delete()
        v = Video.objects.first()
        v.is_processed = False
        v.navigation = {}
        v.save()
        shutil.rmtree(path="/Users/balajidr/Developer/fyp_final/media/SlideExtraction")
        return redirect("/")
