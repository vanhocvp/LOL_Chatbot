from app import app
from dotenv import load_dotenv
import os
load_dotenv('.env')

if __name__ == '__main__':
    app.run(host = os.getenv('HOST'), port = os.getenv('PORT'),debug=True)
