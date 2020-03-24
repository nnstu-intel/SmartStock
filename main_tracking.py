import os
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

def visualizing_predictions_Classification(frame, preds):
    preds_box_list = preds['instances'].pred_boxes.tensor.cpu().numpy().astype(int).tolist()
    print(preds_box_list)
    if len(preds_box_list) > 0:
        for i in range(0, len(preds_box_list)):
            im = frame[preds_box_list[i][1]:preds_box_list[i][3], preds_box_list[i][0]:preds_box_list[i][2]]
            predictions = get_predictions_Classification(model_Classification, im)

            if (predictions[0][0] > 0.5):
                box_class = 'closed'
            else:
                box_class = 'opened'

            frame = cv2.putText(frame, box_class, (preds_box_list[i][0], preds_box_list[i][1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 255, 0), 2, cv2.LINE_AA)

    return frame

def visualize_predictions_Segmentation(frame, metadata, preds):
    v = Visualizer(frame[:, :, ::-1],
                   metadata=metadata,
                   scale=1,
                   instance_mode=ColorMode.IMAGE
                   )
    v = v.draw_instance_predictions(preds["instances"].to("cpu"))
    return v.get_image()[:, :, ::-1]

def get_predictions_Classification(model, input_image):
    img = input_image
    img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
    img = transforms.ToTensor().__call__(img)
    img = torchvision.transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]).__call__(img)
    img = img.unsqueeze_(0).to(device)
    img_dataset = torch.utils.data.TensorDataset(img)
    img_loader = torch.utils.data.DataLoader(img_dataset, batch_size=1)
    for img in img_loader:
        imag = img[0]
        with torch.set_grad_enabled(False):
            preds = model(imag)
        prediction = torch.nn.functional.softmax(preds, dim=1).data.cpu().numpy()
        print('Predictions:', prediction)

    return prediction

if __name__ == "__main__":

    # Segmentation settings
    models_pretrained_list = [
        "faster_rcnn_R_50_FPN_3x_700_box.pth",
        "mask_rcnn_R_50_C4_3x_700_box.pth",
        "mask_rcnn_R_50_FPN_3x_700_box.pth"
    ]
    models_pretrained_type_list = [
        "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml",
        "COCO-InstanceSegmentation/mask_rcnn_R_50_C4_3x.yaml",
        "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
    ]

    model_path = models_pretrained_list[2]

    MetadataCatalog.get("metadata_classes").set(thing_classes=["box"])

    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file(models_pretrained_type_list[2]))
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1

    cfg.MODEL.WEIGHTS = "output/" + model_path
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.80

    predictor = DefaultPredictor(cfg)
    metadata_classes = MetadataCatalog.get("metadata_classes")


    # Classification settings
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    path_to_model_Classification = 'output/ResNet18_Opened_vs_Closed_v2.pth'

    model_Classification = models.resnet18(pretrained=True)
    model_Classification.fc = torch.nn.Linear(model_Classification.fc.in_features, 2)
    model_Classification.load_state_dict(torch.load(path_to_model_Classification))
    model_Classification = model_Classification.to(device)
    model_Classification.eval()

    # Tracking
    cap = cv2.VideoCapture('samples/test1.mp4')

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter('result/rezult_example.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 25,
                          (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()

        preds = predictor(frame)

        frame = visualizing_predictions_Classification(frame, preds)

        image = visualize_predictions_Segmentation(frame, metadata_classes, preds)

        out.write(image)
        cv2.imshow('frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()