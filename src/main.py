from move_static import move_static
from page import generate_pages_recursive

def main():
    move_static("public", "static")
    generate_pages_recursive("content", "template.html", "public")
main()