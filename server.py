from fastapi import FastAPI, UploadFile, Request
from pydantic_settings import BaseSettings
from typing import List, Optional
import uvicorn
import logging
from PIL import Image

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
    image = Image.open(file.file)
    return inference(image)
