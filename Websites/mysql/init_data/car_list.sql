SET GLOBAL local_infile = 'ON';
GRANT ALL PRIVILEGES ON *.* TO 'daniel'@'%' WITH GRANT OPTION;
use carsgo;
DROP TABLE IF EXISTS car_list;
CREATE TABLE car_list(
    carID VARCHAR(200) PRIMARY KEY,
    carBrand VARCHAR(200),
    carModel VARCHAR(200),
    carYear INT,
    carPrice INT,
    carMileage INT,
    carAddress VARCHAR(1000),
    carTitle VARCHAR(1000),
    carPhoto VARCHAR(1000),
    dealerAddress VARCHAR(1000),
    source VARCHAR(200),
    segment INT
);


LOAD DATA LOCAL INFILE  '/home/carList_forWebsite.csv' INTO TABLE car_list
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;