import llm
from conf import *
from flask import Flask, request, jsonify, render_template
import time
import os
import summarization
import recommendation

DELIMITER = ":::EOM:::"  # Define the end-of-conversation delimiter

app = Flask(__name__)

conversation = []

@app.route('/')
def home():
    """Render the homepage with a text box for user input."""
    return render_template('conversation.html')

@app.route('/converse', methods=['POST'])
def converse():
    """Handle the AI conversation with user input."""
    global conversation

    try:
        # Retrieve user input from the JSON request
        data = request.get_json()
        user_msg = data.get('user_input', '').strip() if data else ''

        if not user_msg:
            return jsonify({"error": "Empty input received."}), 400

        if user_msg == "~~~~~":
            # Initialize conversation with the starting prompt
            conversation_prompt = "config/conv_2.txt"
            try:
                with open(conversation_prompt, "r") as f:
                    starting_msg = f.read()
                conversation.append({"role": "system", "content": starting_msg})
            except FileNotFoundError:
                return jsonify({"error": "Conversation prompt file not found."}), 500

            # First AI response
            ai_msg = llm.get_msg(conversation=conversation)
            conversation.append({"role": "assistant", "content": ai_msg})

            return jsonify({"response": ai_msg, "end": False})

        elif user_msg == "DEBUG_TTTTTT":
            return jsonify({"response": "DEBUGGING", "end": True})

        else:
            # Append user's message to the conversation
            conversation.append({"role": "user", "content": user_msg})

            # Get AI response
            ai_msg = llm.get_msg(conversation=conversation)
            conversation.append({"role": "assistant", "content": ai_msg})

            # Check for the end-of-conversation delimiter
            if DELIMITER in ai_msg:
                return jsonify({"response": ai_msg.replace(DELIMITER, ""), "end": True})
            else:
                return jsonify({"response": ai_msg, "end": False})

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/export', methods=['GET'])
def export_conversation():
    """Export the conversation to a text file."""
    try:
        # Create a timestamped folder for the conversation
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        folder_name = f"conversation_{timestamp}"
        os.makedirs(folder_name, exist_ok=True)

        # Save the conversation
        output_file = os.path.join(folder_name, "conversation.txt")
        with open(output_file, "w") as f:
            for turn in conversation[1:]:
                f.write(f"{turn['role']}:\n{turn['content']}\n\n")

        # Summarize the conversation
        summarization_file = os.path.join(folder_name, "summarization.txt")
        summarization.summarize(SUMMARIZATION_PROMPT, output_file, summarization_file)

        # Generate recommendations
        recommendation_file = os.path.join(folder_name, "recommendation.txt")
        recommendation.recommend(RECOMMENDATION_PROMPT, summarization_file, LIST_TESTS, recommendation_file)

        return jsonify({
            "message": "Conversation exported successfully.",
            "files": {
                "conversation": output_file,
                "summarization": summarization_file,
                "recommendation": recommendation_file
            }
        })

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred during export: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
