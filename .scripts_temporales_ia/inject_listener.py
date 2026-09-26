with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# We want to inject the FAQ listener inside the window.onload or DOMContentLoaded, or just at the end of the script before `</script></body>`
# Let's see if there is `window.onload`
if 'window.onload' in text:
    print('window.onload found!')

# Let's just find `</script>\n</body>`
text_new = text.replace('</script>\n</body>', """
    document.addEventListener('DOMContentLoaded', function() {
        const masterFaq = document.getElementById('masterFaq');
        if(masterFaq) {
            masterFaq.addEventListener('toggle', function() {
                if(this.open) {
                    setTimeout(() => {
                        this.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 100);
                }
            });
        }
    });
</script>\n</body>""")

if text_new != text:
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text_new)
    print("Injected toggle event via replace 1")
else:
    # Try another replace
    text_new = text.replace('</script>\n</html>', """
    document.addEventListener('DOMContentLoaded', function() {
        const masterFaq = document.getElementById('masterFaq');
        if(masterFaq) {
            masterFaq.addEventListener('toggle', function() {
                if(this.open) {
                    setTimeout(() => {
                        this.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 150);
                }
            });
        }
    });
</script>\n</html>""")
    if text_new != text:
        with open('v2.html', 'w', encoding='utf-8') as f:
            f.write(text_new)
        print("Injected toggle event via replace 2")
    else:
        print("Failed to inject.")
