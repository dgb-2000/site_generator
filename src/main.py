import os
import shutil
from page_generator import generate_pages_recursive


def copy_static(dir):
    if os.path.exists(dir):
        for item in os.listdir(dir):
            path = os.path.join(dir, item)
            new_dir = ""
            if "/" in dir:
                new_dir = os.path.join("public", dir.split("/", 1)[1])
            else:
                new_dir = "public"
            if os.path.isfile(path):
                if not os.path.exists(new_dir):
                    os.mkdir(new_dir)
                shutil.copy(path, os.path.join(new_dir, item))
            else:
                if not os.path.exists(new_dir):
                    os.mkdir(new_dir)
                copy_static(path)


def main():
    shutil.rmtree("public")
    os.mkdir("public")
    copy_static("static")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
