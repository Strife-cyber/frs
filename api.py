from flask import Flask, request, jsonify
from sqlalchemy.exc import IntegrityError
from functions import register, arrived, departed, assiduity, everyone, someone, arrivals, departures, update

app = Flask(__name__)

@app.route("/update", methods=["POST"])
def api_update():
    data = request.form
    profile = request.files.get("profile")

    if not all(k in data for k in ('name', 'phone', 'email', 'password', 'post')) or not profile:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        success = update(
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            password=data['password'],
            post=data['post'],
            profile=profile.read()
        )
        return jsonify({"success": success}), 201
    except IntegrityError:
        return jsonify({"error": "Operator already exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/register', methods=['POST'])
def api_register():
    data = request.form
    profile = request.files.get('profile')

    if not all(k in data for k in ('name', 'phone', 'email', 'password', 'post')) or not profile:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        success = register(
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            password=data['password'],
            post=data['post'],
            profile=profile.read()
        )
        return jsonify({"success": success}), 201
    except IntegrityError:
        return jsonify({"error": "Operator already exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/arrived', methods=['POST'])
def api_arrived():
    profile = request.files.get('profile')
    if not profile:
        return jsonify({"error": "Profile image is required"}), 400

    try:
        arrived(profile.read())
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/departed', methods=['POST'])
def api_departed():
    profile = request.files.get('profile')
    if not profile:
        return jsonify({"error": "Profile image is required"}), 400

    try:
        departed(profile.read())
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/assiduity/<string:operator_id>', methods=['GET'])
def api_assiduity(operator_id):
    try:
        result = assiduity(operator_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/operators', methods=['GET'])
def api_everyone():
    try:
        result = everyone()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/operator/<string:operator_id>', methods=['GET'])
def api_someone(operator_id):
    try:
        result = someone(operator_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/arrivals/<string:operator_id>', methods=['GET'])
def api_arrivals(operator_id):
    interval = request.args.get('interval', default=7, type=int)
    try:
        result = arrivals(operator_id, interval)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/departures/<string:operator_id>', methods=['GET'])
def api_departures(operator_id):
    interval = request.args.get('interval', default=7, type=int)
    try:
        result = departures(operator_id, interval)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
