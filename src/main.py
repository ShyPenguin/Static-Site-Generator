from move_static import move_static
from page import generate_pages_recursive
import sys

def main():
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    generated_dir = "docs" 
    move_static(generated_dir, "static")
    generate_pages_recursive("content", "template.html", generated_dir, base_path)
main()