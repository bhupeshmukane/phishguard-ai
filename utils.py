import re
import tldextract

def highlight_text(text):
    words = ["urgent","bank","verify","otp","password","click"]
    highlighted = text
    for w in words:
        highlighted = re.sub(
            w,
            f"**:red[{w}]**",
            highlighted,
            flags=re.IGNORECASE
        )
    return highlighted

def url_risk(url):
    score = 0
    reasons = []

    if "@" in url:
        score += 20
        reasons.append("Uses @ symbol")

    if "-" in url:
        score += 10
        reasons.append("Hyphenated domain")

    if len(url) > 60:
        score += 10
        reasons.append("Long URL")

    domain = tldextract.extract(url).domain
    if domain.isnumeric():
        score += 20
        reasons.append("Numeric domain")

    return score, reasons
