from io import BytesIO

import torch
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from PIL import Image

from src.api.schemas import SingleResult
from src.api.utils import get_labels, get_model, preprocess_image


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return RedirectResponse("/docs")


@app.post("/predict")
async def predict_image(file: UploadFile = File(...)) -> SingleResult:
    contents = await file.read()

    image = Image.open(BytesIO(contents))
    img_tensor = preprocess_image(image)

    model = get_model()

    output = model(img_tensor)
    _, pred = torch.max(output, 1)

    labels = get_labels()
    result = labels[pred.item()]

    return {
        "filename": file.filename,
        "result": result,
    }
