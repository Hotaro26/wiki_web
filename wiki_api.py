import requests

def get_summary(topic):
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + topic.replace(" ", "_")
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    res = requests.get(url, headers=headers)
    
    print("Status code:", res.status_code)  # 👈 important
    
    if res.status_code != 200:
        print("Error:", res.text)
        return
    
    data = res.json()
    
    print("\n📖 Title:", data.get("title"))
    print("\n🧠 Summary:\n", data.get("extract"))

topic = input("Enter topic: ")
get_summary(topic)
