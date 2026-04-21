import os
from block_markdown import extract_title, markdown_to_html_node

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            if from_path[-3:] != '.md':
                continue
            generate_page(from_path, template_path, f"{dest_path[:-3]}.html")
        else:
            generate_pages_recursive(from_path, template_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    from_file = read_file(from_path)
    template_file = read_file(template_path)
    html_nodes = markdown_to_html_node(from_file.strip())

    html_string = html_nodes.to_html()
    title = extract_title(html_string)

    dest_content = template_file.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    write_file(dest_path, dest_content)

def read_file(path):
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        raise Exception(f"File does not exists {abs_path}")
    file = None
    with open(abs_path, "r") as f:
        file = f.read()
    return file

def write_file(file_path, content):
    try :
        abs_path = os.path.abspath(file_path)
        if os.path.isdir(abs_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)

        with open(abs_path, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"