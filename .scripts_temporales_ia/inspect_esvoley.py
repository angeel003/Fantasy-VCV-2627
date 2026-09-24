import urllib.request
import re
import json

urls = [
    'https://esvoley.es/voleibol/competiciones-masculinas/superliga-masculina-2/grupo-c',
    'https://esvoley.es/voleibol/competiciones-masculinas/primera-division-masculina/grupo-a',
    'https://esvoley.es/voleibol/competiciones-femeninas/primera-division-femenina/grupo-d'
]

for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    
    print(f"--- Analyzing {url} ---")
    
    # Look for API calls or JSON paths
    api_paths = re.findall(r'[\'"](/api/[^\'"]+)[\'"]', html)
    print("API Paths:", set(api_paths))
    
    json_paths = re.findall(r'[\'"](/[^\'"]+\.json[^\'"]*)[\'"]', html)
    print("JSON Paths:", set(json_paths))
    
    # Sometimes it's hardcoded as a variable in a script tag
    script_vars = re.findall(r'const\s+\w+\s*=\s*(".*api.*"|\'.*api.*\');', html)
    print("Script Vars:", set(script_vars))

    # Print the first script block that has data-related variables
    scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
    for s in scripts:
        if 'fetch(' in s or '$.ajax' in s or 'axios' in s:
            print("Fetch script found. Length:", len(s))
            print(s[:500])

