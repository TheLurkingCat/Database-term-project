CREATE TABLE Temperatures(
   dt                                           DATE                PRIMARY KEY    NOT NULL,
   LandAverageTemperature                       double precision NOT NULL,
   LandAverageTemperatureUncertainty            double precision NOT NULL,
   LandMaxTemperature                           double precision NOT NULL,
   LandMaxTemperatureUncertainty                double precision NOT NULL,
   LandMinTemperature                           double precision NOT NULL,
   LandMinTemperatureUncertainty                double precision NOT NULL,
   LandAndOceanAverageTemperature               double precision NOT NULL,
   LandAndOceanAverageTemperatureUncertainty    double precision NOT NULL
);

.mode csv
.import ../GlobalTemperatures.csv Temperatures
select * from Temperatures ORDER BY dt DESC limit 1;
delete from Temperatures ORDER BY dt DESC limit 1;
select * from Temperatures DESC limit 1;
delete from Temperatures where LandAverageTemperature="";

CREATE TABLE LandTemperaturesByState(
   dt                               DATE                 NOT NULL,
   AverageTemperature               double precision     NOT NULL,
   AverageTemperatureUncertainty    double precision     NOT NULL,
   State                            nvarchar(1000)       NOT NULL,
   Country                          nvarchar(1000)       NOT NULL
);

.mode csv
.import ../GlobalLandTemperaturesByState.csv LandTemperaturesByState
select * from LandTemperaturesByState ORDER BY dt DESC limit 1;
delete from LandTemperaturesByState ORDER BY dt DESC limit 1;
select * from LandTemperaturesByState limit 1;
delete from LandTemperaturesByState where AverageTemperature="";

CREATE TABLE LandTemperaturesByMajorCity(
   dt                               DATE                 NOT NULL,
   AverageTemperature               double precision     NOT NULL,
   AverageTemperatureUncertainty    double precision     NOT NULL,
   City                             nvarchar(1000)       NOT NULL,
   Country                          nvarchar(1000)       NOT NULL,
   Latitude                         nvarchar(1000)       NOT NULL,
   Longitude                        nvarchar(1000)       NOT NULL
);

.mode csv
.import ../GlobalLandTemperaturesByMajorCity.csv LandTemperaturesByMajorCity
select * from LandTemperaturesByMajorCity ORDER BY dt DESC limit 1;
delete from LandTemperaturesByMajorCity ORDER BY dt DESC limit 1;
select * from LandTemperaturesByMajorCity limit 1;
delete from LandTemperaturesByMajorCity where AverageTemperature="";

CREATE TABLE LandTemperaturesByCountry(
   dt                               DATE                 NOT NULL,
   AverageTemperature               double precision     NOT NULL,
   AverageTemperatureUncertainty    double precision     NOT NULL,
   Country                          nvarchar(1000)       NOT NULL
);

.mode csv
.import ../GlobalLandTemperaturesByCountry.csv LandTemperaturesByCountry

select * from LandTemperaturesByCountry ORDER BY dt DESC limit 1;
delete from LandTemperaturesByCountry ORDER BY dt DESC limit 1;
select * from LandTemperaturesByCountry limit 1;
delete from LandTemperaturesByCountry where AverageTemperature="";

CREATE TABLE LandTemperaturesByCity(
   dt                               DATE                 NOT NULL,
   AverageTemperature               double precision     NOT NULL,
   AverageTemperatureUncertainty    double precision     NOT NULL,
   City                             nvarchar(1000)       NOT NULL,
   Country                          nvarchar(1000)       NOT NULL,
   Latitude                         nvarchar(1000)       NOT NULL,
   Longitude                        nvarchar(1000)       NOT NULL
);

.mode csv
.import ../GlobalLandTemperaturesByCity.csv LandTemperaturesByCity

select * from LandTemperaturesByCity ORDER BY dt DESC limit 1;
delete from LandTemperaturesByCity ORDER BY dt DESC limit 1;
select * from LandTemperaturesByCity limit 1;
delete from LandTemperaturesByCity where AverageTemperature="";
