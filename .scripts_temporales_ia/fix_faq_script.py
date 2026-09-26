with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_script = """    // Add FAQ scroll behavior on load
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
    });"""

new_script = """    // Add FAQ scroll behavior directly
    (function() {
        const masterFaq = document.getElementById('masterFaq');
        if(masterFaq) {
            masterFaq.addEventListener('toggle', function(e) {
                if(this.open) {
                    setTimeout(() => {
                        this.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        // Also try scrolling window directly in case scrollIntoView fails on some mobile browsers
                        // const rect = this.getBoundingClientRect();
                        // const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                        // window.scrollTo({ top: rect.top + scrollTop - 60, behavior: 'smooth' });
                    }, 150);
                }
            });
            // Fallback for summary click
            const summary = masterFaq.querySelector('summary');
            if(summary) {
                summary.addEventListener('click', function() {
                    if(!masterFaq.open) {
                        setTimeout(() => {
                            masterFaq.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }, 150);
                    }
                });
            }
        }
    })();"""

if old_script in text:
    text = text.replace(old_script, new_script)
else:
    print("Warning: old_script not found")

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed FAQ script')
