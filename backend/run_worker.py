import os
from dotenv import load_dotenv

if __name__ == '__main__':
    # Load .env file from the parent directory (since we are in backend)
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path)

    # Make sure OpsPilot root is in PYTHONPATH
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    print(f"Starting Celery Worker with REDIS_URL={os.getenv('REDIS_URL')}")
    # Execute the Celery worker command
    os.system('celery -A worker.celery_app worker -l info --pool=solo')
