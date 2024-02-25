import pickle
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
import numpy as np

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load the model and scaling
model = pickle.load(open('regression_model.pkl', 'rb'))
scaling = pickle.load(open('scaling.pkl', 'rb'))


@app.get('/')
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "prediction_text": ""})


@app.post('/predict')
def predict(request: Request, CRIM: float = Form(...), ZN: float = Form(...), INDUS: float = Form(...),
            CHAS: float = Form(...), NOX: float = Form(...), RM: float = Form(...), Age: float = Form(...),
            DIS: float = Form(...), RAD: float = Form(...), TAX: float = Form(...), PTRATIO: float = Form(...),
            B: float = Form(...), LSTAT: float = Form(...)):
    data = [CRIM, ZN, INDUS, CHAS, NOX, RM, Age, DIS, RAD, TAX, PTRATIO, B, LSTAT]
    final_input = scaling.transform(np.array(data).reshape(1, -1))
    output = model.predict(final_input)[0]
    return templates.TemplateResponse("home.html", {"request": request, "prediction_text": f"The House price prediction is {output:.2f}"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=7860)
