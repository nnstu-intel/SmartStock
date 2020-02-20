#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import sys
sys.setrecursionlimit(999999999)
block_cipher = None
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QFileDialog)
from PyQt5.QtCore import QCoreApplication
from Front3 import *
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import time
import cv2
from utils import *
from multiprocessing import Process, Queue, Manager
import requests
import json
import urllib3
import scipy.misc
import numpy as np
import os
from fpdf import FPDF
import random
import xlrd, xlwt
import qrcode
from datetime import datetime, date, time
import codecs

video_path = "!"
box_count = 0
coor_Warehouse = None
coor_Conveyor = None
next_box = False
count_frame = 1
count_Ware = 0
count_temp = 0
click = False
initBB = None
object_qr = {  
        'Number'   : int,
        'Data'     : str,
        'X' : int,
        'Y'   : int
}
cap_size_weight = 760
cap_size_height = 360
alert = False
arr_qr = []
Validation = False
Bigest = False
log =""
pas =""
count = 0
shet = 0

def send_mes(f_name):
      
      #print("sys")
      global log
      global pas 
      #log = self.ui.textEdit.toPlainText()
      #pas = self.ui.textEdit_2.toPlainText()
     
      #print(log)
      #print(pas)
      #time.sleep(10)
      
      if (log == "") or (pas == ""):
          
          print("авторизация отключена")
          #self.ui.textBrowser.setText("Set Login and Pasword")
      else:    
          try:
           api_autoriz = eval((requests.get('https://api.vk.com/oauth/token?grant_type=password&client_id=3697615&scope=offline,messages&client_secret=AlVXZFMUqyrnABp8ncuU&username='+str(log)+'&password='+str(pas)).text))  
           
           id_vk = api_autoriz['user_id']
           
           # !! создайте свое сообщество и получите токе с разрешиниями messages и docs
           token  = api_autoriz['access_token']
           
           server_url = requests.get('https://api.vk.com/method/docs.getMessagesUploadServer?type=doc&peer_id=' + str(id_vk) +'&access_token=' + str(token) + '&v=5.50').json()
           
           file = {'file': open(f_name,'rb')}
           ur = requests.post(server_url['response']['upload_url'], files=file).json()
           
           save_doc = requests.get('https://api.vk.com/method/docs.save?file='+ str(ur['file']) +'&title=box&access_token=' + str(token) + '&v=5.38').json()
           
           
           send_mes = requests.get('https://api.vk.com/method/messages.send?user_id=' + str(id_vk) +'&message=massege:&attachment=doc'+str(save_doc['response'][0]['owner_id']) + '_' + str(save_doc['response'][0]['id']) + '&access_token=' + str(token) + '&v=5.50').json()
          except:
             print("Failed send")
             
#/////////////////////////////////////////
#/////////////////////////////////////////GET BOX FROM IBM POWER AI VISION////////////////
#/////////////////////////////////////////
def get_pair_labels(image, frame):
    global coor_Conveyor
    
    Con_x = coor_Conveyor[0]
    Con_y = coor_Conveyor[1]
    Con_w = coor_Conveyor[2]
    Con_h = coor_Conveyor[3]
    
    url = 'http://172.19.12.55:8002/inference'
    filename = os.path.join(image)
    files = {
        'imagefile': open(filename, 'rb')
        }
    response = requests.post(url, files=files, verify=False)
    data = response.json()
    mas = []
    for i in data['classified']:
        y_max = i['ymax']
        y_min = i['ymin']
        x_max = i['xmax']
        x_min = i['xmin']
        cv2.rectangle(frame, (x_max, y_max), (x_min, y_min), (0, 255, 255), 2)
        if ( ( (x_min >= Con_x) and (x_max <= Con_x + Con_w) ) and ( (y_min >= Con_y) and (y_max <= Con_y + Con_h) ) ):
            mas = [x_max, x_min, y_max, y_min]
            print("in")
    if len(mas) == 0:
        return None
    else:
        return mas



#////////////////////////////////////////
#////////////////////////////////////////
#////////////////////////////////////////
def detection_Box(x, y, w, h, frame):
    global initBB
    global coor_Conveyor
    global coor_Warehouse
    global count_frame
    global count_temp
    global count_Ware
    global next_box
    
    Con_x = coor_Conveyor[0]
    Con_y = coor_Conveyor[1]
    Con_w = coor_Conveyor[2]
    Con_h = coor_Conveyor[3]
    
    Ware_x = coor_Warehouse[0]
    Ware_y = coor_Warehouse[1]
    Ware_w = coor_Warehouse[2]
    Ware_h = coor_Warehouse[3]
    
    if ( ( (x >= Con_x) and (x + w <= Con_x + Con_w) ) and ( (y >= Con_y) and (y + h <= Con_y + Con_h) ) ):
        print("In conveyor zone")
        count_temp = 0
        
    if ( ( (x >= Ware_x) and (x + w <= Ware_x + Ware_w) ) and ( (y >= Ware_y) and (y + h <= Ware_y + Ware_h) ) ):
        print("In Warehouse zone")
        count_temp = 0
        count_Ware+=1
        if count_Ware == 30:
            print("next")
            initBB = None
            next_box = True
            count_Ware = 0
    if not( ( (x >= Con_x) and (x + w <= Con_x + Con_w) ) and ( (y >= Con_y) and (y + h <= Con_y + Con_h) ) ):
        if not ( ( (x >= Ware_x) and (x + w <= Ware_x + Ware_w) ) and ( (y >= Ware_y) and (y + h <= Ware_y + Ware_h) ) ):
            count_temp+=1
    
    if count_temp >= 111:
        while True:
            cv2.putText(frame, "Warning!! Box undetected!!!", (100, 250),
    				cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
            cv2.putText(frame, "Press 'q' for exit", (100, 300),
    				cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
            key2 = cv2.waitKey(1) or 0xff
            cv2.imshow('Warning', frame)
            if key2 == ord("q"):
                break    
    
def draw_Coor(frame):
    global coor_Warehouse
    global coor_Conveyor
    global count_frame
    
    if count_frame == 1:
            cv2.putText(frame, "Select area Warehouse", (40, 40),
    				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            coor_Warehouse = cv2.selectROI("Frame", frame, fromCenter=False,
    			showCrosshair=True)
    if count_frame == 2:
        cv2.putText(frame, "Select area Conveyor", (40, 40),
				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        coor_Conveyor = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)
    if count_frame >= 3:
        cv2.rectangle(frame, (coor_Warehouse[0], coor_Warehouse[1]), (coor_Warehouse[0] + coor_Warehouse[2], coor_Warehouse[1] + coor_Warehouse[3]),(0, 255, 255), 2)
        cv2.rectangle(frame, (coor_Conveyor[0], coor_Conveyor[1]), (coor_Conveyor[0] + coor_Conveyor[2], coor_Conveyor[1] + coor_Conveyor[3]),(255, 255), 2)



#////////////////////////////////
#////////////////////////////////TREKING BOX//////////////////////////////
#////////////////////////////////
def traking_object():
    
    global video_path
    global coor_Warehouse
    global count_frame
    global next_box
    global initBB
    count_frame = 1
    
    (major, minor) = cv2.__version__.split(".")[:2]
    OPENCV_OBJECT_TRACKERS = {
            "csrt": cv2.TrackerCSRT_create,
            "kcf": cv2.TrackerKCF_create,
            "boosting": cv2.TrackerBoosting_create,
            "mil": cv2.TrackerMIL_create,
            "tld": cv2.TrackerTLD_create,
            "medianflow": cv2.TrackerMedianFlow_create,
            "mosse": cv2.TrackerMOSSE_create}
    tracker = OPENCV_OBJECT_TRACKERS["csrt"]()
    
    if video_path == "":
    	print("[INFO] starting video stream...")
    	vs = VideoStream(src=0).start()
    else:
    	vs = cv2.VideoCapture(video_path)
        
    fps = None
    temp = 0
    while True:
        
        frame = vs.read()
        if True:
            if video_path == "":
                frame = frame
            else: 
                frame = frame[1]
                
        if frame is None:
            break
        
        frame = imutils.resize(frame, 800)
        (H, W) = frame.shape[:2]
        
        draw_Coor(frame)
        
        if (initBB is None and temp == 20) or next_box:
            cv2.imwrite('1.jpg', frame)
            temp_mas = get_pair_labels('1.jpg', frame)
            
            if temp_mas != None:
                tracker = OPENCV_OBJECT_TRACKERS["csrt"]()
                initBB = (temp_mas[1], temp_mas[3], temp_mas[0] - temp_mas[1] + 20, temp_mas[2] - temp_mas[3] + 20)
                tracker.init(frame, initBB)
                fps = FPS().start()
                next_box = False
            temp = 0
            
        if initBB is not None:
            (success, box) = tracker.update(frame)
    
            if success:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 255, 0), 2)
    
            fps.update()
            fps.stop()
            info = [
    			("Tracker", "csrt"),
    			("Success", "Yes" if success else "No"),
    			("FPS", "{:.2f}".format(fps.fps())),
    		]
    
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
    				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            detection_Box(x, y, w, h, frame)
    
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        
        count_frame+=1
        temp+=1
        
        if key == ord("s"):
            initBB = cv2.selectROI("Frame", frame, fromCenter=False,
    			showCrosshair=True)
            print(initBB)
            tracker = OPENCV_OBJECT_TRACKERS["csrt"]()
            tracker.init(frame, initBB)
            fps = FPS().start()
    
        elif key == ord("q"):
            break
    if video_path == "":
    	vs.stop()
    else:
    	vs.release()
    
    cv2.destroyAllWindows()

def decode(im) : 
    decodedObjects = pyzbar.decode(im)  
    #for obj in decodedObjects:
     #   print('Type : ', obj.type)
     #   print('Data : ', obj.data,'\n')     
    return decodedObjects
    
def qrDecode(ret, frame):
    global alert
    global count 
    global shet 
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    decodedObjects = decode(im)
    global arr_qr
    arr_qr = []
    i = 1
    for decodedObject in decodedObjects: 
        points = decodedObject.polygon
        if len(points) > 4 : 
          hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
          hull = list(map(tuple, np.squeeze(hull)))
        else : 
          hull = points;
        n = len(hull)     
        for j in range(0,n):
          cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)
        x = decodedObject.rect.left
        y = decodedObject.rect.top
        #Проблема с кодировкой
        #Проблема с кодировкой
        barCode = decodedObject.data
        print("-----my------")
        print(barCode)
        object_qr['Number'] = i
        data = str(barCode)
        object_qr['Data'] = data
        #Проблема с кодировкой
        #Проблема с кодировкой
        object_qr['X'] = x
        object_qr['Y'] = y
        arr_qr.append(object_qr)
        print("----------------------------------------")
        print("arr_qr")
        print(arr_qr)
        
        print("----------------------------------------")
        if len(arr_qr) > count:
            shet+=1
        print("всего коробок")
        print(shet)
        mas_index = []
        index = 0
        
        print(data)
        for i in data:
            if i == '/':
                mas_index.append(index);
            index+=1
        number_production = ""
        ot = ""
        do = ""
        index = 0
        count = len(arr_qr)
        for i in data:
            if index > mas_index[2] and index < mas_index[3]:
                number_production+= i
            if index > mas_index[3] and index < mas_index[4]:
                ot+= i
            if index > mas_index[4] and index < mas_index[5]:
                do+= i
            index+=1
        do_date = datetime(int(do[4]+do[5]+do[6]+do[7]), int(do[2]+do[3]), int(do[0]+do[1]))
        now = datetime.now()
        delta = do_date - now
       
        if ((data[2] == "1") and (alert == False)) or delta.days < 0:
            alert = True
            pdf = FPDF()
            pdf.add_page()
            cv2.imwrite('1.jpg', frame)
            pdf.image("1.jpg", 0, 0, w = 100, h = 100)
            pdf.set_font("Arial", size=14)
            pdf.set_left_margin(100)
            pdf.ln(11)
            pdf.cell(0, 0, txt="The box in stock was open", ln=1)
            pdf.output("vk1.pdf")
            
            #Отправка в вк файлика
            send_mes('vk1.pdf')
            #Отправка в вк файлика
            i = 0 
            book = xlwt.Workbook(encoding="utf-8")
            sheet1 = book.add_sheet("Sheet 1")
            for k in arr_qr:
                sheet1.write(i, 0, i+1)
                data = str(k['Data'])
                sheet1.write(i, 1, data)
                id_s = random.randint(1000000000000000, 9999999999999999)
                sheet1.write(i, 2, id_s)
                i+=1
            book.save("data.xls")
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            pdf.set_left_margin(65)
            pdf.cell(0, 0, txt="Product Details", ln=1)
            pdf.ln(10)
            excel_data_file = xlrd.open_workbook("data.xls")
            sheet = excel_data_file.sheet_by_index(0)
            row_number = sheet.nrows
            for row in range(0,row_number):
                name = str(sheet.row(row)[1])
                pdf.cell(0, 0, txt=name[6:-1], ln=1)
                pdf.ln(10)
            pdf.output("vk2.pdf")
            #Отправка в вк файлика
            send_mes('vk2.pdf')
            #Отправка в вк файлика
        
    string = "Qantity of goods in stock " + str(len(arr_qr))
    cv2.putText(frame, string, (40, 40),
    				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.putText(frame, string, (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    if len(arr_qr) != 0: 
        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("Sheet 1")
        i = 0
        for k in arr_qr:
            print('Product ', i+1)
            sheet1.write(i, 0, i+1)
            data = str(k['Data'])
            sheet1.write(i, 1, data[2:-1])
            i+=1
        book.save("data.xls")
    
def qr_main():
    global Bigest
    global Validation
    global alert
    global cap_size_weight
    global cap_size_height
    global video_path
    Vpath = video_path
    print(Vpath)
    if (video_path == "!") or (video_path == ""):
        Vpath = 0
    cap = cv2.VideoCapture(Vpath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    count = 0
    global flag
    while(cap.isOpened()):
        ret, frame = cap.read()
        fps = cap.get(cv2.CAP_PROP_FPS)  
        frame = imutils.resize(frame, 400) 
        qrDecode(ret, frame)
                   
        temp = str(fps)
       #q cv2.putText(frame, temp, (0,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 2)
        if alert:
            cv2.putText(frame, "Box opening", (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        cv2.imshow('frame',frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
       
        if key == ord('p'):
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            pdf.set_left_margin(65)
            pdf.cell(0, 0, txt="Product Details", ln=1)
            pdf.ln(10)
            excel_data_file = xlrd.open_workbook("data.xls")
            sheet = excel_data_file.sheet_by_index(0)
            row_number = sheet.nrows
            count_list = 0
            for row in range(0,row_number):
                name = str(sheet.row(row)[1])
                name = name[6:-1]
                mas_index = []
                index = 0
                print(name)
                for i in name:
                    if i == '/':
                        mas_index.append(index);
                    index+=1
                iden = ""
                number_production = ""
                ot = ""
                do = ""
                place = ""
                index = 0
                for i in name:
                    if index > mas_index[1] and index < mas_index[2]:
                        iden+= i
                    if index > mas_index[2] and index < mas_index[3]:
                        number_production+= i
                    if index > mas_index[3] and index < mas_index[4]:
                        ot+= i
                    if index > mas_index[4] and index < mas_index[5]:
                        do+= i
                    if index > mas_index[5] and index < mas_index[6]:
                        place+= i
                    index+=1
                iden = str("Id: " + iden)
                pdf.cell(0, 0, txt=iden, ln=1)
                pdf.ln(10)
                number_production = str("Number production: " + number_production)
                pdf.cell(0, 0, txt=number_production, ln=1)
                if Bigest:
                    pdf.ln(10)
                    ot = str("Made by: " + ot)
                    pdf.cell(0, 0, txt=ot, ln=1)
                if Bigest or Validation:
                    pdf.ln (10)
                    do = str("Valid until: " + do)
                    pdf.cell(0, 0, txt=do, ln=1)
                if Bigest:
                    pdf.ln(10)
                    place = str("Producer: " + place)
                    pdf.cell(0, 0, txt=place, ln=1)
                pdf.ln(10)
                count_list+=1
                if count_list == 4:
                    pdf.add_page()
                    pdf.set_font("Arial", size=14)
                    pdf.set_left_margin(65)
                    pdf.ln(10)
                    count_list = 0
                    
            pdf.output("info.pdf")
            #Отправка в вк файлика
            #send__mes('info.pdf')
            #Отправка в вк файлика
    cap.release()
    cv2.destroyAllWindows()


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.video_choice)                     
        self.ui.pushButton_2.clicked.connect(self.web_choice)
        self.ui.pushButton_3.clicked.connect(self.exit_program)
        self.ui.pushButton_4.clicked.connect(self.FallingBox)
        self.ui.pushButton_5.clicked.connect(self.QROpenBox)
        self.ui.pushButton_6.clicked.connect(self.QRTimeBox)
      #  self.ui.pushButton_7.clicked.connect(self.QRCountBox)
     #   self.ui.pushButton_8.clicked.connect(self.Palets)


    #
    #НЕ РАБОТАЕТ
    #
    
    
    def video_choice(self):
        global click
        if not click:
            click = True
            global video_path
            fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
            video_path = fname
            self.ui.textBrowser.setText("Web mode selected\nvideo path: " + video_path)
            click = False
            return video_path
        else: 
            return
        
    
    def web_choice(self):
        global click
        if not click:
            click = True
            global video_path
            video_path = ""
            self.ui.textBrowser.setText("Web mode selected")
            click = False
        else: 
            return
    
    def exit_program(self):
        sys.exit()


    def FallingBox(self):
        global click
        if not click:
            click = True
            global video_path
            if video_path != "!":
                traking_object()
            else:
                self.ui.textBrowser.setText("Choose mode!")
            click = False
        else:
            return
        
    def QROpenBox(self):
        global click
        global Bigest
        global log
        global pas
        log = self.ui.textEdit.toPlainText()
        pas = self.ui.textEdit_2.toPlainText()
        if not click:
            click = True
            Bigest = True
            global video_path
            qr_main()
            click = False
        else: 
            return
    
    def QRTimeBox(self):
        global click
        global Validation
        global log
        global pas
        log = self.ui.textEdit.toPlainText()
        pas = self.ui.textEdit_2.toPlainText()
        if not click:
            click = True
            Validation = True
            global video_path
            qr_main()
            click = False
        else: 
            return
    
    #def QRCountBox():
        
        
    #def Palets():

            
if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
