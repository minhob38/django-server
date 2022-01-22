import sys
import subprocess

script = sys.argv[-1]

"""
django server script
- python script.py docker:db-up (docker database container를 올립니다.)
- python script.py docker:db-down (docker database container를 내립니다.)
- python script.py docker:compose-up (django server container를 올립니다.)
- python script.py docker:compose-up (django server container를 내립니다.)
- python script.py docker:build (django server image를 만듭니다.)
- python script.py docker:push (django server image를 docker hub에 push합니다.)
"""

if script == "docker:db-up":
    subprocess.Popen(["docker-compose", "-f", "docker-database/docker-compose.database.yml", "--env-file", ".env", "up", "-d"])
elif script == "docker:db-down":
    subprocess.Popen(["docker-compose", "-f", "docker-database/docker-compose.database.yml", "--env-file", ".env", "down"])
elif script == "docker:compose-up":
    subprocess.Popen(["docker-compose", "up", "-d"])
elif script == "docker:compose-down":
    subprocess.Popen(["docker-compose", "down"])
elif script == "docker:build":
    subprocess.Popen(["docker", "build", "-t", "django-server:latest", "."])
elif script == "docker:push":
    subprocess.Popen(["docker", "tag", "django-server:latest", "minhob38/django-server:latest"])
    subprocess.Popen(["docker", "push", "minhob38/django-server:latest"])

# python manage.py test
# python manage.py makemigrations
# python manage.py migrate
# python manage.py inspectdb
# python manage.py inspectdb --database=postgresql
# pip freeze > requirements.txt
