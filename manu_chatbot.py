from flask import Flask, request, jsonify, render_template_string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# 🧠 FAQs
faqs = {
    "what is ghee": "Ghee is a type of clarified butter used in Indian cooking.",
    "how is ghee made": "Ghee is made by melting butter and removing milk solids and water.",
    "is ghee healthy": "Yes, when consumed in moderation, ghee is rich in healthy fats and vitamins.",
    "what are the uses of ghee": "Ghee is used in cooking, rituals, skincare, and as a health supplement.",
    "where is ghee used": "Ghee is used in Indian and Middle Eastern cuisines, and in Ayurvedic medicine.",
    "is ghee better than butter": "Many prefer ghee for its higher smoke point and lactose-free nature.",
}

questions = list(faqs.keys())
answers = list(faqs.values())

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

# 🎙️ Small Talk
def small_talk(msg):
    msg = msg.lower().strip()
    if msg in ["hi", "hello", "hey", "hlo"]:
        return "Hey there! 😊 I'm Manu. Ask me anything about ghee!"
    elif msg in ["bye", "goodbye", "see you"]:
        return "Goodbye! 👋 Stay healthy and enjoy your food with ghee!"
    elif msg in ["how are you", "how are you?"]:
        return "I'm feeling buttery smooth 😄 How can I help you today?"
    elif msg in ["thanks", "thank you"]:
        return "You're welcome! I'm always here to talk ghee!"
    return None

# 📚 FAQ Matching
def faq_bot(user_input):
    user_vec = vectorizer.transform([user_input.lower()])
    similarity = cosine_similarity(user_vec, X)
    idx = similarity.argmax()
    score = similarity[0][idx]
    if score > 0.5:
        return answers[idx]
    return "Hmm, I don't know that one yet. Try rephrasing or ask something else about ghee."

@app.route("/", methods=["GET"])
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Manu - Ghee Chatbot</title>
        <style>
            body { font-family: Arial; background: #fff9e6; padding: 30px; }
            #chat { max-width: 600px; margin: auto; background: #fff3cd; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px #ccc; }
            .user, .bot { margin: 10px 0; }
            .user { text-align: right; color: #007bff; }
            .bot { text-align: left; color: #343a40; }
            input { padding: 10px; width: 75%; border-radius: 5px; border: 1px solid #ccc; }
            button { padding: 10px 20px; border: none; background: #ffcc00; border-radius: 5px; margin-left: 10px; }
        </style>
    </head>
    <body>
        <div id="chat">
            <div class="bot"><b>Manu:</b> 👋 Hello! I’m <b>Manu</b>, your friendly ghee expert. Ask me anything!</div>
        </div>
        <input id="msg" placeholder="Type your message..." />
        <button onclick="send()">Send</button>

        <script>
            async function send() {
                let msg = document.getElementById("msg").value;
                if (!msg.trim()) return;

                document.getElementById("chat").innerHTML += `<div class='user'><b>You:</b> ${msg}</div>`;
                document.getElementById("msg").value = "";

                const response = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: msg })
                });

                const data = await response.json();
                document.getElementById("chat").innerHTML += `<div class='bot'><b>Manu:</b> ${data.reply}</div>`;
                document.getElementById("chat").scrollTop = document.getElementById("chat").scrollHeight;
            }

            document.getElementById("msg").addEventListener("keydown", function (e) {
                if (e.key === "Enter") send();
            });
        </script>
    </body>
    </html>
    """)

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "").strip()
    if not msg:
        return jsonify({"reply": "Please type something."})

    reply = small_talk(msg)
    if reply:
        return jsonify({"reply": reply})

    reply = faq_bot(msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
