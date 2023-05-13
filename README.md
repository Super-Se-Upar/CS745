# CS 745 Course Project

# Design of a Secure Python Web Application Implementing Chinese Wall Model of Access Control and CSRF Protection

## Team Chusariro : Members

- Sankalp Bhamare 200110096
- Rohan Rajesh Kalbag 20D170033
- Jujhaar Singh 200110052
- Rishabh Ravi 200260041

## Front End Website

Designed using HTML, Bootstrap

## Backend

Designed using Flask and Python

## Salient Features of Project

- ### Native Implementation of CSRF Token Based Login

- ### User Authentication

- ### Database for Users

  1. Employee ID, Password, Role, Set of Accessible Companies.
  2. Files accessed before (CD, COI)

- ### Database for Files (Objects)

  1. Flag to check whether Sanitized or Unsanitized Data
  2. Content of the File
  3. Owner Company (CD)

- ### Database for Companies

  1. Company Name (CD)
  2. Conflict of Interest (COI)

- ### Chinese Wall Model Based Access Control System
  1. The backend has a set of documents owned by specific companies
  2. List of users and the companies they have access to initially
  3. Chinese Wall Model for temporal access control of different documents

## Chinese Wall Rules

- ### Definitions

  1. Object: Files of a company (Text Documents .txt)
  2. CD: all the files belonging to the same company
  3. COI: similar companies that have a conflict of interest

- ### Rule for allowing a user to read a new file

  1. Has already read an file of the same company
  2. Has not read any file before having the same COI.
  3. The file is sanitized or its contents are available for public access

- ### Rule to allow a user to write/edit a file

  1. Has read access to the file
  2. All the files that he can read must be in the same company.
