# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`
from firebase_functions import https_fn
from firebase_admin import initialize_app, firestore
import numpy as np
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
from torchvision import transforms, models
from PIL import Image
import matplotlib.pyplot as plt

initialize_app()
db = firestore.client()

@https_fn.on_request()
def on_request_fish(req: https_fn.Request) -> https_fn.Response:
    test_transforms = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
    ])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = torch.load('/Users/owenrowe/functions/fishmodel_above_90.pth')
    model.eval()

    def predict_image(image):
        image_tensor = test_transforms(image).float()
        image_tensor = image_tensor.unsqueeze(0)
        input = image_tensor.to(device)
        output = model(input)
        index = output.data.cpu().numpy().argmax()
        classes = ['brook', 'brown', 'cutthroat', 'rainbow', 'tiger', 'other']
        predicted_class = classes[index]
        plt.imshow(image)

        return predicted_class

    # Retrieve the newest image from the Firebase database
    images_ref = db.collection('images')
    query = images_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
    docs = query.stream()
    for doc in docs:
        image_path = doc.get('path')

    if image_path:
        image = Image.open(image_path).convert("RGB")
        predicted_class = predict_image(image)
        return https_fn.Response(predicted_class)
    else:
        return https_fn.Response('No image found')

