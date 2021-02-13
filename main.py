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
"""

import os
from datetime import datetime
import collections

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
        # title -if title is not given use filename without extn
        POSTS[markdown_post].metadata.setdefault(
            'title', markdown_post[:-3])
        # permalink -if permalink is not given use filename without extn
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

"""
layout_template = env.get_template('layout_tem.html')
layout_html = layout_template.render(info=info)
# This file will be removed at the end. ie -
# - data required for creating pages will be passed through layout.html
# all the _template extends layout.html file
with open('_templates/layout.html', 'w') as f:
    f.write(layout_html)
"""

# Pass metadata to index.html page
posts_metadata = [POSTS[post].metadata for post in POSTS]
# posts_metadata is a list, so we can't access posts.mode in index.html
index_html = index_template.render(posts=posts_metadata, mode=MODE, info=info)
# This will pass a list of metadata through the
# variable posts to our index.html page template

# metadata_date: key - date and value list of posts
metadata_date = collections.defaultdict(list)
for post in posts_metadata:
    year = datetime.strptime(post['date'], '%B %d, %Y').year
    metadata_date[year].append(post)
blog_html = blog_template.render(posts=metadata_date, mode=MODE, info=info)


# Create _site dir if not exists
os.makedirs('_site', exist_ok=True)
with open('_site/index.html', 'w') as f:
    f.write(index_html)
with open('_site/blog.html', 'w') as f:
    f.write(blog_html)

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
# ============================================================
# to render individual pages.
# PAGES dict is to store pages from the dir _pages
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