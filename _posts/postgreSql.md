---
title: PostgreSQL Tutorial
image: postgre.jpeg
---


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

## PostgreSQL Roles

Database access permissions within PostgreSQL are handled with the concept of roles. A role can represent a database user or a group of database users.

The installation procedure created an user account called "postgres" that is associated with the default postgres role, and a database with the same name ("postgres").
This user is the superuser for the PostgreSQL instance, and it is equivalent to the MySQL root user.
In order to use "postgres" you have to login to that account.

There are two way to login to you PostgreSQL account.

The first one is to switch over to the postgres account on your terminal by typing

```bash
sudo -i -u postgres
```

You can now access the PostgreSQL prompt immediately by typing

```bash
psql
```

From there you are free to interact with the database management system.

To know the details about the connection you can use `\conninfo` inside the PostgreSQL prompt.

Exit out of the PostgreSQL prompt by typing `\q` .

Another method to login is by running the command you’d like with the postgres account directly with `sudo`.
That means in the last method we were get to the Postgres prompt by first switching to the postgres user and then running `psql` to open the Postgres prompt.
You could do this in one step by running the single command `psql` as the postgres user with `sudo`

```bash
sudo -u postgres psql
```

This will log you directly into Postgres without the intermediary `bash` shell in between.

## Creating a New Role

You can create new roles from the command line with the `createuser` command.
The `--interactive` flag will prompt you for the name of the new role and also ask whether it should have superuser permissions.

If you are logged in as the Postgres account, you can create a new user by typing

```bash
createuser --interactive
```

if you prefer to use `sudo`, without switching from your normal account,

```bash
sudo -u postgres createuser --interactive
```

This will ask your name role and give choice to be a super user.

Inside the psql shell you can give the DB user postgres a password:

```sql
ALTER USER postgres PASSWORD 'newPassword';
```

You can access more about additional flags of a command from `man` page. For example,

```bash
man createuser
```

## Creating a New Database

If you created a user with username user_1, that role will attempt to connect to a database which is also called “user_1” by default.
You can create the appropriate database with the `createdb` command.

PostgreSQL flexibility provides multiple paths for creating databases as needed.

If you are logged in as the postgres account,

```bash
createdb database_name
```

If you are in your linux terminal

```bash
sudo -u postgres createdb database_name
```

instead of postgres you can also use role name (username) who has create database privilege

## Login with new user

To log in with `ident` based authentication, you’ll need a Linux user with the same name as your Postgres role and database.

If you don’t have a matching Linux user available, you can create one with the `adduser` command.

```bash
sudo adduser linux_username
```

After creating a role, you can login with that username instead of "postgres"

```bash
sudo -u username psql
```

If you want your user to connect to a different database, you can do so by specifying the database like this

```bash
psql -d postgres
```

## Creating Tables

The basic syntax for creating tables is as follows:

```sql
CREATE TABLE table_name (
    column_name1 col_type (field_length) column_constraints,
    column_name2 col_type (field_length),
    column_name3 col_type (field_length)
);
```

Some data types like id, date, etc. don’t require a set length because the length or format is implied.

For id we use `serial` as type, which is an auto-incrementing integer.
This column also has the constraint of `PRIMARY KEY` which means that the values within it must be unique and not null.

To see new table

```sql
\d
```

If you want to see just the table without the sequence,

```sql
\dt
```
