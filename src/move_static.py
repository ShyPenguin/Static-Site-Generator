import os
import shutil

def move_static(destination, copy_path):
        try:
            dest_dir_abs = os.path.abspath(destination)
            if os.path.exists(dest_dir_abs):
                shutil.rmtree(dest_dir_abs)
            
            if not os.path.exists(dest_dir_abs):
                os.mkdir(dest_dir_abs)

            abs_path = os.path.abspath(copy_path)
            if os.path.exists(abs_path) and os.path.isdir(abs_path):
                items = os.listdir(abs_path)
                for item in items:
                    copy_files(destination, f"{copy_path}/{item}")
        except Exception as e:
            print(f"Something went wrong: {e}")
    
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

