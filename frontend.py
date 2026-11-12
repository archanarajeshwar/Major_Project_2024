from flask import Flask, request, render_template, flash, redirect 
from text_processor import TextProcessor
from data_extraction import ExtractPDFData
from prompt import Prompt
import os

app = Flask(__name__) 


@app.route("/cbc", methods=["GET", "POST"])
def upload_pdf():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file:
            filename = file.filename
            file.save(os.path.join("uploads/pdf", filename))
            file_path = os.path.join("uploads/pdf", filename)
            
            graphLab = ['Neutrophils', 'Lymphocytes', 'Eosinophils', 'Monocytes', 'Basophils']
            extract_pdf = ExtractPDFData()
            extracted_data = extract_pdf.extract_information(file_path)[0]
            graphVal = [extract_pdf.extract_value(extracted_data, keyword) for keyword in graphLab]
            print(graphVal)
            
            summary, type_of_amemia, diet, daily_activity = Prompt().generate_prompt(extracted_data)
            breakfast, lunch, dinner = TextProcessor().processor(diet)
            activities = TextProcessor().extract_activities(daily_activity)
            
            dietVal = {
                    'breakfast': breakfast,
                    'lunch': lunch,
                    'dinner': dinner,
                }
            
            data = {
                'summary': summary, 
                'type_of_amemia': type_of_amemia, 
                'daily_activity': activities,
                'graphLab':graphLab,
                'graphVal': graphVal,
                'diet': dietVal
            }

            graphData = {
                'graphLab':graphLab,
                'graphVal': graphVal,
            }
            
            return render_template("home.html", data=data , graphData=graphData)
        
    return render_template("upload.html")


if __name__=="__main__":
    app.run(debug=True, port=8080)