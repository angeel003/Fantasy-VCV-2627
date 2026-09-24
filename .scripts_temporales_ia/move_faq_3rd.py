import re

def update_html(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update the APK download link
    html = html.replace('href="files/app/fantasy-vcv.apk"', 'href="files/app/fantasy-vcv-2627.apk"')

    # 2. Extract the app install <details> block
    # It starts with <details class="faq-details"> \n <summary class="faq-summary">📱 Cómo instalar la App (Android / iOS)</summary>
    app_block_regex = r'(\s*<details class="faq-details">\s*<summary class="faq-summary">📱 Cómo instalar la App \(Android / iOS\)</summary>.*?</details>)'
    
    match = re.search(app_block_regex, html, flags=re.DOTALL)
    if not match:
        print(f"Could not find app block in {filename}")
        return
        
    app_block = match.group(1)
    
    # Remove it from its current position
    html = html.replace(app_block, '')

    # Now, find the 2nd FAQ <details> block to insert the app block after it
    # We will split the HTML by <details class="faq-details">
    # Wait, splitting by <details might be tricky. Let's use a regex to match the first two details blocks.
    
    faq_details_pattern = r'(<details class="faq-details">.*?</details>)'
    # Find all details in the faq-container (after faq-title)
    # Actually, we can just find the first two details globally in the faq-container
    
    faq_start_idx = html.find('<div class="faq-title">')
    if faq_start_idx == -1:
        # maybe emoji
        faq_start_idx = html.find('Preguntas Frecuentes y Gesti')
        
    # Let's find all <details class="faq-details"> after faq_start_idx
    details_matches = list(re.finditer(faq_details_pattern, html[faq_start_idx:], flags=re.DOTALL))
    
    if len(details_matches) >= 2:
        # Insert after the second details block
        insert_pos = faq_start_idx + details_matches[1].end()
        html = html[:insert_pos] + app_block + html[insert_pos:]
    else:
        # If there are fewer than 2, just append it
        html += app_block

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
        print(f"Updated {filename}")

update_html('dev.html')
update_html('index.html')

