"""
metada needed for blog posts
don't put value in quotes
date - eg: Month day, Year (by default current date)
time - time required to complete - eg: 3 min (by default 0 min )
title - title of the post (by default file name without extension)
tags - tags related to the post (by default ... )
permalink - name shows in the url link and
    template file saves the post in that name
    (by default file name without extendsion)
image - image name with extension - to show in home page

Save the image name for project directories same as the dir name
"""

import os
from datetime import datetime
import collections
import re

import markdown2
import jinja2
import yaml

"""
Currently 2 modes are available: dark and lite
by default : dark
"""
MODE = "dark"

# for personal details
favicon = False
with open('info.yaml') as f:
    info = yaml.safe_load(f)
    if info['favicon']:
        favicon = True

# POSTS dict to store blog posts from the directory posts
POSTS = {}
# Loop through all the markdown files from posts directory
for markdown_post in os.listdir('_posts'):
    file_path = os.path.join('_posts', markdown_post)
    with open(file_path, 'r') as f:
        # extras = ['metadata'] gives a dict of metadata
        # that we provided at the begining of the markdown file.
        POSTS[markdown_post] = \
            markdown2.markdown(f.read(), extras=['metadata',
                                                 'fenced-code-blocks',
                                                 'code-color'])
        # POSTS dict -
        # key : markdown_post, ie file name
        # value: content (string format html)
        # POSTS['markdown_post'].metadata gives a dict of metadata
    # DEFAULT DATA FOR POSTS
        # date (Current date) if date is not given in the post
        # strftime returns the string representation of date.
        POSTS[markdown_post].metadata.setdefault(
            'date', datetime.today().strftime('%B %d, %Y'))
        # title -if title is not given use filename without extension
        POSTS[markdown_post].metadata.setdefault(
            'title', markdown_post[:-3].title())
        # permalink -if permalink is not given use filename without extension
        POSTS[markdown_post].metadata.setdefault(
            'permalink', markdown_post[:-3])
        # tags - if tags are not give put ...
        POSTS[markdown_post].metadata.setdefault(
            'tags', '...')
        # time - if time is not give use 0 min
        POSTS[markdown_post].metadata.setdefault(
            'time', '0 min')

# Sort the markdown_post w.r.t time
# strptime is used to convert string date to date format
POSTS = {
    # key: value for key in sorted posts
    post: POSTS[post] for post in sorted(
        POSTS, key=lambda post: datetime.strptime(
            POSTS[post].metadata['date'], '%B %d, %Y'),
        reverse=True)
}

env = jinja2.Environment(loader=jinja2.PackageLoader('main', '_templates'))
# PackageLoader -
# 1st arg - name of python file
# 2nd arg - directory name where template files are located
index_template = env.get_template('index.html')
post_template = env.get_template('post.html')
blog_template = env.get_template('blog.html')

# Create a file_data dict to pass details about file in each page.
# file_data contains mode, page title,
# filePath (dir name) for permalink and assetPath
file_data = {"mode": MODE}

# HOME PAGE
# Pass metadata to index.html page
posts_metadata = [POSTS[post].metadata for post in POSTS]
file_data["pageTitle"] = "Home"
file_data["filePath"] = "posts"
file_data["assetPath"] = "."
# posts_metadata is a list, so we can't access posts.mode in index.html
index_html = index_template.render(posts=posts_metadata, info=info,
                                   file_data=file_data)
# This will pass a list of metadata through the
# variable posts to our index.html page template
# Create _site dir if not exists
os.makedirs('_site', exist_ok=True)
with open('_site/index.html', 'w') as f:
    f.write(index_html)

# BLOG PAGE
# metadata_date: key - date and value list of posts
metadata_date = collections.defaultdict(list)
for post in posts_metadata:
    year = datetime.strptime(post['date'], '%B %d, %Y').year
    metadata_date[year].append(post)
blog_html = blog_template.render(posts=metadata_date, mode=MODE, info=info)
# we already created _site dir for index.html file
with open('_site/blog.html', 'w') as f:
    f.write(blog_html)

# PROJECTS PAGE
# Create project categories w.r.t the directories inside the_projects dir.
# save the image name for directories same as the directory name

# In this section we  deal with 3 types of files.
# 1. main Projects page - contents are directories inside the _projects dir.
# we have to add metadata manually, that are title, image name, and permalink
# permalink is needed otherwise we have to edit index.html template.
# we also need to create pages for the contents inside this project categories.
# 2. markdown files directly inside the _project file
# we use PROJECTS_DIR dict for this.
# 3. markdown files inside the directory inside the _project directory.
# we use PROJECTS dict for it

# dir_metadata collect the data for main Project page - list of dictionaries.
# contents in the project page are directories,
# so we have to add data manually.
dir_metadata = []

# To get the extension of the image of directories inside _project dir.
# image name should be same as that of the directory name
assets_dir = {os.path.splitext(path)[0]: os.path.splitext(path)[1] for path in os.listdir("assets/projects")}

# PROJECT_DIR dict is to store the markdown file directly inside the _projects.
PROJECTS_DIR = {}
for project in os.listdir("_projects"):
    project_dict = {}
    # title is the directory name
    project_dict["title"] = project.title()
    file_path = os.path.join("_projects", project)
    if os.path.isdir(file_path):
        # if it's not dir, image name and permalink should pass
        # with the mardown file or we can add it in default section.
        project_dict["permalink"] = project
        if project in assets_dir:
            project_dict["image"] = project + assets_dir[project]

        # parse markdown files inside the directories in the _project folder
        # PROJECTS dict is to store the markdown files
        # inside the directories inside the _projects dir.
        PROJECTS = {}
        # Check whether the directory is empty or not
        directories = os.listdir(file_path)
        for markdown_post in os.listdir(file_path):
            new_file_path = os.path.join(file_path, markdown_post)
            with open(new_file_path, 'r') as f:
                PROJECTS[markdown_post] = \
                    markdown2.markdown(f.read(), extras=['metadata',
                                                         'fenced-code-blocks',
                                                         'code-color'])
                # DEFAULT DATA FOR PROJECTS
                # title - if title is not given use filename without extension
                PROJECTS[markdown_post].metadata.setdefault(
                    'title', markdown_post[:-3].title())
                # permalink - if permalink is not given use
                # filename without extension
                PROJECTS[markdown_post].metadata.setdefault(
                    'permalink', markdown_post[:-3])
        # CREATE A PAGE FOR DIRECTORIES INSIDE THE _PROJECT DIR
        # IT SHOWS CONTENTS IN PROJECTS DICT (contents inside that directory)
        projects_metadata = [PROJECTS[proj].metadata for proj in PROJECTS]
        file_data["pageTitle"] = project
        file_data["filePath"] = f"projects/{project}"
        file_data["assetPath"] = ".."
        # render
        projects_html = index_template.render(posts=projects_metadata,
                                              info=info, file_data=file_data)
        # save html files
        projects_filepath = f"_site/projects/{project}.html"
        os.makedirs(os.path.dirname(projects_filepath), exist_ok=True)
        with open(projects_filepath, 'w') as f:
            f.write(projects_html)
    else:
        # else it's a markdown file
        # parse it's contents and add into PROJECTS_DIR dict.
        with open(file_path, 'r') as f:
            PROJECTS_DIR[project] = \
                markdown2.markdown(f.read(), extras=['metadata',
                                                     'fenced-code-blocks',
                                                     'code-color'])
        # DEFAULT DATA FOR PROJECTS_DIR
        # title -if title is not given use filename without extension
        PROJECTS_DIR[project].metadata.setdefault(
            'title', project[:-3].title())
        # permalink -if permalink is not given use filename without extension
        PROJECTS_DIR[project].metadata.setdefault(
            'permalink', project[:-3])
        # TODO - if a markdown file directly inside the _projects directory
        # which template will use.
    dir_metadata.append(project_dict)

# data to render Projects page.
file_data["pageTitle"] = "Projects"
# path is the folder to store files, so we can use in link.
file_data["filePath"] = "projects"
file_data["assetPath"] = "."
projects_html = index_template.render(posts=dir_metadata, info=info,
                                      file_data=file_data)
# already created _site dir for index.html file.
with open('_site/projects.html', 'w') as f:
    f.write(projects_html)

# POST PAGE
# To render individual post pages
for post in POSTS:
    posts_metadata = POSTS[post].metadata
    # post_data dict is used to pass content also
    post_data = {
        'content': POSTS[post],
        'title': posts_metadata['title'],
        'date': posts_metadata['date'],
        'time': posts_metadata['time'],
        'tags': posts_metadata['tags'],
        'mode': MODE
        }
    post_html = post_template.render(post=post_data, info=info)
    post_filepath = '_site/posts/{permalink}.html'.format(
        permalink=posts_metadata['permalink'])
    os.makedirs(os.path.dirname(post_filepath), exist_ok=True)
    with open(post_filepath, 'w') as f:
        f.write(post_html)

# CHEATSHEET PAGE
CHEATSHEETS = {}
for markdown_post in os.listdir("_projects/cheatsheet"):
    cheatsheet_path = os.path.join("_projects/cheatsheet", markdown_post)
    with open(cheatsheet_path, 'r') as f:
        CHEATSHEETS[markdown_post] = \
            markdown2.markdown(f.read(), extras=['metadata',
                                                 'fenced-code-blocks',
                                                 'code-color'])
    # DEFAULT DATA FOR PROJECTS
        # title - if title is not given use filename without extension
        CHEATSHEETS[markdown_post].metadata.setdefault(
               'title', markdown_post[:-3].title())
        # permalink - if permalink is not given use
        # filename without extension
        CHEATSHEETS[markdown_post].metadata.setdefault(
               'permalink', markdown_post[:-3])

cheatsheet_template = env.get_template('cheatsheet.html')
for cheatsheet in CHEATSHEETS:
    lines = CHEATSHEETS[cheatsheet].split('\n')
    contents = collections.defaultdict(list)
    for line in lines:
        if line.strip().startswith('<h'):
            # striping <h1> and </h1>
            heading = line[4:-5].title()
            continue
        contents[heading].append(line)
    heading_content = collections.OrderedDict()
    for content in contents:
        heading_content[content] = '\n'.join(contents[content])
    import pprint
    pprint.pprint(heading_content)

    file_data["pageTitle"] = os.path.splitext(cheatsheet)[0].title()
    file_data["assetPath"] = "../.."
    # file_data["filePath"] is not required here.
    cheatsheet_html = cheatsheet_template.render(contents=heading_content,
                                                 info=info,
                                                 file_data=file_data)
    post_filepath = '_site/projects/cheatsheet/{permalink}.html'.format(
        permalink=CHEATSHEETS[cheatsheet].metadata['permalink'])
    os.makedirs(os.path.dirname(post_filepath), exist_ok=True)
    with open(post_filepath, 'w') as f:
        f.write(cheatsheet_html)

# ============================================================
# to render individual pages.
# PAGES dict is to store pages from the dir _pages
# TODO - delete page directory and create a template for about page
PAGES = {}
for markdown_page in os.listdir('_pages'):
    page_path = os.path.join('_pages', markdown_page)
    with open(page_path, 'r') as f:
        PAGES[markdown_page] = \
            markdown2.markdown(f.read(), extras=['metadata',
                                                 'fenced-code-blocks',
                                                 'code-color'])

page_template = env.get_template('page.html')

for page in PAGES:
    page_metadata = PAGES[page].metadata
    # page_data dict is used to pass content also
    page_data = {
        'content': PAGES[page],
        'title': page_metadata['title'],
        'mode': MODE
    }
    page_html = page_template.render(page=page_data, info=info)
    page_filepath = '_site/pages/{permalink}.html'.format(
        permalink=page_metadata['permalink'])
    os.makedirs(os.path.dirname(page_filepath), exist_ok=True)
    with open(page_filepath, 'w') as f:
        f.write(page_html)

# If the assets dir is not present create one and
# put all the css files and images inside the asset dir
# copy to the _site
os.makedirs('assets', exist_ok=True)
cp_cmd = "cp -r assets _site"
# copy favicon.ico to _site folder directly
if favicon:
    cp_cmd += "; cp -r assets/favicon.ico _site"
os.popen(cp_cmd)

# Check whether a favicon.ico is added in assets folder or not
# by checking true/false in info.yaml file


# ============================================================