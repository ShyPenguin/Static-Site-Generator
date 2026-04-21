import os
import shutil

def move_static(destination, copy_path):
    if not os.path.exists(destination):
        os.mkdir(destination)

    for filename in os.listdir(copy_path):
        from_path = os.path.join(copy_path, filename)
        dest_path = os.path.join(destination, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            move_static(from_path, dest_path)
    
def copy_files(destination, copy_path):
    abs_path = os.path.abspath(copy_path)
    dest_path = os.path.abspath(destination)
    if not os.path.exists(abs_path):
        raise Exception(f"{abs_path} does not exist")
    
    if os.path.isdir(abs_path):
        created_dest_path = os.path.normpath(os.path.join(dest_path, os.path.basename(copy_path)))
        os.mkdir(created_dest_path)
        content_dir = os.listdir(abs_path)
        for item in content_dir:
            copy_files(created_dest_path, f"{copy_path}/{item}")

    if os.path.isfile(abs_path):
        shutil.copy(abs_path, dest_path)
    return 

