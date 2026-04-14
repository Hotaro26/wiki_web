import requests
from bs4 import BeautifulSoup

def scrape_wikipedia(topic):
    url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to fetch page:", response.status_code)
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    title = soup.find("h1").text
    paragraphs = soup.find_all("p")
    
    print(f"\n📖 Title: {title}\n")
    
    count = 0
    for para in paragraphs:
        text = para.text.strip()
        if text:
            print(text, "\n")
            count += 1
        if count == 3:
            break

if __name__ == "__main__":
    topic = input("Enter topic: ")
    scrape_wikipedia(topic)
