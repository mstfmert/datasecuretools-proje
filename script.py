import os
import requests
from datetime import datetime

# GÜVENLİK: API anahtarı artık kodun içinde değil, sistem değişkenlerinden çekiliyor.
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_automated_blog():
    if not API_KEY:
        print("❌ HATA: DEEPSEEK_API_KEY bulunamadı. Lütfen GitHub Secrets veya Environment Variables kontrol edin.")
        return

    target_dir = os.path.join(os.getcwd(), 'src', 'content', 'blog')
    os.makedirs(target_dir, exist_ok=True)

    # 1000+ Kelime, İngilizce, SEO ve Trend Odaklı Prompt
    prompt = """
    Write a comprehensive, SEO-optimized English blog post about a trending technology topic (AI, Cybersecurity, Web3, or Cloud Computing) as of March 2026.
    
    REQUIREMENTS:
    1. LENGTH: Minimum 1200 words.
    2. FORMAT: Start exactly with this Astro-compatible frontmatter:
    ---
    title: "[SEO Optimized Title]"
    description: "[Engaging 150-character SEO description]"
    pubDate: "{date}"
    author: "Mustafa Mert"
    tags: ["tech", "ai", "innovation"]
    ---
    
    3. STRUCTURE: Use H2, H3 subheadings, bullet points, and bold key terms.
    4. CONTENT: Deep-dive analysis of current global tech trends.
    5. LANGUAGE: Professional and fluent English.
    """.format(date=datetime.now().strftime('%Y-%m-%d'))

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are an expert tech journalist and SEO specialist writing long-form content for Astro.build sites."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 4000
    }

    try:
        print("🤖 DeepSeek is crafting a 1000+ word masterpiece...")
        response = requests.post(API_URL, json=data, headers=headers, timeout=180)
        response.raise_for_status()
        
        content = response.json()['choices'][0]['message']['content']
        
        # Benzersiz dosya ismi (Saat-Dakika-Saniye dahil)
        filename = f"blog-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        file_path = os.path.join(target_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ SUCCESS: {filename} created successfully.")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    generate_automated_blog()