from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "fridge.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS fridges (
            fridge_id TEXT PRIMARY KEY,
            chat_id TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fridge_id TEXT,
            item_name TEXT,
            expires_in INTEGER
        )
    """)

    conn.commit()
    conn.close()

def handle_join(chat_id, fridge_id):
    if not fridge_id:
        return jsonify({"response": "Please provide a fridge ID to join."}), 200

    fridge_id = fridge_id.strip().upper()

    conn = sqlite3.connect("fridge.db")
    cur = conn.cursor()

    # Prevent duplicate joins
    cur.execute("SELECT * FROM fridges WHERE fridge_id=? AND chat_id=?", (fridge_id, chat_id))
    if cur.fetchone():
        conn.close()
        return jsonify({"response": f"You are already in fridge {fridge_id}."}), 200

    # Insert subscription
    cur.execute("INSERT INTO fridges (fridge_id, chat_id) VALUES (?, ?)", (fridge_id, chat_id))
    conn.commit()
    conn.close()

    return jsonify({"response": f"✅ You have successfully joined fridge {fridge_id}!"}), 200


@app.route("/")
def home():
    return "Fridge Bot is running."

def handle_add(chat_id, args):
    if not args:
        return jsonify({"response": "Please provide an item and days, e.g., ADD bagels, 2"}), 200

    try:
        item_name, expires_in = [x.strip() for x in args.split(",", 1)]
        expires_in = int(expires_in)
    except ValueError:
        return jsonify({"response": "⚠️ Invalid command format. Use: ADD <item>, <days>"}), 200

    conn = sqlite3.connect("fridge.db")
    cur = conn.cursor()

    # Find all fridges user belongs to
    cur.execute("SELECT fridge_id FROM fridges WHERE chat_id=?", (chat_id,))
    fridges = cur.fetchall()
    if not fridges:
        conn.close()
        return jsonify({"response": "You are not in any fridge. Join one first with JOIN <fridge>."}), 200

    # Add item to each fridge
    for (fridge_id,) in fridges:
        cur.execute("INSERT INTO items (fridge_id, item_name, expires_in) VALUES (?, ?, ?)",
                    (fridge_id, item_name, expires_in))

    conn.commit()
    conn.close()

    return jsonify({"response": f"✅ Added **{item_name}** (expires in {expires_in} days) to your fridge(s)."}), 200



@app.route("/bot", methods=["POST"])
def bot():
    data = request.get_json()  # expects JSON: {"chat_id": "...", "message": "..."}
    if not data or "chat_id" not in data or "message" not in data:
        return jsonify({"error": "Invalid request"}), 400

    chat_id = data["chat_id"]
    message = data["message"].strip()

    # Split message into command and arguments
    parts = message.split(" ", 1)
    command = parts[0].upper()
    args = parts[1] if len(parts) > 1 else ""

    if command == "JOIN":
        return handle_join(chat_id, args)
    elif command == "ADD":
        return handle_add(chat_id, args)
    else:
        return jsonify({"response": f"Unknown command: {command}"}), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
