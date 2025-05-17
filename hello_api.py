from fastapi import FastAPI

# hello world api (creating a small api, if someone hits the endpoint, it will return hello world)
app = FastAPI()


@app.get("/")
def hello_world():
    return {"Message": "Hello World"}


@app.get("/about")
def about():
    return {"Message": "This is a simple API created using FastAPI."}
