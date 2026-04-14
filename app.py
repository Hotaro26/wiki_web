from flask import Flask, render_template, request
import requests

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def search_topic(query):
    url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=1&format=json"
    res = requests.get(url, headers=HEADERS)
    
    if res.status_code != 200:
        return None
    
    data = res.json()
    
    if data[1]:
        return data[1][0]
    
    return None


def get_summary(topic):
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + topic.replace(" ", "_")
    res = requests.get(url, headers=HEADERS)
    
    if res.status_code != 200:
        return None
    
    return res.json()


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    
    if request.method == "POST":
        query = request.form.get("topic")
        topic = search_topic(query)
        
        if topic:
            data = get_summary(topic)
            
            if data:
                result = {
                    "title": data.get("title"),
                    "summary": data.get("extract"),
                    "image": data.get("thumbnail", {}).get("source")
                }
    
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
