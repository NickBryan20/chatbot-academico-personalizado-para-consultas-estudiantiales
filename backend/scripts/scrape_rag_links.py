import os
import re
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse

def extract_urls(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # Simple regex for http/https URLs
    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text)
    return [url.rstrip(').,]') for url in urls]

def is_valid_url(url):
    allowed_domains = ('pucesi.edu.ec', 'puce.edu.ec')
    excluded_domains = [
        'youtube.com', 'facebook.com', 'instagram.com', 
        'linkedin.com', 'tiktok.com', 'x.com', 'flickr.com',
        'twitter.com', 'wa.me'
    ]
    excluded_extensions = ['.pdf', '.jpg', '.png', '.jpeg', '.gif', '.mp4']
    netloc = urlparse(url if url.startswith('http') else f'https://{url}').netloc.lower()

    if not any(netloc == domain or netloc.endswith(f'.{domain}') for domain in allowed_domains):
        return False
    
    for domain in excluded_domains:
        if domain in netloc:
            return False
            
    for ext in excluded_extensions:
        if url.lower().endswith(ext):
            return False
            
    return True

def scrape_url(url):
    try:
        print(f"Scraping: {url}", flush=True)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()
            
        # Get text
        text = soup.get_text(separator='\n')
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_file = os.path.join(base_dir, 'documents', 'puce_ibarra_info.txt')
    output_file = os.path.join(base_dir, 'documents', 'scraped_web_content.txt')
    
    urls = extract_urls(source_file)
    # Remove duplicates
    urls = list(set(urls))
    
    valid_urls = [url for url in urls if is_valid_url(url)]
    print(f"Se encontraron {len(valid_urls)} URLs válidas para procesar.")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# CONTENIDO EXTRAÍDO AUTOMÁTICAMENTE DE LA WEB (RAG SCRAPING)\n\n")
        
        for url in valid_urls:
            content = scrape_url(url)
            if content:
                f.write(f"\n--- INICIO CONTENIDO DE: {url} ---\n")
                f.write(content)
                f.write(f"\n--- FIN CONTENIDO DE: {url} ---\n\n")
            time.sleep(1) # Polite delay
            
    print(f"\n✅ Proceso completado. Contenido guardado en {output_file}")

if __name__ == '__main__':
    main()
