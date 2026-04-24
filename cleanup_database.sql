-- Complete Database Cleanup Script for GTAS
-- This will remove ALL data to avoid constraint violations and duplicates

SET FOREIGN_KEY_CHECKS=0;

-- Message and APIS/PNR related tables
TRUNCATE TABLE message;
TRUNCATE TABLE message_status;
TRUNCATE TABLE message_booking;
TRUNCATE TABLE apis_message;
TRUNCATE TABLE pnr;
TRUNCATE TABLE pnr_passenger;

-- Flight related tables
TRUNCATE TABLE flight;
TRUNCATE TABLE flight_leg;
TRUNCATE TABLE flight_direction;
TRUNCATE TABLE mutable_flight_details;

-- Passenger related tables
TRUNCATE TABLE passenger;
TRUNCATE TABLE flight_passenger;
TRUNCATE TABLE passenger_details;
TRUNCATE TABLE pax_watchlist_link;
TRUNCATE TABLE passenger_id_tag;
TRUNCATE TABLE passenger_trip_details;

-- Hit and case management tables
TRUNCATE TABLE hit_detail;
TRUNCATE TABLE hit_summary;
TRUNCATE TABLE hits_disposition;
TRUNCATE TABLE hits_disposition_comments;
TRUNCATE TABLE rule_hit_detail;

-- Document and address tables
TRUNCATE TABLE document;
TRUNCATE TABLE address;
TRUNCATE TABLE credit_card;
TRUNCATE TABLE email;
TRUNCATE TABLE phone;
TRUNCATE TABLE travel_agency;
TRUNCATE TABLE frequent_flyer;

-- Bag related tables
TRUNCATE TABLE bag;
TRUNCATE TABLE bag_measurement;
TRUNCATE TABLE flight_pax_bags;

-- Booking detail tables
TRUNCATE TABLE booking_detail;
TRUNCATE TABLE dwell_time;
TRUNCATE TABLE payment_form;
TRUNCATE TABLE reporting_party;

-- ATS message tables
TRUNCATE TABLE ats_message;

-- Seat information
TRUNCATE TABLE seat;
TRUNCATE TABLE flight_pax_seat;

-- Code share tables
TRUNCATE TABLE code_share_flight;

SET FOREIGN_KEY_CHECKS=1;

-- Verify cleanup
SELECT 'Cleanup Complete' as status;
SELECT 
    (SELECT COUNT(*) FROM message) as messages,
    (SELECT COUNT(*) FROM flight) as flights,
    (SELECT COUNT(*) FROM passenger) as passengers,
    (SELECT COUNT(*) FROM apis_message) as apis_messages;
