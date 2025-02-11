import re

text = r"Test \abc/123\def!"
clean_text = re.sub(r"[^a-zA-ZåäöÅÄÖ0-9/\\]", "", text)

print(clean_text)  # Output: Test\abc/123\def
