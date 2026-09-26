import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's insert a @media query right before the closing </style> tag.
media_query = r"""
    /* MOBILE RESPONSIVENESS */
    @media (max-width: 600px) {
        .form-container {
            padding: 15px !important;
            border-radius: 0px !important; /* maybe 0px or small radius if it takes full width? */
            border-left: none !important;
            border-right: none !important;
        }
        body {
            padding-left: 0px !important;
            padding-right: 0px !important;
        }
        .vcv-card-v2 {
            padding: 12px;
            border-radius: 12px;
        }
    }
</style>"""

text = text.replace('</style>', media_query)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Media query added to v2.html")
