SELECT 
    TO_CHAR(dropoff_event.created_at, 'YYYY-MM') AS month,
    CONCAT(driver.first_name, ' ', driver.last_name) AS driver,
    COUNT(*) AS count_of_trips_over_1hr
FROM ride_rideevent AS pickup_event
JOIN ride_rideevent AS dropoff_event 
    ON pickup_event.id_ride_id = dropoff_event.id_ride_id
    AND pickup_event.description = 'Status changed to pickup'
    AND dropoff_event.description = 'Status changed to dropoff'
    AND dropoff_event.created_at > pickup_event.created_at
JOIN ride_ride AS ride ON ride.id = pickup_event.id_ride_id
JOIN core_user AS driver ON driver.id = ride.id_driver_id
WHERE dropoff_event.created_at - pickup_event.created_at > interval '1 hour'
GROUP BY month, driver
ORDER BY month, driver;