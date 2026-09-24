import re

with open('dev.html', 'r', encoding='utf-8') as f:
    dev = f.read()

dev_url = 'https://script.google.com/macros/s/AKfycbzM7QuqH1yFRL9rSA7CAUHZX3cogU6AH3PAW36mQkWhMw2ZDnA3JhI-U2bC7TQyNOHz/exec'
prod_url = 'https://script.google.com/macros/s/AKfycbyw9L6Te3q2ibdRBaaAwaiPpEPWLbsNdb8JA9yO272DBHgxaZA2l3TLkH9ofAXlQiWfAg/exec'

prod = dev.replace(dev_url, prod_url)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(prod)
    
print("Synced dev.html to index.html with prod URL preserved.")

