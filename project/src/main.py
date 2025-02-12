from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def top():
    return 'top here'


@app.get("/echo/{thing}")
def echo(thing):
    return ' '.join([thing for _ in range(3)])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)