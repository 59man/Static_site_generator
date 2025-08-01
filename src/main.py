from textnode import TextNode, TextType
import os
import shutil
from pathlib import Path
from Inline_markdown import markdown_to_blocks,split_nodes_link,split_nodes_image,split_nodes_delimiter,text_to_textnodes
from Block_type import markdown_to_html_node


def copy_static_files(source: str, destination: str):
    # Step 1: Delete the destination directory if it exists
    if os.path.exists(destination):
        shutil.rmtree(destination)
        print(f"Deleted existing directory: {destination}")

    # Step 2: Recreate the destination directory
    os.makedirs(destination, exist_ok=True)
    print(f"Created new directory: {destination}")

    # Step 3: Recursively copy files
    def recursive_copy(src, dst):
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dst_path = os.path.join(dst, item)

            if os.path.isdir(src_path):
                os.makedirs(dst_path, exist_ok=True)
                recursive_copy(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
                print(f"Copied file: {src_path} ➜ {dst_path}")

    recursive_copy(source, destination)

def generate_page(from_path, template_path, dest_path):
    print(f" * Generating page: {from_path} -> {dest_path}")
    with open(from_path, "r", encoding="utf-8") as from_file:
        markdown_content = from_file.read()

    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()

    try:
        title = extract_title(markdown_content)
        print(f"   Extracted title: {title}")
    except ValueError:
        print(f"   Warning: No H1 title found in {from_path}, using 'Untitled Page'")
        title = "Untitled Page"

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as to_file:
        to_file.write(template)

def extract_title(md):
    lines = md.splitlines()
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    print(f"Warning: No H1 title found, using 'Untitled Page'")
    return "Untitled Page"



def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating pages from: {dir_path_content}")
    for root, dirs, files in os.walk(dir_path_content):
        for file_name in files:
            if file_name.endswith(".md"):
                from_path = os.path.join(root, file_name)
                rel_path = os.path.relpath(from_path, dir_path_content)
                rel_path_html = os.path.splitext(rel_path)[0] + ".html"
                dest_path = os.path.join(dest_dir_path, rel_path_html)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                print(f"Generating page from {from_path} to {dest_path}")
                generate_page(from_path, template_path, dest_path)



def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

if __name__ == "__main__":
    main()
