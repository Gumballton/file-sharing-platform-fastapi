import os
import urllib
import psycopg2

from fastapi import FastAPI, HTTPException, Response, File, UploadFile
from dotenv import dotenv_values
from uuid import uuid4


app = FastAPI()

env_vars = dotenv_values()

# Database connection
connection = psycopg2.connect(**env_vars)


# Directory to work with files
UPLOAD_DIR = 'uploads'
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
    
# Route to upload a file
@app.post('/upload/')
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = f'{uuid4()}_{file.filename}'
        path = os.path.join(UPLOAD_DIR, file_path)
        with open(path, 'wb') as f:
            f.write(await file.read())
        
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO files(filename) VALUES(%s)', (file_path,))
            connection.commit()

        return  {"filename": file_path, 'to_download': f'/download/{file_path}'}

    except:
        return {'error': 'something wrong'}

# Route to download a file
@app.get('/download/{filename}')
async def download_file(filename: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT filename FROM files WHERE filename = %s', (filename,))
            
            file_path = cursor.fetchone()[0]

        full_file_path = f'uploads/{file_path}'
        if not os.path.exists(full_file_path):
            return HTTPException(404, 'no such file')

        with open(full_file_path, 'rb') as f:
            contents = f.read()

        return Response(content=contents, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename*=UTF-8''{urllib.parse.quote(os.path.basename(file_path))}"})

    except:
        return {'error': 'something wrong'}

# Route to delete a file
@app.delete('/delete/{filename}')
async def delete_file(filename: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM files WHERE filename = %s', (filename,))
            connection.commit()

        os.remove(f'uploads/{filename}')
        
        return {'message': 'file deleted successfully'}

    except:
        return {'error': 'something wrong'}