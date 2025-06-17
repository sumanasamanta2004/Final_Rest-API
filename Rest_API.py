from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def echo_iris_data():
    try:
        # Get data from the JSON body
        data = request.get_json()

        # Extract all expected fields
        iris_fields = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        message = {field: data[field] for field in iris_fields}

        return jsonify({
            'status': 'success',
            'received_message': message
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
