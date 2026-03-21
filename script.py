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
    # Türkçe karakter desteği gerekirse buraya ekleme yapılabilir, şu an İngilizce odaklı
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def generate_automated_blog():
    if not API_KEY:
        print("❌ ERROR: DEEPSEEK_API_KEY not found.")
        return

    target_dir = os.path.join(os.getcwd(), 'src', 'content', 'blog')
    os.makedirs(target_dir, exist_ok=True)

    # 1. GENİŞLETİLMİŞ KONU KATMANLARI (Hibrid Model)
    categories = {
        "Web Performans & UX": [
            "Core Web Vitals 2026 Optimization", "Edge Computing for LCP", "INP Optimization Strategies",
            "Next-gen Image Formats (AVIF vs WebP2)", "Zero-latency APIs in 2026", "Server-side Rendering 2026"
        ],
        "SEO & Dijital Pazarlama": [
            "AI Search (SGE) Optimization", "Programmatic SEO for SaaS", "Zero-click Search Trends",
            "Domain Authority vs Trust Signals", "AI-driven Search Intent Analysis", "Ethical Web Scraping for SEO"
        ],
        "Network & Developer Tools": [
            "API Management in Serverless Era", "6G Infrastructure Readiness", "Real-time Network Auditing",
            "DNS Lookup Security", "Tech Stack Analysis for 2026", "API Latency Reduction"
        ],
        "Gizlilik & Güvenlik": [
            "Post-Quantum Cryptographic Agility", "Deepfake Defense for Enterprises", "Browser Fingerprinting Protection",
            "Data Sovereignty in 2026", "Quantum-resistant VPN Protocols", "Anonymous Digital Identity"
        ]
    }

    # Rastgele bir kategori ve konu seçimi
    selected_cat = random.choice(list(categories.keys()))
    selected_topic = random.choice(categories[selected_cat])
    
    # Makale formatı çeşitliliği
    formats = ["Top 10 Tools for", "The Ultimate Guide to", "2026 Industry Report:", "How to Optimize", "Deep Dive Analysis:"]
    selected_format = random.choice(formats)

    # 2. GÜNCELLENMİŞ 2026 PROMPT
    prompt = f"""
    ROLE: You are a Senior Tech Analyst & Full-Stack Developer at DataSecureTools.com. 
    TASK: Write a UNIQUE, high-quality technical blog post in English.
    
    FOCUS: {selected_format} {selected_topic}
    CATEGORY: {selected_cat}

    1. STRUCTURE (STRICT):
    ---
    title: "[Catchy Technical Title]"
    description: "[150-char SEO summary focused on 2026 trends]"
    pubDate: {datetime.now().strftime('%Y-%m-%d')}
    author: "DataSecureTools Research Labs"
    tags: ["{selected_cat}", "2026-Trends", "Web-Analysis"]
    ---

    2. CONTENT RULES:
    - Start with '# [Title]'.
    - Mention 'DataSecureTools' in the first paragraph.
    - CONTENT DEPTH: Min 1200 words. Use H2 (##) and H3 (###).
    - INTEGRATION: Naturally link technical terms to DataSecureTools tools. 
      Example: If discussing page speed, mention /tools/speed-test. 
      Example: If discussing security, mention /tools/port-scanner or /tools/dns-lookup.
    
    3. 2026 TREND KEYWORDS (Sprinkle naturally):
    "Server-side rendering 2026", "Zero-latency APIs", "AI-driven search intent", "Data sovereignty", "Real-time network auditing".

    4. AUTHORITY SIGNATURE:
    End the post with: "This content was prepared by the DataSecure technical team and web analysts within the framework of 2026 digital standards."

    5. LANGUAGE: Advanced, Professional Technical English.
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a versatile technology expert. You solve real-world problems for WebMasters. You never repeat yourself."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 4000
    }

    try:
        print(f"🤖 Generating {selected_cat} report: {selected_topic}...")
        response = requests.post(API_URL, json=data, headers=headers, timeout=240)
        response.raise_for_status()
        
        content = response.json()['choices'][0]['message']['content']
        
        if content.startswith("```"):
            content = "\n".join(content.split("\n")[1:-1])

        title_match = re.search(r'title:\s*"(.*?)"', content)
        if title_match:
            filename = f"{slugify(title_match.group(1))}.md"
        else:
            filename = f"tech-report-{datetime.now().strftime('%Y%m%d%H%M')}.md"

        file_path = os.path.join(target_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
            
        print(f"✅ SUCCESS: {filename} published.")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    generate_automated_blog()