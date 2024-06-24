This project implements a secure file-sharing system using Django and Django Rest Framework (DRF). 
The system involves two types of users: Operation Users (Ops Users) and Client Users.
 Ops Users can upload specific file types (pptx, docx, xlsx), while Client Users can sign up, 
verify their email, login, download files, and list all uploaded files.

Features

Ops Users
sign up
Login
Upload files (pptx, docx, xlsx)

Client Users
Sign Up (returns an encrypted URL)
Email Verification (sends a verification email) for sending mail for verification, test instance are used so please go to localhost:8025 to see the sent mail details.
Login
Download files
List all uploaded files

Command to run project:
docker-compose up --build


