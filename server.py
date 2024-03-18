from fastapi import FastAPI, UploadFile, Request
from pydantic_settings import BaseSettings
from typing import List, Optional
import uvicorn
import logging
from PIL import Image
import rawpy
import magic

from load_models import load_model
from contextlib import asynccontextmanager


class Settings(BaseSettings):
    model_name: str = "ram_plus"
    image_size: int = 384
    threshold: float = 0.68
    delete_tag_index: Optional[List[int]] = None


settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield load_model(
        settings.model_name,
        settings.image_size,
        settings.threshold,
        settings.delete_tag_index
    )


app = FastAPI(lifespan=lifespan)


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    console_formatter = uvicorn.logging.ColourizedFormatter(
        "{asctime} {levelprefix} : {message}",
        style="{", use_colors=True)
    logger.handlers[0].setFormatter(console_formatter)


@app.post("/")
async def handle(request: Request, file: UploadFile):
    inference = request.state.inference

    if is_raw_image(file):
        # TODO: may not work for all TIFF files, but tested with Nikon (.nef) and Sony (.arw) files
        rawImage = rawpy.imread(file.file)
        rgb = rawImage.postprocess(use_camera_wb=True)
        image = Image.fromarray(rgb)
    else:
        image = Image.open(file.file)

    return inference(image)

def is_raw_image(file: UploadFile):
    result = magic.from_buffer(file.file.read(2048), mime=True)
    file.file.seek(0)
    return result == "image/tiff"
