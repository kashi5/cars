create DATABASE vehical;
create table car(id INT PRIMARY KEY NOT NULL, name CHAR(50) NOT NULL, brand CHAR(50) NOT NULL);
insert into car(id,name,brand) values(1,'audi-1','audi');
insert into car(id,name,brand) values(2,'audi-2','audi');
insert into car(id,name,brand) values(3,'audi-3','audi');
insert into car(id,name,brand) values(4,'bmw-1','bmw');
insert into car(id,name,brand) values(5,'bmw-2','bmw');
insert into car(id,name,brand) values(6,'honda-1','honda');
insert into car(id,name,brand) values(7,'honda-2','honda');
insert into car(id,name,brand) values(8,'lotus-1','lotus');
insert into car(id,name,brand) values(9,'toyota-1','toyota');
insert into car(id,name,brand) values(10,'toyota-2','toyota');
insert into car(id,name,brand) values(11,'toyota-3','toyota');

--select DISTINCT(brand) from cars;