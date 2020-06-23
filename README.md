Box Segmentation and Classification
====

This program is intended for segmentation of boxes on the image, video and webcam with subsequent classification into classes: open and closed, identification anomalies.

The solution is presented as a web service written in django. 
Linux is the preferred system due to possible problems installing the detectron 2 framework.

Upload the segmentation model to the directory ```../box_tracking/output/``` and follow this commands:

```
cd SmartStock
python manage.py runserver
```
Next, follow the link ```http://127.0.0.1:8000/stream/screen/``` to see the result

