from flask import Flask, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded.'})
    
    file = request.files['file']
    action = request.form['action']

    try:
        # Load the CSV file into a Pandas DataFrame
        data = pd.read_csv(file)

        if action == 'summary':
            # Return summary statistics
            result = data.describe().to_string()
            return jsonify({'result': result})

        elif action == 'histogram':
            # Plot histogram for pH values
            plt.figure(figsize=(10, 6))
            sns.histplot(data['pH'], kde=True, bins=30, color='blue')
            plt.title('pH Value Distribution')
            plt.xlabel('pH')
            plt.ylabel('Frequency')
            
            # Save the plot as a base64-encoded image
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            buffer.close()
            plt.close()
            
            return jsonify({'image': image_base64})

        elif action == 'scatter':
            # Scatter plot for pH vs Dissolved Oxygen
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x='pH', y='Dissolved Oxygen', data=data, color='green')
            plt.title('pH vs Dissolved Oxygen')
            plt.xlabel('pH')
            plt.ylabel('Dissolved Oxygen')
            
            # Save the plot as a base64-encoded image
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            buffer.close()
            plt.close()
            
            return jsonify({'image': image_base64})

        else:
            return jsonify({'error': 'Invalid action selected.'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
