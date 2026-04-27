import logging
from md_blocks import markdown_to_blocks, markdown_to_html_node
import os, shutil, logging, sys

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


def generate_page(from_path, template_path, dest_path, basepath):
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
        template = template.replace('href="/', f'href="{basepath}')
        template = template.replace('src="/', f'src="{basepath}')
        directory = os.path.dirname(dest_path)
        os.makedirs(directory, exist_ok=True)
        with open(dest_path, 'w') as f:
            f.write(template)
    except Exception as e:
        print(f"Error occured :{e}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.exists(dir_path_content):
        try:
            for filename in os.listdir(dir_path_content):
                content_path = os.path.join(dir_path_content, filename)
                logger.info(content_path)
                try:
                    if os.path.isdir(content_path):
                        new_dest_dir = os.path.join(dest_dir_path, filename)
                        os.mkdir(new_dest_dir)
                        generate_pages_recursive(content_path, template_path, new_dest_dir, basepath)
                    elif os.path.isfile(content_path):
                        if content_path.endswith(".md"):
                            generate_page(content_path, template_path, dest_dir_path+"/index.html", basepath)
                except Exception as e:
                    print(f"Failed to generate file: {e}")
        except Exception as e:
            print(f"{dir_path_content} not exist: {e}")



def main():
    logging.basicConfig(filename='log_file', level=logging.INFO)
    src = "../static"
    dst = "../docs"
    copy_content(src, dst)  
    basepath =  sys.argv[1] if len(sys.argv) > 1 else "/"
    from_path, tmp_path = "../content", "../template.html"
    generate_pages_recursive(from_path, tmp_path, dst, basepath)




if __name__ == "__main__":
    main()
