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

import markdown2
import jinja2
import yaml


def parseMdPost(filepath):
    with open(filepath, 'r') as f:
        md_post = markdown2.markdown(f.read(), extras=['metadata',
                                                       'fenced-code-blocks',
                                                       'code-color'])
    return md_post


def createMdDict(dir_name):
    MD = {}
    for md_file in os.listdir(dir_name):
        MD[md_file] = parseMdPost(os.path.join(dir_name, md_file))

    # DEFAULT DATA FOR POSTS
        # date (Current date) if date is not given in the post
        # strftime returns the string representation of date.
        MD[md_file].metadata.setdefault(
            'date', datetime.today().strftime('%B %d, %Y'))
        # title -if title is not given use filename without extension
        MD[md_file].metadata.setdefault(
            'title', md_file[:-3].title())
        # permalink -if permalink is not given use filename without extension
        MD[md_file].metadata.setdefault(
            'permalink', md_file[:-3])
        # tags - if tags are not give put ...
        MD[md_file].metadata.setdefault(
            'tags', '...')
        # time - if time is not give use 0 min
        MD[md_file].metadata.setdefault(
            'time', '0 min')

        # Abstract and Language are for Projects
        MD[md_file].metadata.setdefault(
            'abstract', md_file[:-3].title())
        MD[md_file].metadata.setdefault(
            'language', "")


    return MD


def createMetadataList(md_dict):
    md_metadata = [md_dict[post].metadata for post in md_dict]
    return md_metadata


def save(filepath, html_file):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(html_file)


def setFileData(page_title, assets_path):
    return {"pageTitle": page_title,
            "assetPath": assets_path}


def parseContent(html):
    lines = html.split('\n')
    contents = collections.defaultdict(list)
    # if there is no tag at first (no heading)
    heading = "Introduction"
    for line in lines:
        if line.strip().startswith('<h'):
            # striping <h1> and </h1>
            heading = line[4:-5].title()
            continue
        contents[heading].append(line)
    headingAndContent = collections.OrderedDict()
    for content in contents:
        headingAndContent[content] = '\n'.join(contents[content])
    return headingAndContent


# Sort the markdown_post w.r.t time
# strptime is used to convert string date to date format
def sortWrtTime(DICT):
    DICT = {
        # key: value for key in sorted posts
        post: DICT[post] for post in sorted(
            DICT, key=lambda post: datetime.strptime(
                DICT[post].metadata['date'], '%B %d, %Y'),
            reverse=True)
    }
    return DICT
# TODO
# for personal details
favicon = False
with open('info.yaml') as f:
    info = yaml.safe_load(f)
    if info['favicon']:
        favicon = True
file_data = {}
os.makedirs('_site', exist_ok=True)

env = jinja2.Environment(loader=jinja2.PackageLoader('main', '_templates'))
# PackageLoader -
# 1st arg - name of python file
# 2nd arg - directory name where template files are located
index_template = env.get_template('index.html')
about_template = env.get_template('about.html')
blog_template = env.get_template('blog.html')
projects_template = env.get_template('projects.html')
post_template = env.get_template('post.html')
cheatsheets_template = env.get_template('cheatsheets.html')
cheatsheets_posts_template = env.get_template('cheatsheets_post.html')

# COLLECTING PROJECTS POSTS DATA
# PROJECTS dict to store blog posts from the directory posts
PROJECTS = createMdDict("_projects")
# Sort the markdown_post w.r.t time
PROJECTS = sortWrtTime(PROJECTS)
# for loop for home page Projects section.
projects_metadata = createMetadataList(PROJECTS)

# PROJECTS PAGE
# path is the folder to store files, so we can use in link.
file_data = setFileData("Projects", ".")
projects_html = projects_template.render(posts=projects_metadata, info=info,
                                         file_data=file_data)
save("_site/projects.html", projects_html)

# PROJECTS POST PAGE
# To render individual post pages
for project in PROJECTS:
    project_metadata = PROJECTS[project].metadata
    file_data = setFileData(project_metadata['title'], "..")
    # post_template is used for project posts.
    project_html = post_template.render(post=project_metadata,
                                        content=PROJECTS[project],
                                        info=info,
                                        file_data=file_data)
    project_filepath = '_site/projects/{permalink}.html'.format(
        permalink=project_metadata['permalink'])
    save(project_filepath, project_html)

# COLLECTING BLOG POSTS DATA
# POSTS dict to store blog posts from the directory posts
POSTS = createMdDict("_posts")
# Sort the markdown_post w.r.t time
POSTS = sortWrtTime(POSTS)
# for loop for home page resent blogs section.
# posts in this list is sorted w.r.t time
posts_metadata = createMetadataList(POSTS)

# BLOG PAGE
# metadata_date: key - date and value list of posts
metadata_date = collections.defaultdict(list)
for post in posts_metadata:
    year = datetime.strptime(post['date'], '%B %d, %Y').year
    metadata_date[year].append(post)
file_data = setFileData('Blog', '.')
blog_html = blog_template.render(posts=metadata_date, info=info,
                                 file_data=file_data)
save("_site/blog.html", blog_html)

# BLOG POST PAGE
# To render individual post pages
for post in POSTS:
    post_metadata = POSTS[post].metadata
    file_data = setFileData(post_metadata['title'], "..")
    post_html = post_template.render(post=post_metadata,
                                     content=POSTS[post],
                                     info=info,
                                     file_data=file_data)
    post_filepath = '_site/posts/{permalink}.html'.format(
        permalink=post_metadata['permalink'])
    save(post_filepath, post_html)

# CHEATSHEETS PAGE
CHEATSHEETS = createMdDict("_cheatsheets")
# COLLECT CHEETSHEET DATA FOR HOME PAGE
cheatsheets_metadata = createMetadataList(CHEATSHEETS)
# A list of data which contains Category as key and item list as value
category = collections.defaultdict(list)
for cheatsheet in cheatsheets_metadata:
    cat = cheatsheet['category'].title()
    category[cat].append(cheatsheet)
# sort categories based on alphabetical order
categories = collections.OrderedDict()
for cat in sorted(category):
    categories[cat] = category[cat]
file_data = setFileData("CheatSheet", '.')
cheatsheets_html = cheatsheets_template.render(
                                        categories=categories,
                                        cheatsheets=cheatsheets_metadata,
                                        info=info, file_data=file_data)
save("_site/cheatsheets.html", cheatsheets_html)

# CHEATSHEET POST PAGE
for cheatsheet in CHEATSHEETS:
    headingAndContent = parseContent(CHEATSHEETS[cheatsheet])
    file_data = setFileData(os.path.splitext(cheatsheet)[0].title(), "..")
    cheatsheets_posts_html = cheatsheets_posts_template.render(
                                                 contents=headingAndContent,
                                                 info=info,
                                                 file_data=file_data)
    post_filepath = '_site/cheatsheets/{permalink}.html'.format(
        permalink=CHEATSHEETS[cheatsheet].metadata['permalink'])
    save(post_filepath, cheatsheets_posts_html)

# ABOUT PAGE
about = parseMdPost('about.md')
# Parse about.md file, if "abstract" is provided as metadata
# use it for home page, otherwise take fist line.
about_abstract = about.metadata['abstract']
if not about_abstract:
    about_abstract = about.split('\n\n')[0]
file_data = setFileData("About", ".")
# posts_metadata is a list, so we can't access posts.mode in index.html
about_html = about_template.render(content=about, info=info,
                                   file_data=file_data)
save("_site/about.html", about_html)

# HOME PAGE
# Pass metadata to index.html page
file_data = setFileData("Home", ".")
# posts_metadata is a list, so we can't access posts.mode in index.html
index_html = index_template.render(posts=posts_metadata, info=info,
                                   about_abstract=about_abstract,
                                   file_data=file_data,
                                   projects=projects_metadata,
                                   cheatsheets=cheatsheets_metadata)
# This will pass a list of metadata through the
# variable posts to our index.html page template
save("_site/index.html", index_html)


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