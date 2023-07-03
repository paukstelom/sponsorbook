#!/bin/sh
docker exec -it mongo_mongo1_1 mongosh --eval 'rs.initiate({"_id":"rs0","members":[{"_id":0,"host":"172.16.238.10:27017"},{"_id":1,"host":"172.16.238.11:27017"},{"_id":2,"host":"172.16.238.12:27017"}]})'
