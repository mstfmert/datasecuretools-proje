import os
import requests
import re
import random
from datetime import datetime

# API anahtarı GitHub Secrets'tan gelecek
API_KEY = os.getenv("DEEPSEEK_API_KEY")
# DÜZELTME: URL tertemiz hale getirildi, parantezler kaldırıldı.
API_URL = "https://api.deepseek.com/v1/chat/completions"

def slugify(text):
    """Başlığı URL dostu dosya ismine dönüştürür."""
    text = text.lower()
    # Türkçe ve özel karakter temizliği
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def generate_automated_blog():
    if not API_KEY:
        print("❌ ERROR: DEEPSEEK_API_KEY not found.")
        return

    target_dir = os.path.join(os.getcwd(), 'src', 'content', 'blog')
    os.makedirs(target_dir, exist_ok=True)

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

    selected_cat = random.choice(list(categories.keys()))
    selected_topic = random.choice(categories[selected_cat])
    formats = ["Top 10 Tools for", "The Ultimate Guide to", "2026 Industry Report:", "How to Optimize", "Deep Dive Analysis:"]
    selected_format = random.choice(formats)
    current_date = datetime.now().strftime('%Y-%m-%d')

    prompt = f"""
    ROLE: You are a Senior Tech Analyst & Full-Stack Developer at DataSecureTools.com. 
    TASK: Write a UNIQUE, high-quality technical blog post in English.
    
    IMPORTANT: You MUST start the file with the following YAML frontmatter exactly. 
    Do not use any markdown code blocks (```) around the frontmatter.

    ---
    title: "{selected_format} {selected_topic}"
    description: "Deep dive into {selected_topic} within the 2026 ecosystem. Learn how DataSecureTools is leading the next-gen web analysis."
    pubDate: {current_date}
    author: "DataSecureTools Research Labs"
    tags: ["{selected_cat}", "2026-Trends", "Web-Analysis"]
    ---

    1. CONTENT RULES:
    - Start with '# {selected_format} {selected_topic}'.
    - Mention 'DataSecureTools' in the first paragraph.
    - CONTENT DEPTH: Min 1200 words. Use H2 (##) and H3 (###).
    - INTEGRATION: Naturally link to /tools/speed-test, /tools/port-scanner, /tools/dns-lookup, or /tools/hide-ip.
    
    2. 2026 TREND KEYWORDS:
    "Server-side rendering 2026", "Zero-latency APIs", "AI-driven search intent", "Data sovereignty", "Real-time network auditing".

    3. AUTHORITY SIGNATURE:
    End with: "This content was prepared by the DataSecure technical team and web analysts within the framework of 2026 digital standards."
    """

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a versatile technology expert. You ALWAYS provide the YAML frontmatter at the top. Never wrap the entire response in markdown code blocks."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 4000
    }

    try:
        print(f"🤖 Generating {selected_cat} report: {selected_topic}...")
        response = requests.post(API_URL, json=data, headers=headers, timeout=240)
        response.raise_for_status()
        
        content = response.json()['choices'][0]['message']['content'].strip()
        
        # DÜZELTME: Markdown blok temizliğini daha güvenli hale getirdik
        if content.startswith("```"):
            content = re.sub(r'^```[a-z]*\n', '', content, flags=re.MULTILINE)
            content = re.sub(r'\n```$', '', content, flags=re.MULTILINE)

        # Slugify tabanlı dosya adı belirleme
        title_match = re.search(r'title:\s*"(.*?)"', content)
        if title_match:
            filename = f"{slugify(title_match.group(1))}.md"
        else:
            filename = f"report-{datetime.now().strftime('%Y%m%d%H%M')}.md"

        file_path = os.path.join(target_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ SUCCESS: {filename} published.")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    generate_automated_blog()