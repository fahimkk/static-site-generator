---
title: MySQL Tutorial
image: mysql.png
---

This post only shows you how to install mysql on ubuntu by using terminal and setup very basic credentials of it to get started for learning purpose.

Before jump in let's talk a little bit about what MySQL is,
it's very popular open source relational database management system (DBMS).
There is different types of databases or DBMS, like relational, NoSQL, distributed, or graph databases,
but the relational databases are very popular within web development.
Some other examples for relational databases are postgre, Microsoft SQL Server, or Oracle databases.

One thing that all relational databases have common is that they all use SQL which is structured query language,
and SQL for the most part is just that it's a query language to do things like select data, insert, sort all that stuffs and it's very similar across all relational databases (it's not identical, there are some quirks in the syntax depending on which relational database you're using but a lot of it is the same).

MySQL is a leading database for web applications and it's used in small business websites all the way to very large scale enterprise applications, so you can use it for just about anything, and it's used with multiple languages pretty much any programming language, but very popular with the languages that are used highly in web development like PHP, nodejs (JavaScript), Python, C#, etc.
And it's completely cross-platform so you can installed on Linux, Windows or Mac.

### Relational Database

A relational database (RDBMS) is based on the relational model of data, like I said majority of the databases use SQL to manage them.
RDBMS uses `tables` to store your data and this tables have `columns` and `rows` similar to what you'd see in like an Excel spreadsheet.
Tables and fields can relate to each other through `keys`.

### Common Data Types

- Numeric &nbsp; &nbsp; &nbsp;INT, TINYINT, BIGINT, FLOAT
- String &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; VARCHAR, TEXT, CHAR
- Dates &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; DATE, DATETIME, TIMESTAMP
- Other &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; BINARY, JSON

TINYINT normally used for bool values, `0 for false and 1 for true`

VARCHAR is normally for small texts (below 255), and for larger text we use TEXT (max of 65,000 characters).

## Installation & Environment

Locally you can install standalone server of MySQL this is what I'll be showing in this post,
but you can also install software suites like XAMPP, MAMP, WAMP/LAMP which they come with an Apache web server, PHP which is a programming language, MySQL and some other stuff as well, Usually they used for local development.

If you are using a solution like digitalocean or aws like cloud hosting,
they pretty much give you a terminal or a Linux container and you can access it through a terminal in that case you would install MySQL using whatever package manager that Linux distribution uses.

As far as managing your server or managing your databases there's different ways to do this, so with MySQL you get a shell program that you login through your `terminal or command line`, you have desktop tools such as `MySQL workbench` and you also have web-based tools like `PHPMyAdmin` if you are installed XAMPP, WAMP/LAMP or MAMP.
In PHPMyAdmin you can log in to the program through your browser and you can actually manage your database from there in a graphical interface.

## Install on Ubuntu using Terminal

```bash
sudo apt update
sudo apt install mysql-server
```

The first command is to update the system softwares, and second is to install mysql.

To check the version

```bash
mysql --version
```

which will give you the version of my sql installed on your ubuntu system.

## Configure Mysql

If you wanna go with the root password you can also go,
but if you wanna to set your password yourself you could also do that.

To configure your mysql

```bash
sudo mysql_secure_installation
```

The first step after running the above code is password validation.
The prompt will ask your permission to setup VALIDATE PASSWORD component. Press y for yes.
It would say that there are three levels of password validation policy, so choose the one you want.
And after that type your password which matches the level you have chosen.
Then the prompt shows the estimated strength of your password,
so you can decide whether you want to continue with this password or not.
(if you press no then it will allow you to rewrite your password)

After the password setup, the prompt will ask you about Removing anonymous users. Choose yes/no.

Then it will as your permission for Disallow root login remotely.

After that it will ask your permission to Remove test database and access to it.

And finally it will ask your permission to Reload privilege tables now.

You can change these credentials in future with the same above command.
So you can see that it's all done now.
So we have installed Mysql and now we have also changed the password and we have done the settings that we waned to.

## Get starts with Mysql

To go to mysql console or to login

```bash
sudo mysql -u root

or

mysql -u root -p
```

The second command is for if you enabled password authentication for root,(we discussed in the last session) here -p is for password, it will ask for your password, so you can put your root users password or if you created an user account then you can put user name instead of root and give its password

After creating an user account instead of using root in above commands you can use the username to login as the user.

Now you will enter into the mysql console (interface).

Use this username and password to connect in mysql-workbench.

- Database -> connect to database - change the root with your username and enter the password after clicking ok button.

You can clear the terminal with `Ctrl l`

To exit from mysql interface you can use `quit` command.

## Create a new User

Once you have access to the MySQL prompt, you can create a new user with a CREATE USER statement. These follow this general syntax:

```bash
CREATE USER 'username'@'host' IDENTIFIED BY 'password';
```

After `CREATE USER`, you specify a username.
This is immediately followed by an @ sign and then the hostname from which this user will connect.
If you only plan to access this user locally from your Ubuntu server, you can specify `localhost`.
Wrapping both the username and host in single quotes isn’t always necessary, but doing so can help to prevent errors.

To list all the users that you have

```bash
SELECT user, host FROM mysql.user;
```

Right now the user we have created can't do anything, we have to give this user some privileges.
To make this user as an admin so that he can create new databases, update data in other databases etc, so full access and you.

```bash
GRANT ALL PRIVILEGES ON * . * TO 'username'@'host';
```

You can also grant limited privileges, here is an example for that

```bash
GRANT CREATE, DROP, INSERT, UPDATE, DELETE, SELECT, ON * . * TO 'username'@'host';
```

In both the examples we use asterisks(\*) which grants user privileges globally in place of databases and table names.
In SQL, asterisks are special characters used to represent "all" databases or tables.

Following this, it’s good practice to run the FLUSH PRIVILEGES command. This will free up any memory that the server cached as a result of the preceding CREATE USER and GRANT statements:

```bash
FLUSH PRIVILEGES;
```

To check the privileges for a certain user

```bash
SHOW GRANTS FOR 'username'@'host';
```

## Create a Database

To see the databases you have

```bash
SHOW DATABASES;
```

To create a new database

```bash
CREATE DATABASE database_name;
```

if you don't put semicolon it will go on to the next line, because you can do multi-line statements.

To check whether the database creation is successful or not,
type `SHOW DATABASES;` command again to list all your databases.

To use that database we actually have to specify `USE` and then the database name

```bash
USE database_name
```

To remove a table

```bash
DROP DATABASE database_name;
```

## Creating Tables

To create a table

```bash
CREATE TABLE table_name(
    id INT AUTO_INCREMENT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(75),
    password VARCHAR(255),
    location VARCHAR(100),
    dept VARCHAR(75),
    is_admin TINYINT(1),
    register_date DATETIME,
    PRIMARY KEY(id)
);
```

To see the tables inside the selected database

```bash
SHOW TABLES;
```

To remove a table

```bash
DROP TABLE table_name;
```
