# PythonAnywhere deployment

1. Create a new web app in PythonAnywhere.
2. Choose the Python version matching runtime.txt.
3. Set the project path to:
   - /home/<your_username>/Student_Risk
4. In the virtualenv section, create/select a virtualenv and install dependencies:
   - pip install -r requirements.txt
5. In the Web tab, set the WSGI file to:
   - /home/<your_username>/Student_Risk/wsgi.py
6. Set environment variables in the web app config:
   - USE_SQLITE=1
   - MYSQL_HOST=studentrisk.mysql.database.azure.com
   - MYSQL_PORT=3306
   - MYSQL_DATABASE=flexibleserverdb
   - MYSQL_USER=Driga@studentrisk
   - MYSQL_PASSWORD=Tanatswa@1212
7. Reload the web app.

If you want to use the Azure MySQL database instead of the local SQLite fallback, set USE_SQLITE=0.
