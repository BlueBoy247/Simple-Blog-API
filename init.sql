-- Create database
CREATE DATABASE IF NOT EXISTS blogdb;

-- Set blogdb as current database
USE blogdb;

-- Create users tables
CREATE TABLE IF NOT EXISTS users (
    email VARCHAR(255) PRIMARY KEY NOT NULL,
    pwd VARCHAR(60) NOT NULL
);

-- Create posts tables
CREATE TABLE IF NOT EXISTS posts (
    id VARCHAR(16) PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    content LONGTEXT,
    tags JSON
);
