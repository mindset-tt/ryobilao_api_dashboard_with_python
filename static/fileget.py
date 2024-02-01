from fastapi.responses import RedirectResponse, FileResponse
from config.connect import app
import os
@app.get('/api/v1/images/{filename}', tags=['ຮູບພະນັກງານ'])
async def display(filename: str):
    op = os.path.abspath
    print (op)
    file_path = os.path.join(f"static\\images\\{filename}")
    if (filename.endswith('.png')):
        return FileResponse(file_path, media_type="image/png", filename=filename)
    elif (filename.endswith('.jpg')) or (filename.endswith('.jpeg')):
        return FileResponse(file_path, media_type="image/jpeg", filename=filename)
    elif filename.endswith('.webp'):
        return FileResponse(file_path, media_type="image/webp", filename=filename)
    else:
        return {"message": "ບໍ່ພົບຮູບພະນັກງານ"}

@app.get('/api/v1/attachs/{filename}', tags=['ເອກະສານຕ່າງໆ'])
async def display2(filename: str):
    file_path = os.path.join(f"static\\attachments\\{filename}")
    if (filename.endswith('.pdf')):
        return FileResponse(file_path, media_type="application/pdf", filename=filename)
    elif (filename.endswith('.docx')):
        return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename=filename)
    elif filename.endswith('.doc'):
        return FileResponse(file_path, media_type="application/msword", filename=filename)
    else:
        return {"message": "ບໍ່ພົບເອກະສານ"}
