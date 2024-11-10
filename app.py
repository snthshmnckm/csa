from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd

app = Flask(__name__)

# Path to the CSV file
CSV_FILE = 'car_sales.csv'

# Route to display the form to add a new car entry
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the form submission for adding a new car entry
@app.route('/add_car', methods=['POST'])
def add_car():
    # Get data from the form
    car_data = {
        'Brand': request.form['brand'],
        'Price': float(request.form['price']),
        'Body': request.form['body'],
        'Mileage': int(request.form['mileage']),
        'EngineV': float(request.form['engineV']),
        'Engine Type': request.form['engine_type'],
        'Registration': request.form['registration'],
        'Year': int(request.form['year']),
        'Model': request.form['model'],
        'Category': request.form['category']
    }

    # Load the existing CSV file
    df = pd.read_csv(CSV_FILE)

    # Convert car_data to a DataFrame with a single row
    new_row = pd.DataFrame([car_data])

    # Concatenate the new data to the existing DataFrame
    df = pd.concat([df, new_row], ignore_index=True)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(CSV_FILE, index=False)

    # Redirect to the results page to show updated analysis
    return redirect(url_for('results'))

# Route to display the results of the analysis
@app.route('/results')
def results():
    # Load the updated data
    df = pd.read_csv(CSV_FILE)

    # Perform analysis on the data
    analysis = perform_analysis(df)

    # Render the analysis results in the results template
    return render_template('results.html', analysis=analysis)

# Route to display charts
@app.route('/charts')
def charts():
    return render_template('charts.html')

# Route to provide data for charts in JSON format
@app.route('/chart_data')
def chart_data():
    df = pd.read_csv(CSV_FILE)
    chart_data = {
        "Brand": df['Brand'].value_counts().to_dict(),
        "Body": df['Body'].value_counts().to_dict(),
        "AveragePriceByBrand": df.groupby('Brand')['Price'].mean().to_dict()
    }
    return jsonify(chart_data)

# Function to perform analysis on the car data
def perform_analysis(df):
    results = {
        "Total Cars by Brand": df['Brand'].value_counts().to_dict(),
        "Average Price by Brand": df.groupby('Brand')['Price'].mean().to_dict(),
        "Cars by Category": df['Category'].value_counts().to_dict()
    }
    return results

if __name__ == '__main__':
    app.run(debug=True)
