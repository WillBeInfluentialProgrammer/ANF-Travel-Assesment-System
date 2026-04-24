-- Complete database cleanup script for GTAS
-- This removes ALL flight, passenger, and message data

SET FOREIGN_KEY_CHECKS=0;

-- Message tables
TRUNCATE TABLE message;
TRUNCATE TABLE message_status;
TRUNCATE TABLE message_booking;
TRUNCATE TABLE apis_message;
TRUNCATE TABLE apis_message_passenger;
TRUNCATE TABLE pnr;
TRUNCATE TABLE pnr_passenger;

-- Flight tables
TRUNCATE TABLE flight;
TRUNCATE TABLE flight_leg;
TRUNCATE TABLE flight_passenger;
TRUNCATE TABLE flight_passenger_count;

-- Passenger tables
TRUNCATE TABLE passenger;
TRUNCATE TABLE passenger_details;
TRUNCATE TABLE passenger_details_from_message;
TRUNCATE TABLE passenger_trip_details;
TRUNCATE TABLE passenger_id_tag;
TRUNCATE TABLE passenger_notes;
TRUNCATE TABLE passenger_wl_timestamp;

-- Document tables
TRUNCATE TABLE document;
TRUNCATE TABLE travel_agency;
TRUNCATE TABLE address;
TRUNCATE TABLE credit_card;
TRUNCATE TABLE email;
TRUNCATE TABLE frequent_flyer;
TRUNCATE TABLE phone;
TRUNCATE TABLE seat;

-- Hit/Case tables
TRUNCATE TABLE hit_detail;
TRUNCATE TABLE hits_summary;
TRUNCATE TABLE cases;
TRUNCATE TABLE case_comments;
TRUNCATE TABLE attachment;

-- Bag tables
TRUNCATE TABLE bag;
TRUNCATE TABLE bag_measurement;
TRUNCATE TABLE flight_pax_bags;

-- Booking tables
TRUNCATE TABLE booking_detail;

-- Report tables
TRUNCATE TABLE reporting_party;

-- Other related tables
TRUNCATE TABLE mutable_flight_details;
TRUNCATE TABLE dwell_time;

SET FOREIGN_KEY_CHECKS=1;

SELECT 'Database completely cleaned - all data removed' as status;
