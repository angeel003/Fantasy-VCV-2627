with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
    start = text.find("action: 'login_guest'")
    end = text.find("if(finalHtml === \"\")")
    if start != -1 and end != -1: 
        print(text[start+500:end].encode('ascii', 'ignore').decode('ascii'))
