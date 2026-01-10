import json

SUBSCRIBERS_FILE = "subscribers.json"

def load_subscribers():
    """Load subscribers from JSON file"""
    try:
        with open(SUBSCRIBERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_subscribers(subs):
    """Save subscribers to JSON file"""
    with open(SUBSCRIBERS_FILE, 'w') as f:
        json.dump(subs, f, indent=2)

def add_subscriber(fridge_id, chat_id):
    """Add a subscriber to a fridge"""
    subs = load_subscribers()
    if fridge_id not in subs:
        subs[fridge_id] = []
    if chat_id not in subs[fridge_id]:
        subs[fridge_id].append(chat_id)
    save_subscribers(subs)
    print(f"Added subscriber {chat_id} to fridge {fridge_id}")

def get_subscribers(fridge_id):
    """Get all subscribers for a fridge"""
    subs = load_subscribers()
    return subs.get(fridge_id, [])