import sys
import subprocess

script = sys.argv[-1]

"""
django server script
- python script.py docker:db-up
"""

if script == "docker:db-up":
    subprocess.Popen(["docker-compose", "-f", "docker-database/docker-compose.database.yml", "--env-file", ".env", "up", "-d"])
elif script == "docker:db-down":
    subprocess.Popen(["docker-compose", "-f", "docker-database/docker-compose.database.yml", "--env-file", ".env", "down"])


# source bin/activate
# deactive

# python manage.py test
# python manage.py makemigrations
# python manage.py runserver
# python manage.py migrate
# python manage.py inspectdb
# python manage.py inspectdb --database=postgresql

# pip freeze > requirements.txt
