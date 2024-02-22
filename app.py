import pickle
from flask import Flask , request, jsonify, redirect, render_template
import pandas as pd , numpy as np 

app=Flask(__name__)
## load the model 
model = pickle.load(open('regression_model.pkl', 'rb'))
scaling = pickle.load(open('scaling.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict_api', methods = ['POST'])
def predict_api():
    data = request.json['data']
    data = np.array(list(data.values())).reshape(1,-1)
    # data = list(np.array(data.values()))
    new_data = scaling.transform(data)
    output = model.predict(new_data)
    return jsonify(output[0])

@app.route('/predict',methods=['POST'])
def predict():
    data=[float(x) for x in request.form.values()]
    final_input=scaling.transform(np.array(data).reshape(1,-1))
    print(final_input)
    output=model.predict(final_input)[0]
    return render_template("home.html",prediction_text="The House price prediction is {}".format(output))


if __name__ == '__main__':
    app.run(debug=True)
