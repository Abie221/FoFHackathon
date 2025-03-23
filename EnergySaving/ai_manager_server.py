
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)
messages = []  # Stores received messages

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the AI Manager API server. Use POST /receive to send messages."

@app.route('/receive', methods=['POST'])
def receive_message():
    data = request.get_json()
    messages.append(data)
    print(f"{datetime.datetime.now()} - Received message:", data)
    return jsonify({"status": "success", "message": "Message received"}), 200

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(messages), 200

def aggregate_decisions(messages):
    high_demand_count = sum(1 for m in messages if "High demand" in m["message"])
    deficit_count = sum(1 for m in messages if "deficit" in m["message"])
    surplus_count = sum(1 for m in messages if "surplus" in m["message"])
    undercharged_count = sum(1 for m in messages if "undercharged" in m["message"])
    optimal_count = sum(1 for m in messages if "optimal" in m["message"])

    decision = {}
    if high_demand_count >= 1 or deficit_count >= 1:
        decision["action"] = "Increase token burn rate and adjust procurement."
    elif surplus_count >= 1 or optimal_count > undercharged_count:
        decision["action"] = "Maintain or slightly decrease token burn rate, and charge storage."
    else:
        decision["action"] = "No major change required."

    decision["details"] = {
        "high_demand_count": high_demand_count,
        "deficit_count": deficit_count,
        "surplus_count": surplus_count,
        "undercharged_count": undercharged_count,
        "optimal_count": optimal_count,
    }
    
    decision["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return decision

@app.route('/aggregate', methods=['GET'])
def aggregate_endpoint():
    # Aggregate current messages and then optionally clear the messages
    decision = aggregate_decisions(messages)
    return jsonify(decision), 200

if __name__ == '__main__':
    app.run(port=9000)


# # ai_manager_server.py
# from flask import Flask, request, jsonify
# from decision_models import DecisionInput, DecisionOutput
# from decision_logic import make_decision
# import datetime

# app = Flask(__name__)
# messages = []  # Still used for agent messages

# @app.route('/', methods=['GET'])
# def index():
#     return "Welcome to the AI Manager API server. Use POST /receive for agent messages and POST /make_decision to compute a decision."

# @app.route('/receive', methods=['POST'])
# def receive_message():
#     data = request.get_json()
#     messages.append(data)
#     print(f"{datetime.datetime.now()} - Received agent message:", data)
#     return jsonify({"status": "success", "message": "Message received"}), 200

# @app.route('/messages', methods=['GET'])
# def get_messages():
#     return jsonify(messages), 200

# # New endpoint for decision-making
# @app.route('/make_decision', methods=['POST'])
# def decision_endpoint():
#     try:
#         # Parse the incoming JSON to a DecisionInput object
#         input_data = DecisionInput.parse_obj(request.get_json())
#     except Exception as e:
#         return jsonify({"error": "Invalid input", "details": str(e)}), 400

#     # Apply the decision logic
#     decision = make_decision(input_data)

#     # Return the decision as a JSON response
#     return jsonify(decision.dict()), 200

# if __name__ == '__main__':
#     app.run(port=9000)
