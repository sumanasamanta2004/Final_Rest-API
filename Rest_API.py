# File: Rest_API.py

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def message():
    try:
        data = request.get_json()

        expected_fields = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        valid_ranges = {
            'sepal_length': (4.0, 8.0),
            'sepal_width': (2.0, 4.5),
            'petal_length': (1.0, 7.0),
            'petal_width': (0.1, 2.5)
        }

        cleaned_data = {}
        for field in expected_fields:
            if field not in data:
                return jsonify({"status": "error", "message": f"Missing: {field}"}), 400
            try:
                value = float(data[field])
            except ValueError:
                return jsonify({"status": "error", "message": f"{field} must be a number"}), 400
            min_val, max_val = valid_ranges[field]
            if not (min_val <= value <= max_val):
                return jsonify({"status": "error", "message": f"{field} must be between {min_val} and {max_val}"}), 400
            cleaned_data[field] = value

        # Save cleaned data to a temporary file
        with open("message_buffer.json", "w") as f:
            json.dump(cleaned_data, f)

        return jsonify({"status": "success", "received_message": cleaned_data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
