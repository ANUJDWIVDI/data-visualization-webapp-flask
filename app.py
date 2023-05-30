from flask import Flask, render_template, send_file, request, redirect
import os
from reportlab.lib.pagesizes import portrait
from reportlab.lib import colors
import zipfile
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image

from flask import Flask, render_template, jsonify

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

app.config['STATIC_FOLDER'] = "static"
# Home Page


#@app.route('/')
def homemm():
    return redirect('/start')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home')
def home1():
    return render_template('home.html')

# Age Page
@app.route('/age')
def age():
    return render_template('age.html')

# Gender Page
@app.route('/gender')
def gender():
    return render_template('gender.html')

# Zone Page
@app.route('/zone')
def zone():
    return render_template('zone.html')

# Device Used Page
@app.route('/deviceused')
def deviceused():
    return render_template('deviceused.html')

# Network Used Page
@app.route('/networkused')
def networkused():
    return render_template('networkused.html')

# Favorite Sport Page
@app.route('/favsport')
def favsport():
    return render_template('favsport.html')

# About Page
@app.route('/about')
def about():
    return render_template('about.html')






@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    image_folder = 'static'
    folders = ['Age', 'Gender', 'Device Used', 'Network Type', 'Zone', 'Sports']
    intro_image_path = os.path.join(image_folder, 'intro.png')
    ending_image_path = os.path.join(image_folder, 'end.png')
    bg_image_path = os.path.join(image_folder, 'BG-TEMP.png')
    pdf_path = os.path.join(image_folder, 'pdf', 'fds_project_report.pdf')

    pdf_canvas = canvas.Canvas(pdf_path, pagesize=portrait(A4))

    # Set background color
    pdf_canvas.setFillColorRGB(0.9, 0.9, 0.9)

    # Add introduction page
    pdf_canvas.drawImage(intro_image_path, x=0, y=0, width=A4[0], height=A4[1])

    for folder in folders:
        pdf_canvas.setFont('Helvetica-Bold', 30)  # Set the font and size for the header

        # Add a new page for each folder
        pdf_canvas.showPage()

        # Draw the background image
        pdf_canvas.drawImage(bg_image_path, x=0, y=0, width=A4[0], height=A4[1])

        # Draw the header in the middle top
        header_text = f"{folder} : Based Visualized Graphs on the Dataset Collected"
        pdf_canvas.drawCentredString(A4[0] / 2, A4[1] - 100, header_text)

        images = ['bar', 'pie', 'hist', 'box']
        images_per_row = 2

        # Calculate the center position for image justification
        center_x = A4[0] / 2 - (images_per_row * 320) / 2
        center_y = A4[1] / 2 - 240

        for i, image_type in enumerate(images):
            x_start = center_x + (i % images_per_row) * 320
            y_start = center_y + (i // images_per_row) * 300

            image_name = f'{folder}/{image_type}.jpg'
            image_path = os.path.join(image_folder, image_name)

            # Adjust image dimensions
            image_width = 320
            image_height = 240

            pdf_canvas.drawImage(image_path, x_start, y_start, width=image_width, height=image_height,
                                 preserveAspectRatio=True, anchor='nw')

        # Add some space below the images
        pdf_canvas.translate(0, -150)

    # Add ending page
    pdf_canvas.showPage()
    pdf_canvas.drawImage(ending_image_path, x=0, y=0, width=A4[0], height=A4[1])

    # Save the PDF file
    pdf_canvas.save()

    # Send the status as a response
    response_data = {'status': 'success'}
    return jsonify(response_data)







@app.route('/download_pdf')
def download_pdf():
    # Generate the PDF file
    generate_pdf()
    # Send the PDF file as a response
    file_path = os.path.join(app.config['STATIC_FOLDER'], 'pdf', 'fds_project_report.pdf')
    return send_file(file_path, as_attachment=True)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        device_used = request.form['device_used']
        network_type = request.form['network_type']
        zone = request.form['zone']
        sports = request.form['favourite_sport']


        # Read the existing data from the Excel file
        try:
            df = pd.read_excel('data.xlsx')
        except:
            df = pd.DataFrame(
                columns=['Name', 'Age', 'Gender', 'Device Used','Network Type','Zone','Sports'])

        # Append the new data to the existing data
        new_data = {'Name': name, 'Age': age, 'Gender': gender,'Device Used':device_used,'Network Type':network_type,'Zone':zone,'Sports':sports}
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

        # Save the data to the Excel file
        df.to_excel('data.xlsx', index=False)

        return render_template('success.html')

    else:
        # Render the form template
        return render_template('form.html')






@app.route('/start')
def generation_all():
    # Read the data from the Excel file
    data = pd.read_excel('data.xlsx')

    # Define the folder names for the visualizations
    folders = ['Age', 'Gender', 'Device Used', 'Network Type', 'Zone', 'Sports']

    # Define the labels for the visualizations
    # Define the labels for the visualizations
    labels = {
        'Age': 'Age',
        'Gender': 'Gender',
        'Device Used': 'Device Used',
        'Network Type': 'Network Type',
        'Zone': 'Zone',
        'Sports': 'Sports'
    }

    # Create the static folders if they don't already exist
    for folder in folders:
        if not os.path.exists(f'static/{folder}'):
            os.makedirs(f'static/{folder}')

    # Generate the visualizations for each folder
    for folder in folders:
        # Get the column name for the folder
        column = folder.replace('-', '_')

        # Generate the visualizations for each data type
        for data_type in ['bar', 'pie', 'hist', 'box']:
            print("Enter type o length ")
            # Define the filename for the visualization
            filename = f'{data_type}.jpg'

            # Generate the visualization
            if data_type == 'bar':
                plt.bar(data[column].value_counts().index, data[column].value_counts())
                plt.xlabel(labels[folder])
                plt.ylabel('Count')
            elif data_type == 'pie':
                plt.pie(data[column].value_counts(), labels=data[column].value_counts().index)
            elif data_type == 'hist':
                plt.hist(data[column], bins=range(0, 51, 5))
                plt.xlabel(labels[folder])
                plt.ylabel('Frequency')
            elif data_type == 'box':
                plt.boxplot(data.groupby(column)['Age'].apply(list), labels=data[column].unique())
                plt.xlabel(labels[folder])
                plt.ylabel('Age')

            # Save the visualization to the appropriate folder
            plt.savefig(f'static/{folder}/{filename}')

            # Clear the plot for the next visualization
            plt.clf()
    return render_template('home.html')



if __name__ == '__main__':
    app.run(debug=True)