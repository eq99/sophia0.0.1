import os
import subprocess

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def init_db():
    subprocess.run(['python', '-m', 'run', 'db', 'init'])
    subprocess.run(['python', '-m', 'run', 'db', 'migrate'])
    subprocess.run(['python', '-m', 'run', 'db', 'upgrade'])

def migrate_db():
    subprocess.run(['python', '-m', 'run', 'db', 'migrate'])
    subprocess.run(['python', '-m', 'run', 'db', 'upgrade'])

def serve():
    subprocess.run(['gunicorn', 'run:app', '-c', 'gunicorn.conf.py'])

def main():
    # init_db()
    migrate_db()
    serve()

if __name__ == "__main__":
    main()