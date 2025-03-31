create table works(
work_type_id INT primary KEY,
work_type_name varchar (25),
parent_work_type_id int
);

alter table works
ADD foreign KEY (parent_work_type_id)
REFERENCES works (work_type_id)
ON DELETE SET NULL;

create table employees(
user_id int primary key,
first_name varchar (20),
last_name varchar (20),
password varchar (20),
is_admin int
);

create table locations(
location_id varchar(7) primary KEY,
location_desc varchar (40)
);

create table warehouses(
warehouse_id int primary KEY,
warehouse_desc varchar (40)
);

create table batteries(
serial_number varchar(30) primary key,
part_number int,
item_type int,
part_description varchar(40)
);

create table requests(
request_id int primary key,
request_time timestamp unique,
serial_number varchar(30),
work_type_id int,
user_id int,
warehouse_id int,
FOREIGN KEY (serial_number) REFERENCES batteries (serial_number) ON DELETE SET null,
foreign key (work_type_id) REFERENCES works (work_type_id) ON DELETE SET null,
foreign key (user_id) REFERENCES employees (user_id) ON DELETE SET null,
foreign key (warehouse_id) REFERENCES warehouses (warehouse_id) ON DELETE SET null
);

ALTER TABLE spiersnt.employees ADD warehouse_id INT NULL;

alter table employees
add foreign key (warehouse_id)
references warehouses (warehouse_id)
on delete set null;

ALTER TABLE spiersnt.locations ADD warehouse_id INT NULL;

alter table locations
add foreign key (warehouse_id)
references warehouses (warehouse_id)
on delete set null;

create table report(
request_id int primary key,
report_desc varchar (40),
foreign key (request_id) references requests (request_id)
);

insert into works values(1, "Find", null);
insert into works values(2, "Receive", null);
insert into works values(3, "Ship", null);
insert into works values(4, "Move", null);