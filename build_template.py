import os
import re

def compile_standalone_html():
    template_path = "app/templates/index.html"
    static_dir = "app/static"

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Could not find {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Inline CSS files
    def replace_css(match):
        css_file = match.group(1).replace("/static/", "").replace("static/", "")
        file_path = os.path.join(static_dir, css_file)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f"<style>\n{f.read()}\n</style>"
        return match.group(0)

    # Inline JS files
    def replace_js(match):
        js_file = match.group(1).replace("/static/", "").replace("static/", "")
        file_path = os.path.join(static_dir, js_file)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f"<script>\n{f.read()}\n</script>"
        return match.group(0)

    # Replace <link rel="stylesheet" href="/static/..."> tags
    html = re.sub(r'<link[^>]+href=["\']([^"\']+\.css)["\'][^>]*>', replace_css, html)
    
    # Replace <script src="/static/..."></script> tags
    html = re.sub(r'<script[^>]+src=["\']([^"\']+\.js)["\'][^>]*></script>', replace_js, html)

    return html

if __name__ == "__main__":
    compiled = compile_standalone_html()
    os.makedirs("app/static_compiled", exist_ok=True)
    with open("app/static_compiled/standalone_demo.html", "w", encoding="utf-8") as f:
        f.write(compiled)
    print("Successfully built standalone HTML bundle!")