from converters import markdown_to_html_node
import os


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No header found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file = open(from_path)
    file_contents = file.read()
    file.close()
    template = open(template_path)
    template_contents = template.read()
    template.close()
    content = markdown_to_html_node(file_contents).to_html()
    title = extract_title(file_contents)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    new_file = open(dest_path, 'x')
    new_file.write(template_contents.replace("{{ Title }}", title).replace("{{ Content }}", content))
    new_file.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for path in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, path)
        if not os.path.isfile(path):
            generate_pages_recursive(path, template_path, dest_dir_path)
        elif path.endswith(".md"):
            dest_path = os.path.join(dest_dir_path, os.path.relpath(path, "content"))
            generate_page(path, template_path, dest_path.replace(".md", ".html"))
