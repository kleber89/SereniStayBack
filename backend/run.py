from app import app
import uvicorn

if __name__ == '__main__':
    uvicorn.run("app.__init__:app", host="127.0.0.1", port=4000, reload=True)