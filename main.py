from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from rembg import remove
import shutil
import uuid

app = FastAPI()

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    input_path = f"temp_{uuid.uuid4().hex}.png"
    output_path = f"output_{uuid.uuid4().hex}.png"

    # Save uploaded file
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Remove background
    with open(input_path, "rb") as i:
        input_data = i.read()
        output_data = remove(input_data)

    # Save output
    with open(output_path, "wb") as o:
        o.write(output_data)

    return FileResponse(output_path, media_type="image/png")
