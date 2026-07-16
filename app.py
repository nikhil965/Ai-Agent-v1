import sys
import traceback
from flask import Flask, request, jsonify, send_from_directory

from agent import Agent

# ---- TEMPORARY DEBUG LINES: remove after diagnosing the issue ----
print("DEBUG sys.argv:", sys.argv)
print("DEBUG running file:", __file__)
print("DEBUG python executable:", sys.executable)
# --------------------------------------------------------------------

app = Flask(__name__, static_folder="static", static_url_path="")

# Single shared agent instance for the web server.
# If your Agent keeps per-user memory, you may want to create one per
# session instead (see note near /chat below).
agent = Agent()


@app.route("/")
def index():
    # Serves the frontend. Put index_space.html (renamed to index.html)
    # inside a "static" folder next to this file:
    #   LLMMM/
    #     app.py
    #     static/
    #       index.html   <-- your space-style frontend
    return send_from_directory(app.static_folder, "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_input = (data.get("message") or "").strip()

    if not user_input:
        return jsonify({"response": "empty message received."}), 400

    try:
        response = agent.run(user_input)
        return jsonify({"response": response})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"response": f"error: {e}"}), 500


def run_cli():
    """Original terminal mode, kept for convenience: python app.py --cli"""
    print("=" * 60)
    print("AI Agent")
    print("=" * 60)
    print("Type 'exit' to quit.")
    print()

    cli_agent = Agent()
    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["exit"]:
            break

        try:
            response = cli_agent.run(user_input)
            print(f"\nAgent:  {response}\n")
        except Exception as e:
            print(f"Error: {e}\n")


def run_web():
    print("=" * 60)
    print("AI Agent -- web server")
    print("=" * 60)
    print("Open http://localhost:5000 in your browser.")
    print("(Run 'python app.py --cli' for the old terminal mode.)")
    print()
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    print("DEBUG: entered __main__ block")
    if "--cli" in sys.argv:
        print("DEBUG: --cli flag detected, launching CLI mode")
        run_cli()
    else:
        print("DEBUG: no --cli flag, launching WEB mode")
        run_web()