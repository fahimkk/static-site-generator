---
title: PostgreSQL
image: postgrefeat.jpg
category: database
---

## Introduction

PostgreSQL is a relational database management system that provides an implementation of the sql querying language.
It's a popular choice for many small and large projects,
and it has the advantages of being standards compliant and having many advanced features like reliable transactions and concurrency without read blocks.

## Install PostgreSQL on Ubuntu 20.04

Use the terminal to install PostgreSQL

If you’ve not done so recently, refresh your server’s local package index

```bash
sudo apt update
```

Then, install the postgresql package along with a `-contrib` package that adds some additional utilities and functionality

```bash
sudo apt install postgresql postgresql-contrib
```

Now you have installed postgresql on your machine.
