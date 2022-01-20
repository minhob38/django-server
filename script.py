import sys
import subprocess

script = sys.argv[-1]

if script == "docker:db-up":
    subprocess.Popen(["docker-compose", "-f", "docker-database/docker-compose.database.yml", "--env-file", ".env", "up", "-d"])
elif script == "docker:db-down":
    subprocess.Popen(["docker-compose", "-f", "docker-database/docker-compose.database.yml", "--env-file", ".env", "down"])
