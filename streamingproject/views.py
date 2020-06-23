from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponseServerError

from django.views.decorators import gzip
import cv2
import os
import sys
from box_tracking.detector import BoxDetector

boxDetector = BoxDetector("box_tracking/output/mask_rcnn_R_50_FPN_3x_700_box.pth",
                          "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml",
                          'box_tracking/output/ResNet18_Opened_vs_Closed_v2.pth',
                          'resnet18')


class VideoCamera(object):

    def __init__(self,path):
        self.video = cv2.VideoCapture("test3.mp4")
        self.score = 0

        self.ROOT_DIR = os.path.abspath("")
        print(self.ROOT_DIR)

        sys.path.append(self.ROOT_DIR)

        self.codec = cv2.VideoWriter_fourcc(*'DIVX')
        print("\nVizualize:")
        self.crossNow = 0
        self.crossLast = 0
        self.scoreCrossed = 0

    def __del__(self):
        self.video.read()

    # Обработчик фрейма
    def get_frame(self):
        self.ret, self.frame = self.video.read()
        if self.ret:
            self.frame, self.preds = boxDetector.frame_processing(self.frame)
            print(self.preds)
            jpeg = cv2.imencode('.jpg', self.frame)[1].tostring()
            return jpeg

        '''
        self.crossNow = 0
        setFrame = 0
        if self.ret:
            setFrame = setFrame + 1
            results = self.model.detect([self.frame], verbose=0)
            r = results[0]
            self.frame = self.regQR.pyzbar_qr_reader(self.frame)
            self.frame = self.display_instances(self.frame, r['rois'], r['masks'], r['class_ids'], self.class_names, r['scores'])

            (success, boxes) = self.trackers.update(self.frame)
            for box in boxes:
                (xTR, yTR, wTR, hTR) = [int(v) for v in box]
                cv2.rectangle(self.frame, (xTR, yTR), (xTR + wTR, yTR + hTR), (0, 0, 255), 2)

            if r['rois'] != []:
                for rs in r['rois']:
                    (y, x, h, w) = (rs[0].item(), rs[1].item(), rs[2].item(), rs[3].item())
                    (sw, sh) = (round((x + w)/2), round((y + h)/2))
                    if ((sw >= LINE) and (self.score < 10)):
                        if self.score == 0:
                            tracker = self.OPENCV_OBJECT_TRACKERS["csrt"]()
                            self.trackers.add(tracker, self.frame, (x, y, w - x, h - y))
                            self.score = self.score + 1

                        objs = self.trackers.getObjects()
                        add = False
                        for obj in objs:
                            add = True
                            (xOBJ, yOBJ, wOBJ, hOBJ) = (obj[0], obj[1], obj[0] + obj[2], obj[1] + obj[3])
                            print((xOBJ, yOBJ, wOBJ, hOBJ), ((sw, sh)))
                            if ((self.score != 0 and ((xOBJ-30 < sw) and (yOBJ-30 < sh) and (wOBJ+30 > sw) and (hOBJ+30 > sh))) or (sw < LINE)):
                                print("miss")
                                add = False
                                continue
                        if (add):
                            print('Add: ', sh, LINE, (x, y, w, h))
                            tracker = self.OPENCV_OBJECT_TRACKERS["csrt"]()
                            self.trackers.add(tracker, self.frame, (x, y, w - x, h - y))
                            self.score = self.score + 1


                    cv2.rectangle(self.frame, (x, y), (w, h), (0, 255, 0), 2)
                    cv2.circle(self.frame, (sw, sh), 5, (20, 215, 20), 5)

            objects = self.trackers.getObjects()
            for object in objects:
                (swOBJECT, shOBJECT) = (object[0] + object[2]/2, object[1] + object[3]/2)
                cv2.circle(self.frame, (int(round(swOBJECT)), int(round(shOBJECT))), 5, (100, 100, 100), 5)
                if (swOBJECT <= LINE):
                    self.crossNow = self.crossNow + 1
                    continue
            if (self.crossNow != self.crossLast):
                self.crossLast = self.crossNow
                self.scoreCrossed = self.scoreCrossed + 1


            cv2.putText(self.frame, str(self.score), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 3)
            cv2.putText(self.frame, str(self.scoreCrossed), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 3)
            cv2.line(self.frame, (LINE, 0), (LINE, 2000), (0, 255, 0), thickness=2)
            jpeg = cv2.imencode('.jpg', self.frame)[1].tostring()
            return jpeg'''

# Обработчик камеры
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def indexscreen(request):
    try:
        template = "screens.html"
        return render(request,template)
    except HttpResponseServerError:
        print("aborted")

@gzip.gzip_page
def dynamic_stream(request,num=0,stream_path="0"):
    return StreamingHttpResponse(gen(VideoCamera(stream_path)), content_type="multipart/x-mixed-replace;boundary=frame")
