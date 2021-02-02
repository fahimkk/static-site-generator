---
layout: post
title: Jekyll Tutorial
permalink: jekyll-tutorial
image: tutorial.png
date: December 27, 2020
---

## Folder Structure

### **\_post** folder

Its basically the folder where you store all of your blog posts. By default jekyll has given us like this

> 2020-12-30-welcome-to-jekyll.markdown

### **\_site** folder

This is basically like the final output of your website so it continuously get updated, and it used to host the website.

### **\_config.yml** file

This is just like the settings for your jekyll website.
Inside it there are different attributes like title, description, email, baseurl, etc., that we can store about our sites.
So in here we can configure different settings and variables in order to affect the way that our website gonna run.

### **Gemfile** file

This is used with Ruby to store all of the dependencies for our website.

We can add `Themes` or `Plugins` by adding the version inside this Gemfile.

---

### **Front Matter**

Front Matter is basically just information that we store about the _pages_ of our site. All the pages in our jekyll website have front matter, which is at the top of the file.
It contains the information like titles, date, or auther etc.,

Front Matter can be written in two languages either in **YAML** or **JSON**

```
---
layout: post
title: "Welcome To Jekyll!"
date: 2020-12-30 21:02:48 +0530
categories: jekyll update
---
```

By default title is the file name and date is the date on which the file is created. We can redefine or edit these variables by providing custom values.
The jekyll theme that we are using is grabbing the information from the front matter and using it to display our blog posts on our website. So by modifying the front matter in these pages we can change the way that they show up on the website.

Front matter also plays a part in the actual URL of the page. If you click on the blog the url shows is

> localhost:port/jekyll/category/filename_with_date

`localhost:4000/jekyll/update/2020/12/30/welcome-to-jekyll.html`

we can change the term update by changing the _categories_ section.

We can define custom front matter variables, and we can also access these variables in the jekyll layouts.

```
author: "Name"
```

---

### **Default Front Matter**

Default Front Matter is basically the Front Matter that we can define in our `_config.yml` file, that front matter will apply to either all of our pages or some of our pages by default.

```
defaults:
  -
    Scope:
      path:""
      # path is tell us which files the default front matter woult be applied to.
      # emplty string means all of the files.
      type: "posts"
      # if we don't give layout to a page, it uses the default, to avoid that we can mention the type
    values:
      # values we want to store.
      layout: "post"
      title: "Default title"
```

Whenever you modified the \_config.yml file, you should restart the jekyll server

---

### **Writing Posts**

We can create the blog posts directly inside the \_posts folder or the sub-folder inside the \_posts folder to organise them. By default when we created a jekyll file there will be a sample blog post.

`2020-12-30-welcome-to-jekyll.markdown`

> Naming convention: The front of the name is the date that we want to show in our blog post. After that give the title of the post. And delinate the words by hyphen.

For posts we can use both **Markdown** and **HTML** format.

```
---
add Front Matter
---

Some Contents

```

---

### **Working with Draft**

When we write a post inside the \_post folder that will shows in the website. Here the usage of `_drafts` folder comes.
\_drafts folder is used to save the post that are'nt mean to be shows in the website.
And when you ready to publish them just move into `_posts` folder.

There is no need to follow the naming convention to save a file in \_draft folder.

To show the files inside the \_draft folder in the web page run the serer with `--draft` flag

```
jekyll serve --draft
```

When you served up a draft it will shows the default date (current date) in both the URL and below the title.

---

### **Creating Pages**

When you are creating a jekyll blog, you gonna have two type of webpages in your website.

Blog post: Which are more commenly refered to as posts, and also have general pages like About, Contact, etc. Basically these pages in your website are'nt blogs.

Pages will create inside the root directory of our project just like markdown file or html file.

```
---
Front matter
---

Contents

```

To visit the page type the page name after the post name in the url

> localhost:port_number/page_name

We can also create pages inside a sub-folder inside the root directory.

> localhost:port_number/sub-folder/page_name

Unlike the blog post, pages don't have default title or date. So to add title or date, add inside the front matter.

---

### **Permalinks**

Permalink is basically a permanent link or permanent URL that can be assigned to all the pages and posts in the site.

By default the url of a blog post (post inside the \_posts folder) is

> localhost:port/categories/year/month/day/filename

It means that the file is stored in that whole folder structure inside the `_site` folder.

When you change the categories or date in the Front matter section the URL will change.
We need to restart the server to see the changes. Here comes the importants of `permalinks`.
permalinks will add inside the front matter.

```
layout: post
date: 2020-12-30 21:02:48 +0530
categories: jekyll

permalink: "/new-url"
```

Now the URL looks like

> localhost:port/new-url

We can access certain variables inside this permalinks.

```
permalinks: /:categories
```

The `collen (:)` signifies that we want use a variable.
Now the URL using the category variable, here 'jekyll' is the category variable. Spaces between categories will convert into `/` in URL.

> localhost:port/jekyll

Lets see an example with variables and custom extension for title

```
title: "blog"
layout: post
date: 2020-12-30 21:02:48 +0530
categories: jekyll new-cat

permalink: "/:categories/:year/:month/:title.html"
```

This will gives the URL as

> localhost:port/jekyll/new-cat/2020/12/blog.html

---

### **Themes**

By default the theme is `minima`. We can check this in `_config.yml` file under theme section.

To find the theme, visit [rubygems.org]() and search for `jekyll-theme`.
Once you select a theme and you want to know more about it select `Homepage` on left side bar (this will leads into a github repo), to see a preview of the page, select preview in th readme file.

Usage:

1. Under the `Usage` section the readme section copy the theme name,

```
theme: theme_name
```

2. Open up the `Gemfile` in a text editor, (this file allows you to specify the dependencies) and paste the theme name

```
gem "theme_name"
```

3. Open the `terminal`, close the server and run

```
bundle install
```

this will install the all of the gems inside the Gemfile.

3. Open `_config.yml`, update the theme variable

```
theme: theme_name
```

4. restart the jekyll server

```
bundle exec jekyll server
```

> This may show some errors, because the theme may not have the layout (post, page, home) that we used. These layout are from the default minima theme.

> To know the availble layout, under the github page of the theme, select `_layouts` file.
> Replace the new layouts with our old layouts in our posts and pages.

---

### **Layouts**

Layouts are basically just skeltons of the html code that you can used to define the looks and the feel of the different types of pages on your sites or just the entire site in general.
