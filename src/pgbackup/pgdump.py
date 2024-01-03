import sys
import subprocess

def dump(url):
    try:
        return subprocess.Popen(['pg_dump', url], stdout=subprocess.PIPE)
    except OSError as err:
        print(f"Error: {err}")
        sys.exit(1)

def dump_file_name(url, timestamp=None):
    # Below, we split the url, and we will get only the database name, because the name comes after the last slash
    db_name = url.split('/')[-1]
    # And below here we filter out if there are any queries attached to the end
    db_name = db_name.split('?')[0]
    if timestamp:
        return f"{db_name}-{timestamp}.sql"
    else:
        return f"{db_name}.sql"
