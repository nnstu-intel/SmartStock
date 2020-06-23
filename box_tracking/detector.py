import cv2

import torch
import torchvision
from torchvision import transforms, models

from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import ColorMode


class BoxDetector():

    def __init__(self, segmentation_model, segmentation_model_type, classification_model, classification_model_type):

        # Initialize Segmentation

        self.models_pretrained_list = [
            "faster_rcnn_R_50_FPN_3x_700_box.pth",
            "mask_rcnn_R_50_C4_3x_700_box.pth",
            "mask_rcnn_R_50_FPN_3x_700_box.pth"
        ]
        self.models_pretrained_type_list = [
            "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml",
            "COCO-InstanceSegmentation/mask_rcnn_R_50_C4_3x.yaml",
            "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
        ]


        #self.model_path = self.models_pretrained_list[2]
        self.model_path = segmentation_model
        MetadataCatalog.get("metadata_classes").set(thing_classes=["box"])
        self.metadata_classes = MetadataCatalog.get("metadata_classes")

        self.cfg = get_cfg()
        #self.cfg.merge_from_file(model_zoo.get_config_file(self.models_pretrained_type_list[2]))
        self.cfg.merge_from_file(model_zoo.get_config_file(segmentation_model_type))
        self.cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
        self.cfg.MODEL.WEIGHTS = self.model_path
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.80

        self.predictor = DefaultPredictor(self.cfg)


        # Initialize Classification

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        #self.path_to_model_Classification = 'output/ResNet18_Opened_vs_Closed_v2.pth'
        self.path_to_model_Classification = classification_model
        self.classification_model_type = classification_model_type

        if classification_model_type == 'resnet18':
            self.model_Classification = models.resnet18(pretrained=True)
            self.model_Classification.fc = torch.nn.Linear(self.model_Classification.fc.in_features, 2)
        elif classification_model_type == 'resnet50':
            self.model_Classification = models.resnet50(pretrained=True)
            self.model_Classification.fc = torch.nn.Linear(self.model_Classification.fc.in_features, 2)

        self.model_Classification.load_state_dict(torch.load(self.path_to_model_Classification))
        self.model_Classification = self.model_Classification.to(self.device)
        self.model_Classification.eval()

    def visualize_and_get_predictions_Classification(self, frame, preds):
        preds_box_list = preds['instances'].pred_boxes.tensor.cpu().numpy().astype(int).tolist()
        #print(preds_box_list)
        all_preds = []

        if len(preds_box_list) > 0:
            for i in range(0, len(preds_box_list)):
                im = frame[preds_box_list[i][1]:preds_box_list[i][3], preds_box_list[i][0]:preds_box_list[i][2]]
                predictions = self.get_predictions_Classification(self.model_Classification, im)

                if (predictions[0][0] > 0.5):
                    box_class = 'closed'
                else:
                    box_class = 'opened'

                all_preds.append([preds_box_list[i], box_class])

                frame = cv2.putText(frame, box_class, (preds_box_list[i][0], preds_box_list[i][1]),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.7, (0, 255, 0), 2, cv2.LINE_AA)

        return frame, all_preds

    def visualize_predictions_Segmentation(self, frame, metadata, preds):
        v = Visualizer(frame[:, :, ::-1],
                       metadata=metadata,
                       scale=1,
                       instance_mode=ColorMode.IMAGE
                       )
        v = v.draw_instance_predictions(preds["instances"].to("cpu"))
        return v.get_image()[:, :, ::-1]

    def get_predictions_Classification(self, model, input_image):
        img = input_image
        img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
        img = transforms.ToTensor().__call__(img)
        img = torchvision.transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]).__call__(img)
        img = img.unsqueeze_(0).to(self.device)
        img_dataset = torch.utils.data.TensorDataset(img)
        img_loader = torch.utils.data.DataLoader(img_dataset, batch_size=1)
        for img in img_loader:
            imag = img[0]
            with torch.set_grad_enabled(False):
                preds = model(imag)
            prediction = torch.nn.functional.softmax(preds, dim=1).data.cpu().numpy()
            #print('Predictions:', prediction)

        return prediction

    def frame_processing(self, frame):
        preds_classify = self.predictor(frame)

        frame, all_preds = self.visualize_and_get_predictions_Classification(frame, preds_classify)

        self.closed = 0
        self.opened = 0
        if len(all_preds) >= 1:
            for i in all_preds:
                if i[1] == 'opened':
                    self.opened += 1
                else:
                    self.closed += 1
        cv2.putText(frame, "Count boxes: " + str(self.opened + self.closed), (35, 20), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1)
        cv2.putText(frame, "Opened: " + str(self.opened), (35, 50), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1)
        cv2.putText(frame, "Closed: " + str(self.closed), (35, 80), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1)

        image = self.visualize_predictions_Segmentation(frame, self.metadata_classes, preds_classify)
        return image, all_preds
