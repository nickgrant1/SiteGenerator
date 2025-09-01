import os, shutil, re
from blocks import markdown_to_html_node
from htmlnode import *

def main():
    copy_contents('static', 'public')
    generate_pages_recursive('content', 'template.html', 'public')

def copy_contents(src, dest):
    cwd = os.getcwd()
    source = os.path.join(cwd, src)
    destination = os.path.join(cwd, dest)

    if os.path.exists(destination):
        shutil.rmtree(destination)   #clean folder
    os.mkdir(destination)
    copy(source, destination)


def copy(src, dest):
    for thing in os.listdir(src):
        src_path = os.path.join(src, thing)
        dest_path = os.path.join(dest, thing)
        if os.path.isdir(src_path):
            os.mkdir(dest_path)
            copy(src_path, dest_path)
        else:
            shutil.copy(src_path, dest_path)


def extract_title(markdown):
    if bool(re.match(r"# .*?", markdown)):
        lines = markdown.splitlines()
        return lines[0][2:].strip()
    else:
        raise Exception('Missing Title')

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    cwd = os.getcwd()
    content_path = os.path.join(cwd, dir_path_content)

    for thing in os.listdir(content_path):
        path = os.path.join(content_path, thing)
        if os.path.isdir(path):
            new_dest_dir_path = os.path.relpath(path, cwd)
            new_dest_dir_path = path.replace('content', 'public')
            generate_pages_recursive(os.path.relpath(path, cwd), template_path, dest_dir_path)
        elif thing[-3:] == '.md':
            dest = path.replace("content", 'public').replace('.md', '.html')
            dest = os.path.relpath(dest, cwd)
            generate_page(os.path.relpath(path, cwd), template_path, dest)
        else:
            continue


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    cwd = os.getcwd()
    with open(os.path.join(cwd, from_path), "r") as md:
        content = md.read()
    with open(os.path.join(template_path), "r") as temp:
        template = temp.read()
    html_node = markdown_to_html_node(content)
    html = html_node.to_html()
    title = extract_title(content)
    htmlPage = template.replace('{{ Title }}', title).replace('{{ Content }}', html)
    
    destination = os.path.join(cwd, dest_path)
    if not os.path.exists(destination):
        target_parts = dest_path.split('/')
        i=1
        path = os.path.join(cwd, target_parts[0])
        while i<len(target_parts):    #make subdirectories
            if not os.path.exists(path):
                os.mkdir(path)
            path = os.path.join(path, target_parts[i])
            i+=1
        if path != destination:
            raise ValueError('Failure generating page')
    with open(destination, "w+") as dest:
        dest.write(htmlPage)



if __name__ == "__main__":
    main()
