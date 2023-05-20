# Design of a Secure Python Web Application Implementing Chinese Wall Model of Access Control and CSRF Protection

## CS-745 : Principles of Data and System Security

*Developed the application's backend using Flask, a powerful web framework in Python. Utilized Python programming language to implement robust and efficient backend functionalities, including user authentication, database management, and secure file access. Implemented a secure login system using CSRF tokens to prevent cross-site request forgery attacks. Employed industry best practices to ensure the confidentiality and integrity of user credentials and session management. Incorporated the Chinese Wall Model for temporal access control of documents within the application. Designed a comprehensive database structure to manage users, companies, and files, enforcing strict access restrictions based on user roles and conflict of interest criteria.*

## [Link to Website Demo Video](https://youtu.be/BJKygw7BOrs)

## Contributors : Team Chusariro
- Sankalp Bhamare
- Rohan Rajesh Kalbag
- Jujhaar Singh
- Rishabh Ravi

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
