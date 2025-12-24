# TESLA-QA-PORTFOLIO
Entry-Level Software QA portfolio for Tesla - manual tests, Postman API, Selenium Python automation, SQL validation ( built DEC 2025 )

Contains:

## - Manual test cases (Tesla mobile + in-car UI)
  Covers positive/negative scenarios, edge cases, security (SQL injection attempt), usability (biometric, offline, low battery), multi-device sessions, and Tesla-specific flows (Phone key, key card fallback, post-OTA login). 
  Includes high/medium priority classification and real-world user behaviors
  - [30 detailed test cases for Tesla mobile app & in-CAR login](manual-test-cases/manual-test-cases-github.xlsx)
  - [Preview of the 30 detailed test cases](manual-test-cases/manual-test-cases-preview.png)
  
## - Postman API collection with automated tests
  Simulates vehicle telemetry endpoints ( GET status, POST data, PUT config, DELETE logs ) using public mock API's, with JavaScript tests for status codes, response time, JSON schema, and specific fields.
  - [Tesla Vehicle API Test collection - 8 API requests with automated assertions](api-tests-postman/Tesla_Vehicle_API_Test.postman_collection.json)
  - [Preview of the test collection results](api-tests-postman/Postman-runner-result-preview.png)

## - Selenium Python UI automation suite
  Python script that uses the exact ID's ( 'form-input-identity' & 'form-submit-continue' ) from manually inspecting the Tesla signin page. Handles multi-step login flow ( email -> Next -> password ).
  - [Selenium Python script with 5 UI tests for Tesla account login using inspected element ID's](selenium-python-automation/test_tesla_login.py)
  - [Preview of the combined results (console output + browser state on Tesla login page + python code)](selenium-python-automation/selenium-results-preview.png)

## - SQL queries for telemetry and anomaly validation
  Covers battery anomalies, Autopilot events, GPS latency, overheating, range mismatch, phontom drains and more. 
  - [10 SQL queries for validating Tesla vehicle telemetry and anomaly detection](sql-validation-queries/tesla_telemetry_validation.sql)

## - End-to-end mini project with Flask + SQLite

Actively updated December 2025 
