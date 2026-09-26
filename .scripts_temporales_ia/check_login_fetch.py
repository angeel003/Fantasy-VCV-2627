import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'document\.getElementById\(\'btnLogin\'\)\.addEventListener\(.*?fetchSeguro', text, re.DOTALL)
if match:
    sys.stdout.buffer.write(text[max(0, match.end()-50):min(len(text), match.end()+150)].encode('utf-8'))
