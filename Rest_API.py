from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def message():
    try:
        data = request.get_json()

        # Expected input features
        expected_fields = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        
        # Define valid ranges for each field
        valid_ranges = {
            'sepal_length': (4.0, 8.0),
            'sepal_width': (2.0, 4.5),
            'petal_length': (1.0, 7.0),
            'petal_width': (0.1, 2.5)
        }

        cleaned_data = {}

        # Inline validation: check type and range
        for field in expected_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f"Missing required field: {field}"
                }), 400

            try:
                value = float(data[field])
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': f"Invalid value for '{field}': must be a number."
                }), 400

            min_val, max_val = valid_ranges[field]
            if not (min_val <= value <= max_val):
                return jsonify({
                    'status': 'error',
                    'message': f"'{field}' must be between {min_val} and {max_val}."
                }), 400

            cleaned_data[field] = value

        # Everything is valid
        return jsonify({
            'status': 'success',
            'received_message': cleaned_data
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f"Unexpected error: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
