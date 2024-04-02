# File Sharing Platform FastAPI

This is a simple file management system built with FastAPI and PostgreSQL. It allows users to upload, download, and delete files.

![fastapi](https://img.shields.io/badge/fastapi-0.110.0-blue)
![psycopg2](https://img.shields.io/badge/psycopg2-2.9.9-blue)
![python-dotenv](https://img.shields.io/badge/dotenv-1.0.1-blue)
![uvicorn](https://img.shields.io/badge/uvicorn-0.29.0-blue)


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Gumballton/file-sharing-platform-fastapi.git
---
2. Install the required dependencies: `pip install -r requirements.txt`
---
3. Set up the PostgreSQL database and configure the environment variables. You can do this by creating a `.env` file in the root directory and adding the following variables:
   ```
   DB_HOST=your_database_host
   DB_PORT=your_database_port
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_NAME=your_database_name
   ```
---
4. Run the FastAPI application:
   ```bash
   uvicorn main:app --reload
   ```

# Usage

### Uploading a File

Send a **POST** request to `/upload` endpoint with the file attached as *multipart/form-data*. You will receive a response containing the filename and a download link.

---

### Downloading a File

Send a **GET** request to `/download/{filename}` endpoint, where `{filename}` is the name of the file you want to download. The file will be downloaded with the original filename.

---

### Deleting a File

Send a **DELETE** request to `/delete/{filename}` endpoint, where `{filename}` is the name of the file you want to delete. The file will be deleted from the server.