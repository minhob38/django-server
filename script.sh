source bin/activate
deactive

python manage.py makemigrations
python manage.py runserver
python manage.py migrate
python manage.py inspectdb
python manage.py inspectdb --database=postgresql

pip freeze > requirements.txt

shp2pgsql -s 5179 -W euc-kr /Users/minho/Desktop/django-server/data/seoul_bjd/LSMD_ADM_SECT_UMD_11.shp seoul_bjd| psql -h localhost -p 5432 -U postgres -d study
shp2pgsql -s 5179 -W euc-kr /Users/minho/Desktop/django-server/data/seoul_sgg/LARD_ADM_SECT_SGG_11.shp seoul_sgg| psql -h localhost -p 5432 -U postgres -d study