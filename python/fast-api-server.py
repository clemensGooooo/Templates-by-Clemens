# Interactive API docs: http://127.0.0.1:8000/docs
# Alternative API docs: http://127.0.0.1:8000/redoc

from typing import Union, List
from fastapi import FastAPI, Form, UploadFile, Request

from fastapi.staticfiles import StaticFiles
from Imageresizer import ImageResizer
from PDFTool import PDFTool
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pathlib

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/upload", StaticFiles(directory="upload"), name="upload")

@app.get("/")
def read_root():
    return "Hello world"


@app.post("/format/")
async def create_upload_file(file: UploadFile,format: str = Form()):
    try:
        filename =  await save_in_cache(file)
        image = Image.open(f"./cache/{filename}")
        image = image.convert('RGB')
        filenameFull =  filename.replace("."+filename.split(".").pop(),"")
        image.save(f"{pathlib.Path(__file__).parent.absolute()}/upload/{filenameFull}.{format}")
        return {"filename": f"{filenameFull}.{format}"}
    except Exception as e:
        return {"error": "500"}


@app.post("/resize/")
async def create_upload_file(file: UploadFile,size_x: int = Form(),size_y: int = Form()):
    try:
        filename =  await save_file(file)
        print(filename)
        if isinstance(filename,str):
           filename = await reziseImage(filename,size_x,size_y)
           return filename
        else:
          return {"error":"500"}
    except Exception as e:
        return {"error": "500"}


@app.post("/pdfToDocx/")
async def create_upload_file(file: UploadFile):
    try:
        filename =  await save_file(file)
        if isinstance(filename,str):
           filename = await PDFTool.pdfToWord(filename)
           return filename
        else:
          return {"error":"500"}
    except Exception as e:
        print(e)
        return {"error": "500"}


async def save_file(file):
    try:
        filename = file.filename
        content = await file.read()
        with open(f"upload/{filename}", "wb") as f:
            f.write(content)
        return filename
    except Exception as e:
        return {"error": str(e)}


async def reziseImage(filename,x,y):
        if ImageResizer.checkIfImage(f"upload/{filename}"):
            ImageResizer.resize(f"upload/{filename}",f"upload/{filename}",(x,y))
            return {"filename": filename}
        else:
            return {"error":"wrong data type"}


async def save_in_cache(file):
    try:
        filename = file.filename
        content = await file.read()
        with open(f"cache/{filename}", "wb") as f:
            f.write(content)
        return filename
    except Exception as e:
        return {"error": str(e)}