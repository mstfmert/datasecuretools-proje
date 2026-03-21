import os
import requests
import re
import random
from datetime import datetime

# API anahtarı GitHub Secrets'tan gelecek
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

def slugify(text):
    """Başlığı URL dostu dosya ismine dönüştürür."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def generate_automated_blog():
    if not API_KEY:
        print("❌ ERROR: DEEPSEEK_API_KEY not found.")
        return

    target_dir = os.path.join(os.getcwd(), 'src', 'content', 'blog')
    os.makedirs(target_dir, exist_ok=True)

    # KONU ÇEŞİTLİLİĞİ İÇİN HAVUZ (Burayı dilediğin gibi genişletebiliriz)
    topics = [
        "Post-Quantum Cryptography", "Edge Computing in 2026", "Zero Trust Architecture",
        "AI-Driven Threat Hunting", "Decentralized Identity (DID)", "6G Networking Trends",
        "Neuromorphic Computing", "Sustainable Green Data Centers", "Space-Based Internet Security",
        "Bio-Digital Data Storage", "Autonomous Cybersecurity Agents"
    ]
    selected_topic = random.choice(topics)

    # ÖZGÜNLÜK İÇİN GÜNCELLENMİŞ PROMPT
    prompt = f"""
    Write a UNIQUE, high-quality technical report for DataSecureTools Research Labs.
    Focus Topic: {selected_topic} - Explore a very specific, niche aspect of this.
    
    REQUIREMENTS:
    1. DO NOT REPEAT previous generic AI or Cloud topics. Be specific and advanced.
    2. FRONTMATTER (Exact Format):
    ---
    title: "[Unique & Technical Title]"
    description: "[150-char SEO summary]"
    pubDate: {datetime.now().strftime('%Y-%m-%d')}
    author: "DataSecureTools Research Labs"
    tags: ["{selected_topic}", "Analysis", "2026-Trends"]
    ---
    
    3. CONTENT:
    - Start with '# [Title]'.
    - Use H2 (##) and H3 (###) for technical depth.
    - Min 1200 words. Technical and academic English.
    - Mention 'DataSecureTools' naturally in the intro.
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a specialized cybersecurity and future-tech analyst. You avoid repetitive topics and provide deep technical insights."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.85, # Daha özgün ve yaratıcı cevaplar için yükselttik
        "max_tokens": 4000
    }

    try:
        print(f"🤖 Researching: {selected_topic} for DataSecureTools...")
        response = requests.post(API_URL, json=data, headers=headers, timeout=200)
        response.raise_for_status()
        
        content = response.json()['choices'][0]['message']['content']
        
        # Markdown bloklarını temizle
        if content.startswith("```"):
            content = "\n".join(content.split("\n")[1:-1])

        # BAŞLIĞI AYIKLA VE DOSYA ADI YAP
        # Title: "..." kısmını bulur
        title_match = re.search(r'title:\s*"(.*?)"', content)
        if title_match:
            raw_title = title_match.group(1)
            filename = f"{slugify(raw_title)}.md"
        else:
            filename = f"report-{datetime.now().strftime('%Y%m%d-%H%M')}.md"

        file_path = os.path.join(target_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
            
        print(f"✅ SUCCESS: {filename} published with unique content.")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    generate_automated_blog()