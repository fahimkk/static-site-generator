---
layout: post
title: Hosting on Github Pages
permalink: hosting-on-github-pages
image: hosting.png
date: December 31, 2021
---

Github pages is a service that github offers, and it basically allows you to serve and host a static website completely free.

1. Create a new repository - make sure that you don't initialize with a readme.
2. Modify baseurl inside the `_config.yml` file

```
baseurl: "name of the repository"
# if you have a custom domain name put that.
# it acts as the base url for our website.
```

3.Open up terminal

to initialize the git inside the root directory.

```bash
git init
```

checkout to the gh-pages branch.
When you create a Github pages website, all the files for that website get stored on the gh-pages branch

```bash
git checkout -b gh-pages
```

Add all of the files to commit

```bash
git add .
```

Commit all of the files to our repository

```bash
git commit -m "initial commit"
```

Link our local git repository with the Github repository.

```bash
git remote add origin repository_link
```

Push all the files into Github repository

```bash
git push origin gh-pages
```

4.Open Github - settings - inside the Github pages section you will get a link for the website.
