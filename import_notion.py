'''
Run this script to import Notion note to handbook note

Author: minhdq99hp@gmail.com


Todo:
- Unzip file
- Read Markdown file
- Copy images file to folder assets
'''
import os
import re
import logging
from pathlib import Path
import zipfile
from datetime import datetime
import shutil

NOTION_DIR = 'notion_zip'

Path(NOTION_DIR).mkdir(parents=True, exist_ok=True)

IMAGE_ASSET_DIR = os.path.join('docs', 'assets', 'images')
POST_DIR = os.path.join('docs', '_posts')


if __name__ == '__main__':
    # find the zip file in notion_zip/
    zip_file_path = None

    for f in os.listdir(NOTION_DIR):
        if f.endswith('.zip'):
            zip_file_path = os.path.join(NOTION_DIR, f)
            print(f"[Notion archive]: {f}")
            break
    if not zip_file_path:
        logging.error("Found no Notion note archive to import ! (required=1)")
        exit(1)

    with zipfile.ZipFile(zip_file_path, 'r') as f:
        f.extractall(NOTION_DIR)
    

    # get the exported_image_dir
    exported_image_dir = None
    markdown_path = None
    default_title = None
    for f in os.listdir(NOTION_DIR):
        path = os.path.join(NOTION_DIR, f)
        if os.path.isdir(path):
            export_image_dir = path
            print(f"[Image directory]: {f}")
        if os.path.isfile(path) and f.lower().endswith(('.md', '.markdown')):
            markdown_path = path
            default_title = f
            print(f"[Markdown note]: {f}")
    
    if not markdown_path:
        logging.error("Found no Markdown file to import !");
        exit(1)
    
    default_title = default_title.split(' ')
    if len(default_title) > 1:
        default_title = ' '.join(default_title[:-1])
    
    print()



    # get title
    while True:
        if default_title:
            title = input(f"Enter your post title (default: {default_title}): ")
            
            if not title:
                title = default_title
                break
        else:
            title = input(f"Enter your post title: ")
            if len(title) > 0 and bool(re.match("^[A-Za-z0-9_-]*$", title)):
                break

    # get slug
    slug = title.replace(' ', '-').lower()
    ans = input(f"Here is your post slug: {slug}\nIt is ok for you ? <Y/n>: ")
    if not ans.lower() in ('', 'y', 'yes'):
        while True:
            slug = input("Enter your post slug: ")

            if len(slug) > 0 and bool(re.match("^[A-Za-z0-9_-]*$", slug)):
                break
    


    # create image_dir
    image_dir = os.path.join(IMAGE_ASSET_DIR, slug)
    Path(image_dir).mkdir(parents=True, exist_ok=True)

    # copy images to image_dir
    if exported_image_dir:
        for f in os.listdir(exported_image_dir):
            shutil.copy(os.path.join(export_image_dir, f), image_dir)



    # get markdown filename
    today = datetime.now()
    filename = f'{today.year}-{today.month:02}-{today.day}-{slug}.md'
    
    note_path = os.path.join(POST_DIR, filename)
    shutil.copy(markdown_path, note_path)


    # build header
    header = '---\n'
    header += f'title: "{title}"\n'

    # get category
    category = input("Enter category (default: Technology): ")

    if not category:
        category = 'Technology'
    
    header += f'categories: {category}\n'

    # get tags
    tags = input("Enter tags (comma-separate): ").strip()

    tags = tags.split(',')

    if len(tags) > 0 and tags[0] != '':
        header += 'tags:\n'

        for t in tags:
            header += f'    - {t.strip()}\n'

    header += 'toc: true\n'
    header += '---\n\n'

    with open(note_path, 'r+') as f:
        text = f.read()
        f.seek(0)
        f.write(header + text)
        f.truncate()

    print(f"\n[Output note]: {filename}")

    Path(markdown_path).unlink(missing_ok=True)
    Path(zip_file_path).unlink(missing_ok=True)

    if exported_image_dir:
        Path(exported_image_dir).rmdir()

    print("\nDone !")