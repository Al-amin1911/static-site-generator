import logging
import shutil
from textnode import TextNode, TextType, textnode_to_htmlnode, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode
from md_blocks import markdown_to_blocks, markdown_to_html_node
import os, shutil, logging

logger = logging.getLogger(__name__)

def copy_content(source_path:str, destination_path:str):
    # delete content of destination directory "public"
    if os.path.exists(destination_path):
        try:
            shutil.rmtree(destination_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
    os.mkdir(destination_path)
    # copy all files , subdirectories and nested files form "static"
    if os.path.exists(source_path):
        for filename in os.listdir(source_path):
            logger.info(filename)
            file_path = os.path.join(source_path, filename)
            logger.info(file_path)
            try:
                if os.path.isdir(file_path):
                    new_dst = os.path.join(destination_path, filename)
                    os.mkdir(new_dst)
                    copy_content(file_path, new_dst)
                elif os.path.isfile(file_path) or os.path.islink(file_path):
                    shutil.copy(file_path, destination_path)
            except Exception as e:
                print(f"Failed to copy {file_path}, Reason: {e}")

def extract_title(markdown):
    try:
        blocks = markdown_to_blocks(markdown)
        if blocks[0].startswith("# "):
            title = blocks[0][2:]
            return title
    except Exception as e:
        print(f"Error occured {e}")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    try:
        with open(from_path) as f:
            markdown = f.read()
        with open(template_path) as f:
            template = f.read()
        html_str = markdown_to_html_node(markdown).to_html()
        title = extract_title(markdown)
        template = template.replace('{{ Title }}', title)
        template = template.replace('{{ Content }}', html_str)
        directory = os.path.dirname(dest_path)
        os.makedirs(directory, exist_ok=True)
        with open(dest_path, 'w') as f:
            f.write(template)
    except Exception as e:
        print(f"Error occured :{e}")

def main():
    logging.basicConfig(filename='log_file', level=logging.INFO)
    src = '/home/alamin/static-site-generator/static'
    dst = '/home/alamin/static-site-generator/public'
    copy_content(src, dst)
    from_path, tmp_path, dst_path = "/home/alamin/static-site-generator/content/index.md", "/home/alamin/static-site-generator/template.html", "/home/alamin/static-site-generator/public/index.html"
    generate_page(from_path, tmp_path, dst_path)




if __name__ == "__main__":
    main()
