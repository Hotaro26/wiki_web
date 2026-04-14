import requests
import os
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 🔎 Search best matching topic
def search_topic(query):
    url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=1&format=json"
    
    res = requests.get(url, headers=HEADERS)
    
    if res.status_code != 200:
        console.print(f"[red]❌ Search failed:[/red] {res.status_code}")
        return None
    
    try:
        data = res.json()
    except:
        console.print("[red]❌ Failed to decode search response[/red]")
        return None
    
    if data[1]:
        return data[1][0]
    
    return None


# 📖 Get summary
def get_summary(topic):
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + topic.replace(" ", "_")
    
    res = requests.get(url, headers=HEADERS)
    
    if res.status_code != 200:
        console.print(f"[red]❌ Summary fetch failed:[/red] {res.status_code}")
        return None
    
    try:
        return res.json()
    except:
        console.print("[red]❌ Failed to decode summary[/red]")
        return None


# 💾 Save to file
def save_to_file(data, include_image):
    filename = data["title"].replace(" ", "_") + ".txt"
    
    custom_path = Prompt.ask("\n📁 Enter custom save path (or press Enter for Downloads)", default="")
    
    if custom_path:
        save_dir = os.path.expanduser(custom_path)
    else:
        save_dir = os.path.expanduser("~/Downloads")
    
    os.makedirs(save_dir, exist_ok=True)
    
    full_path = os.path.join(save_dir, filename)
    
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(f"Title: {data.get('title')}\n\n")
        f.write(f"Summary:\n{data.get('extract')}\n\n")
        
        if include_image and "thumbnail" in data:
            f.write(f"Image URL:\n{data['thumbnail']['source']}\n")
    
    console.print(f"\n[green]✅ Saved to:[/green] {full_path}")


# 🚀 MAIN
def main():
    console.print(Panel("[bold cyan]🌐 Wikipedia CLI Scraper[/bold cyan]"))

    query = Prompt.ask("[yellow]🔎 Search topic[/yellow]")
    
    topic = search_topic(query)
    
    if not topic:
        console.print("[red]❌ No results found[/red]")
        return
    
    console.print(f"[green]✅ Found:[/green] {topic}")
    
    data = get_summary(topic)
    
    if not data:
        return
    
    console.print(Panel(f"[bold]{data.get('title')}[/bold]\n\n{data.get('extract')}", title="📖 Summary"))
    
    save_choice = Prompt.ask("\n💾 Save to file? (y/n)", choices=["y", "n"])
    
    if save_choice == "y":
        image_choice = Prompt.ask("🖼️ Include image URL? (y/n)", choices=["y", "n"])
        include_image = image_choice == "y"
        
        save_to_file(data, include_image)
    
    console.print("\n[bold green]✨ Done![/bold green]")


if __name__ == "__main__":
    main()
