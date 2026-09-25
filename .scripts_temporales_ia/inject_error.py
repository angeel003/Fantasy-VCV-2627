with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Inject an error catcher at the very top of <head>
error_catcher = """
<script>
window.onerror = function(message, source, lineno, colno, error) {
    alert('JS Error: ' + message + ' at ' + lineno + ':' + colno);
};
</script>
"""

text = text.replace('<head>', '<head>' + error_catcher)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
