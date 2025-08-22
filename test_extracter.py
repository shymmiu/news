#!/usr/bin/env python3
import extracter

# Test without reading HTML file first
print("Testing extract_urls function...")
test_html = '<a href="https://www.eldiariomontanes.es/cantabria/test-nt.html">test</a>'
result = extracter.extract_urls(test_html)
print(f"Result: {result}")
print("Done!")
