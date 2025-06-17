# File: Rest_API.py

from flask import Flask, request, jsonify

app = Flask(__name__)

# This function returns cleaned data from a sample (for topic.py use)
def get_cleaned_sample_data():
    # You can replace this with real data or a CSV reader
    sample_data = [
        {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
        {"sepal_length": 6.2, "sepal_width": 2.9, "petal_length": 4.3, "petal_width": 1.3},
    ]

    valid_ranges = {
        'sepal_length': (4.0, 8.0),
        'sepal_width': (2.0, 4.5),
        'petal_length': (1.0, 7.0),
        'petal_width': (0.1, 2.5)
    }

    cleaned = []
    for record in sample_data:
        try:
            cleaned_record = {}
            for key, val in record.items():
                val = float(val)
                min_val, max_val = valid_ranges[key]
                if min_val <= val <= max_val:
                    cleaned_record[key] = val
                else:
                    raise ValueError(f"{key} out of range")
            cleaned.append(cleaned_record)
        except:
            continue  # Skip invalid rows

    return cleaned


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

        return jsonify({"status": "success", "received_message": cleaned_data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
