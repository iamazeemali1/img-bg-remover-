from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from rembg import remove
import shutil
import uuid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    input_path = f"temp_{uuid.uuid4().hex}.png"
    output_path = f"output_{uuid.uuid4().hex}.png"

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    with open(input_path, "rb") as i:
        output_data = remove(i.read())

    with open(output_path, "wb") as o:
        o.write(output_data)

    return FileResponse(output_path, media_type="image/png")
