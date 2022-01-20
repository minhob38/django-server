# 공간 Data Database 저장

postgresql에 spatial data(shapefile)는 shp2pgsql로 저장할 수 있습니다.

## shp2psql

### • syntax

```sh
shp2pgsql -s [sid] -W [encoding] [.shp 경로] [table 이름] | psql -h [host] -p [port 번호] -U [user 이름] -d [database 이름]
```

### • example

```sh
shp2pgsql -s 4326 -W euc-kr ./seoul_sggs/seoul_sggs.shp seoul_sggs| psql -h localhost -p 5432 -U postgres -d docker-database
```

## 참고자료

• [postgis loading spatial data](https://postgis.net/workshops/postgis-intro/loading_data.html)  
• [shp2pgsql](https://postgis.net/docs/using_postgis_dbmanagement.html#shp2pgsql_usage)
