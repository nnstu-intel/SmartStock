import cv2
import torch
import torchvision
from torchvision import transforms, models

def get_predictions(model, input_image):
    img = input_image
    img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
    image = img
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

    return image, prediction

if __name__ == "__main__":
    class_names = ['opened', 'closed']
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    path_to_model = 'ResNet18_Opened_vs_Closed_v2.pth'

    model = models.resnet18(pretrained=True)
    model.fc = torch.nn.Linear(model.fc.in_features, 2)
    model.load_state_dict(torch.load(path_to_model))
    model = model.to(device)
    model.eval()

    cap = cv2.VideoCapture(0)

    while (True):
        ret, frame = cap.read()
        img, predictions = get_predictions(model, frame)

        if (predictions[0][0] > 0.5):
            BoxClass = 'closed'
        else:
            BoxClass = 'opened'

        image = cv2.putText(frame, BoxClass, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()