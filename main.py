from api.CRUD import employee, department, position
from api.TASK import taskmanagement, workreport
from api.PROJECT import projectmaster
from model import model
from config.connect import app, cursor, conp
import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=3000,
        reload=True,
        debug=True,
    )
