import requests
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 🔎 Search best matching topic
def search_topic(query):
    url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=1&format=json"
    
    res = requests.get(url, headers=HEADERS)
    
    if res.status_code != 200:
        print("❌ Search failed:", res.status_code)
        return None
    
    try:
        data = res.json()
    except:
        print("❌ Failed to decode search response")
        return None
    
    if data[1]:
        return data[1][0]
    
    return None


# 📖 Get summary
def get_summary(topic):
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + topic.replace(" ", "_")
    
    res = requests.get(url, headers=HEADERS)
    
    if res.status_code != 200:
        print("❌ Summary fetch failed:", res.status_code)
        return None
    
    try:
        return res.json()
    except:
        print("❌ Failed to decode summary")
        return None


# 💾 Save to file (with custom path or Downloads fallback)
def save_to_file(data, include_image):
    filename = data["title"].replace(" ", "_") + ".txt"
    
    # Ask for path
    custom_path = input("\n📁 Enter custom save path (or press Enter for Downloads): ").strip()
    
    if custom_path:
        save_dir = os.path.expanduser(custom_path)
    else:
        save_dir = os.path.expanduser("~/Downloads")
    
    # Create dir if not exists
    os.makedirs(save_dir, exist_ok=True)
    
    full_path = os.path.join(save_dir, filename)
    
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(f"Title: {data.get('title')}\n\n")
        f.write(f"Summary:\n{data.get('extract')}\n\n")
        
        if include_image and "thumbnail" in data:
            f.write(f"Image URL:\n{data['thumbnail']['source']}\n")
    
    print(f"\n✅ Saved to: {full_path}")


# 🚀 MAIN FLOW

def main():
    query = input("🔎 Search topic: ")
    
    topic = search_topic(query)
    
    if not topic:
        print("❌ No results found")
        return
    
    print("✅ Found:", topic)
    
    data = get_summary(topic)
    
    if not data:
        return
    
    print("\n📖 Title:", data.get("title"))
    print("\n🧠 Summary:\n", data.get("extract"))
    
    # Ask to save
    save_choice = input("\n💾 Save to file? (y/n): ").lower()
    
    if save_choice == "y":
        image_choice = input("🖼️ Include image URL? (y/n): ").lower()
        include_image = image_choice == "y"
        
        save_to_file(data, include_image)
    
    print("\n✨ Done!")


if __name__ == "__main__":
    main()
