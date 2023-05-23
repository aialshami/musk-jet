"""Tests for transform module and it's utility functions."""
from datetime import datetime, timedelta
from psycopg2.extensions import connection
from transform import *
from utilities import haversine_distance, find_nearest_airport, calculate_fuel_consumption


def test_antipodal_haversine_distance_is_half_circumference_of_earth():
    """Check that Haversine distance between the poles is equal to half the
    circumference of the earth."""
    assert round(haversine_distance(-90, 135, 90, -45)) == 20015


def test_haversine_distance_between_same_points_is_zero():
    """Check that the Haversine distance between a point and itself is 0."""
    assert haversine_distance(17, 17, 17, 17) == 0


def test_haversine_distance():
    """Test the Haversine distance between two points."""
    assert round(haversine_distance(-18, 35, 72, -40)) == 11407


def test_find_nearest_airport_BER(airport_data):
    """Checks that when the lat/lon of BER is input to the find_nearest_airport
    function, BER is returned."""
    assert find_nearest_airport(52.36, 13.51, airport_data) == "BER"


def test_find_nearest_airport_WKK(airport_data):
    """Checks that when the lat/lon of WKK is input to the find_nearest_airport
    function, WKK is returned."""

    assert find_nearest_airport(59.3, -158.61, airport_data) == "WKK"


def test_fuel_usage_of_LJ40_over_one_hour(aircraft_data):
    """Tests the fuel usage of LJ40 jet over a single hour."""
    test_dep_time = datetime.now() - timedelta(hours=1)
    test_arr_time = datetime.now()
    assert calculate_fuel_consumption(test_dep_time, test_arr_time, "LJ40", aircraft_data) == 207


def test_fuel_usage_of_GA5C(aircraft_data):
    """Tests the fuel usage of GA5C jet over 7 hours 43 minutes and 27 seconds."""
    test_dep_time = datetime.now() - timedelta(hours=7, minutes=42, seconds=87)
    test_arr_time = datetime.now()
    assert round(calculate_fuel_consumption(test_dep_time, test_arr_time, "GA5C", aircraft_data)) == 3105


def test_staging_db_connection(staging_db_connection):
    """Checks the connection to the staging database."""
    assert isinstance(staging_db_connection, connection)


def test_production_db_connection(production_db_connection):
    """Checks the connection to the production database."""
    assert isinstance(production_db_connection, connection)


def test_load_airport_data_from_s3(airport_data):
    """Checks that the airport data is successfully retrieved from S3."""
    assert isinstance(airport_data, dict) and "iata" in list(airport_data.values())[0]


def test_load_aircraft_data_from_s3(aircraft_data):
    """Checks that the aircraft data is successfully retrieved from S3."""
    assert isinstance(aircraft_data, dict) and "galph" in list(aircraft_data.values())[0]
