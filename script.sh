source bin/activate
deactive

python manage.py test
python manage.py makemigrations
python manage.py runserver
python manage.py migrate
python manage.py inspectdb
python manage.py inspectdb --database=postgresql

pip freeze > requirements.txt

shp2pgsql -s 5179 -W euc-kr /Users/minho/Desktop/django-server/data/seoul_bjds/LSMD_ADM_SECT_UMD_11.shp seoul_bjds| psql -h localhost -p 5432 -U postgres -d study
shp2pgsql -s 5179 -W euc-kr /Users/minho/Desktop/django-server/data/seoul_sggs/LARD_ADM_SECT_SGG_11.shp seoul_sggs| psql -h localhost -p 5432 -U postgres -d study

shp2pgsql -s 4326 -W euc-kr /Users/minho/Desktop/django-server/data/seoul_bjds/seoul_bjds.shp seoul_bjds| psql -h localhost -p 5432 -U postgres -d study
shp2pgsql -s 4326 -W euc-kr /Users/minho/Desktop/django-server/data/seoul_sggs/seoul_sggs.shp seoul_sggs| psql -h localhost -p 5432 -U postgres -d study


shp2pgsql -s 4326 -W euc-kr /Users/minho/Desktop/a/a.shp a| psql -h localhost -p 5432 -U postgres -d study
