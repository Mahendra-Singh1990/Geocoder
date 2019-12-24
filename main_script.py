from flask import Flask, render_template, request, send_file
import pandas
from geopy.geocoders import ArcGIS
import datetime

app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])

def success():
    global filename
    if request.method=='POST':
        try:
            file_uploaded =request.files["fileToUpload"]
            file= pandas.read_csv(file_uploaded)
            nom = ArcGIS(timeout=3)
        except:
            return render_template("index.html", text="Please upload a file")
        try:
            file["Coordinates"] = file["Address"].apply(nom.geocode)
            file["Latitude"] = file["Coordinates"].apply(lambda x: x.latitude if x != None else None)
            file["Longitude"] = file["Coordinates"].apply(lambda x: x.longitude if x != None else None)
            file= file.drop('Coordinates', axis=1)
            filename=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"+'.csv')
            file.to_csv("filename",index=None)
            return render_template("index.html", text=file.to_html(), btn='download.html')
        except:
            return render_template("index.html", text="Please make sure to have a column named 'Address' in your file")


@app.route("/download-file/")
def download():
    return send_file(filename, attachment_filename='yourfile.csv',as_attachment=True)
if(__name__=="__main__"):
    app.run(debug=True)