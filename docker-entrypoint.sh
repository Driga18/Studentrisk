#!/bin/sh
set -e

echo "Waiting for database readiness..."

python - <<PY
import os, time, sys
import pymysql
from urllib.parse import urlparse

url = os.getenv('DATABASE_URL')
if not url:
    print('DATABASE_URL not set; skipping DB wait')
    sys.exit(0)

# Expect format: mysql+pymysql://user:pass@host:port/dbname
try:
    no_proto = url.split('://',1)[1]
    userpass, hostdb = no_proto.split('@',1)
    user, password = userpass.split(':',1)
    hostport, dbname = hostdb.split('/',1)
    if ':' in hostport:
        host, port = hostport.split(':',1)
        port = int(port)
    else:
        host = hostport
        port = 3306
except Exception as e:
    print('Could not parse DATABASE_URL:', e)
    sys.exit(1)

for i in range(30):
    try:
        conn = pymysql.connect(host=host, user=user, password=password, port=port, db=dbname, connect_timeout=5)
        conn.close()
        print('Database is available')
        sys.exit(0)
    except Exception as e:
        print('Database not ready, retrying...', i+1)
        time.sleep(1)

print('Database did not become available in time')
sys.exit(1)
PY

# Exec the main process (gunicorn)
exec gunicorn --bind 0.0.0.0:5000 app:app
