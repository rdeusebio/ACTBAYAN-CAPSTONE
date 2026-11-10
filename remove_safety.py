import os
import re

base_dir = r"c:\Users\FERDINAND JR\Downloads\Coding Projects\August Revisions\OCTOBER\ACTBAYAN-CAPSTONE-main\ACTBAYAN-CAPSTONE-main\templates"

files = {
    "lgu_map.html": [
        (r"\s*\{\s*cat:\s*'safety'[^}]+\},", ""),
        (r"\s*\{\s*id:\s*'safety'[^}]+\},", "")
    ],
    "barangay_map.html": [
        (r"\s*\{\s*cat:\s*'safety'[^}]+\},", ""),
        (r"\s*\{\s*id:\s*'safety'[^}]+\},", "")
    ],
    "lgu_announcements.html": [
        (r"\s*<option\s+value=\"Safety\">.*?</option>", ""),
        (r"\{%\s*elif\s+cat\s*==\s*'Safety'\s*%\}\{%\s*set\s+emoji\s*=\s*'🚨'\s*%\}", "")
    ],
    "lgu.html": [
        (r"\s*<button\s+class=\"chip\"\s+data-filter=\"safety\">Safety</button>", ""),
        (r"\s*<div\s+class=\"modal-cat-tile\"\s+data-cat=\"Safety\"[^>]*>\s*<span[^>]*>[^<]*</span>\s*<div[^>]*>Safety</div>\s*<div[^>]*>[^<]*</div>\s*</div>", ""),
        (r",\s*Safety:\s*'🚨'", "")
    ],
    "file_concern.html": [
        (r"\s*<button\s+class=\"chip\"\s+data-filter=\"safety\">Safety</button>", ""),
        (r"\s*<div\s+class=\"modal-cat-tile\"\s+data-cat=\"Safety\"[^>]*>\s*<span[^>]*>[^<]*</span>\s*<div[^>]*>Safety</div>\s*<div[^>]*>[^<]*</div>\s*</div>", ""),
        (r",\s*Safety:\s*'🚨'", "")
    ],
    "dashboard.html": [
        (r"\s*<div\s+class=\"modal-cat-tile\"\s+data-cat=\"Safety\"[^>]*>\s*<span[^>]*>[^<]*</span>\s*<div[^>]*>Safety</div>\s*<div[^>]*>[^<]*</div>\s*</div>", ""),
        (r",\s*Safety:\s*'🚨'", "")
    ],
    "index.html": [
        (r"\s*<span\s+class=\"filter-pill\"\s+onclick=\"filterBulletins\('safety',\s*this\)\">[^<]+</span>", "")
    ],
    "announcements.html": [
        (r"\s*<button\s+class=\"filter-chip\"\s+onclick=\"filterAnn\('safety',\s*this\)\">[^<]+Safety</button>", "")
    ]
}

for file_name, patterns in files.items():
    file_path = os.path.join(base_dir, file_name)
    if not os.path.exists(file_path):
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    for pattern, repl in patterns:
        content = re.sub(pattern, repl, content)
        
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file_name}")
