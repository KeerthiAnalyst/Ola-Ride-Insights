CREATE DATABASE ola_ride_insights;

USE ola_ride_insights;

SELECT COUNT(*) AS total_records
FROM ola_bookings;


/*
Q1. Retrieve all successful bookings 
*/

SELECT *
FROM ola_bookings
WHERE Booking_Status = 'Success';


/*
Q2. Find the average ride distance for each vehicle type
*/

SELECT
    Vehicle_Type,
    ROUND(AVG(Ride_Distance), 2) AS Average_Ride_Distance
FROM ola_bookings
GROUP BY Vehicle_Type
ORDER BY Average_Ride_Distance DESC;

/*
Q3. Get the total number of cancelled rides by customers
*/
SELECT
    COUNT(*) AS Total_Customer_Cancellations
FROM ola_bookings
WHERE Booking_Status = 'Canceled by Customer';

/*
Q4. List the top 5 customers who booked the highest number of rides
*/
SELECT TOP 5
    Customer_ID,
    COUNT(Booking_ID) AS Total_Rides
FROM ola_bookings
GROUP BY Customer_ID
ORDER BY Total_Rides DESC;

/*
Q5.Get the number of rides cancelled by drivers due to personal and car-related issues
*/
SELECT
    COUNT(*) AS Driver_Cancellations
FROM ola_bookings
WHERE Canceled_Rides_by_Driver =
      'Personal & Car related issue';

/*
Q6. Find the maximum and minimum driver ratings for Prime Sedan bookings
*/
SELECT
    MAX(Driver_Ratings) AS Maximum_Rating,
    MIN(Driver_Ratings) AS Minimum_Rating
FROM ola_bookings
WHERE Vehicle_Type = 'Prime Sedan';

/*
Q7. Retrieve all rides where payment was made using UPI
*/

SELECT *
FROM ola_bookings
WHERE Payment_Method = 'UPI';

/*
Q8. Find the average customer rating per vehicle type
*/

SELECT
    Vehicle_Type,
    ROUND(AVG(Customer_Rating), 2) AS Average_Customer_Rating
FROM ola_bookings
GROUP BY Vehicle_Type
ORDER BY Average_Customer_Rating DESC;

/*
Q9. Calculate the total booking value of rides completed successfully
*/
SELECT
    SUM(Booking_Value) AS Total_Successful_Booking_Value
FROM ola_bookings
WHERE Booking_Status = 'Success';

/*
Q10. List all incomplete rides along with the reason
*/
SELECT
    Booking_ID,
    Customer_ID,
    Vehicle_Type,
    Booking_Status,
    Incomplete_Rides,
    Incomplete_Rides_Reason
FROM ola_bookings
WHERE Incomplete_Rides = 'Yes';
