with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

injection = """
    // Add FAQ scroll behavior on load
    document.addEventListener('DOMContentLoaded', function() {
        const masterFaq = document.getElementById('masterFaq');
        if(masterFaq) {
            masterFaq.addEventListener('toggle', function(e) {
                if(this.open) {
                    setTimeout(() => {
                        this.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 150);
                }
            });
        }
    });
</script>
"""

start = text.rfind('</script>')
if start != -1:
    text = text[:start] + injection + text[start+9:]
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Injected FAQ listener successfully.")
else:
    print("Could not find </script>")
