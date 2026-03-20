import os
import requests
from datetime import datetime

# API anahtarı GitHub Secrets'tan gelecek
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_automated_blog():
    if not API_KEY:
        print("❌ ERROR: DEEPSEEK_API_KEY not found.")
        return

    target_dir = os.path.join(os.getcwd(), 'src', 'content', 'blog')
    os.makedirs(target_dir, exist_ok=True)

    # ÖRNEĞE TAM UYUMLU PROMPT
    prompt = """
    Write a technical, high-quality English blog post similar to a 'Research Lab' report.
    Topic: A trending 2026 technology (AI, Cybersecurity, Cloud, or Networking).
    
    STRUCTURE REQUIREMENTS (FOLLOW EXACTLY):
    1. FRONTMATTER:
    ---
    title: "[A Technical & Catchy Title]"
    description: "[150-character technical SEO summary]"
    pubDate: {date}
    author: "DataSecureTools Research Labs"
    tags: ["Tech", "Innovation", "Analysis"]
    ---
    
    2. CONTENT START:
    Start with a '# [Same Title]' as an H1 header.
    Follow with an engaging introduction mentioning 'DataSecureTools'.
    
    3. BODY:
    - Minimum 1200 words.
    - Use H2 (##) and H3 (###) for subheadings.
    - Use bold text for key terms.
    - Use bullet points for lists.
    - End with a 'Conclusion' section.
    
    4. LANGUAGE: Professional, technical, and academic English.
    """.format(date=datetime.now().strftime('%Y-%m-%d'))

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a senior technical writer at DataSecureTools Research Labs. You write in-depth, SEO-optimized markdown reports."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 4000
    }

    try:
        print("🤖 Crafting a specialized report for DataSecureTools...")
        response = requests.post(API_URL, json=data, headers=headers, timeout=180)
        response.raise_for_status()
        
        content = response.json()['choices'][0]['message']['content']
        
        # Markdown bloğu (```markdown) temizleme (Astro'da hata verir)
        if content.startswith("```"):
            content = "\n".join(content.split("\n")[1:-1])

        filename = f"blog-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        file_path = os.path.join(target_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
            
        print(f"✅ SUCCESS: {filename} matches your template.")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    generate_automated_blog()
    