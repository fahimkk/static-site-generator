import os
from datetime import datetime

import markdown2
import jinja2

# POSTS dict to store blog posts from the directory posts
POSTS = {}
# Loop through all the markdown files from posts directory
for markdown_post in os.listdir('posts'):
    file_path = os.path.join('posts', markdown_post)
    with open(file_path, 'r') as f:
        # extras = ['metadata'] gives a dict of metadata
        # that we provided at the begining of the markdown file.
        POSTS[markdown_post] = \
            markdown2.markdown(f.read(), extras=['metadata'])
        # POSTS dict -
        # key : markdown_post, ie file name
        # value: content (string format html)
        # POSTS['markdown_post'].metadata gives a dict of metadata

# Sort the markdown_post w.r.t time
# strptime is used to convert string date to date format
POSTS = {
    # key: value for key in sorted posts
    post: POSTS[post] for post in sorted(
        POSTS, key=lambda post: datetime.strptime(
            POSTS[post].metadata['date'], '%d-%m-%Y'),
        reverse=True)
}

env = jinja2.Environment(loader=jinja2.PackageLoader('main', 'templates'))
# PackageLoader -
# 1st arg - name of python file
# 2nd arg - directory name where template files are located
index_template = env.get_template('index.html')
post_template = env.get_template('post.html')

# Pass metadata to index.html page
posts_metadata = [POSTS[post].metadata for post in POSTS]
index_html = index_template.render(posts=posts_metadata)
# This will pass a list of metadata through the
# variable posts to our index.html page template
with open('site/index.html', 'w') as f:
    f.write(index_html)

# To render individual post pages
for post in POSTS:
    posts_metadata = POSTS[post].metadata
    post_data = {
        'content': POSTS[post],
        'title': posts_metadata['title'],
        'date': posts_metadata['date']
    }
    post_html = post_template.render(post=post_data)
    post_filepath = 'site/posts/{slug}.html'.format(
        slug=posts_metadata['slug'])
    os.makedirs(os.path.dirname(post_filepath), exist_ok=True)
    with open(post_filepath, 'w') as f:
        f.write(post_html)
