-- SELECT * FROM satellite
-- WHERE satellite.name == '0 HST';

SELECT * from satellite
WHERE id == 809;


SELECT * from lines
WHERE lines.satellite_id == 809;