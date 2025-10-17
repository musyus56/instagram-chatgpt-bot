from flask import Flask, request
import requests, openai

app = Flask(__name__)

VERIFY_TOKEN = "test_token"
ACCESS_TOKEN = "BURAYA_META_ACCESS_TOKEN_YAZ"
openai.api_key = "BURAYA_OPENAI_API_KEY_YAZ"

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verification token", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data.get("entry"):
        for entry in data["entry"]:
            for msg in entry.get("messaging", []):
                if "message" in msg and "text" in msg["message"]:
                    sender_id = msg["sender"]["id"]
                    user_text = msg["message"]["text"]

                    # ChatGPT'den yanıt al
                    ai_response = openai.ChatCompletion.create(
                        model="gpt-5",
                        messages=[{"role": "user", "content": user_text}]
                    )
                    reply_text = ai_response.choices[0].message.content

                    send_message(sender_id, reply_text)
    return "ok", 200

def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v21.0/me/messages?access_token={ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(port=5000)
