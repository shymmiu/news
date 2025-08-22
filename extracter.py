import re

def extract_urls(text):
    if not text:
        return None
    
    extracted_urls = []
    
    # Use regex to find all URLs that match the pattern
    url_pattern = r'https://[^\s"<>]+\.html'
    
    for line in text.splitlines():
        if "-nt" in line:
            # Find all URLs in this line that match our pattern
            urls_in_line = re.findall(url_pattern, line)
            extracted_urls.extend(urls_in_line)
    
    # Filter to only include URLs with 'nt' but not 'ntrc'
    nt_only_urls = []
    seen = set()
    
    for url in extracted_urls:
        if url not in seen and "-nt" in url and "-ntrc" not in url:
            nt_only_urls.append(url)
            seen.add(url)
    
    return nt_only_urls

def extract_category(url):
    if 'www.eldiariomontanes.es' in url:
        position = url.find('.es/')
        if position != -1:
            if url[position + 4:].startswith('region/'):
                return url[position + 4:].split('/')[0] + ',' + url[position + 4:].split('/')[1]
            else:
                return url[position + 4:].split('/')[0]
    return None
