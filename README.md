![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Selenium](https://img.shields.io/badge/Selenium-4.25-orange)
![SocketIO](https://img.shields.io/badge/Socket.IO-real--time-brightgreen)
![SQLite](https://img.shields.io/badge/SQLite-lightgrey)

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

## - !! End-to-End Mini-App project with Flask + SQLite !!
  Full-stack vehicle task tracker. Add tasks via UI -> save to DB -> list on page with LIVE refresh. Runs locally at http://127.0.0.1:5000.
  Target for full QA testing (manual, Postman, Selenium, SQL).
  - [Backend (Flask API + SQLite DB)](end-to-end-mini-project/app.py)
  - [Frontend UI (HTML + JavaScript)](end-to-end-mini-project/templates/index.html)
  - [Preview of running app with tasks added](end-to-end-mini-project/mini-app-preview.png)
### - QA Testing on created Mini-App
      - [Manual test cases (20 detailed scenarios, all PASSED)](end-to-end-mini-project/tests/manual/mini_app_manual_tests.xlsx)
      - [Preview of manual test sheet](end-to-end-mini-project/tests/manual/mini-app-manual-tests-preview.png)
      - [Postman API test collection - 8 requests with assertions](end-to-end-mini-project/tests/postman/mini_app_postman_test_run.json)
      - [Preview of API test collection results](end-to-end-mini-project/tests/postman/mini-app-api-test-preview.png)
      - [Selenium UI automation script ( adds 3 tasks, asserts, visibility and persistence )](end-to-end-mini-project/tests/selenium/test_mini_app_UI.py)
      - [Preview of Selenium tests results](end-to-end-mini-project/tests/selenium/selenium_mini_app_UI_preview.png)
      - [SQL validation queries on database created from Mini-App](end-to-end-mini-project/tests/sql/SQL_validation_results.py)
      - [Preview of SQL validation results ( executed via Python in CMD )](end-to-end-mini-project/tests/sql/mini_app_sql_validation.png)

### - Live QA Dashboard ( using the Mini-App ) 
      Full-stack dashboard (Flask + SocketIO) that runs all test suites with one click. Features live console streaming, run history, and DB logging of results.
      One-click to launch real Selenium UI automation: opens Chrome, adds tasks, asserts visibility/persistence, streams full output live.
      - [Dashboard app (Flask + SocketIO)](qa-dashboard/dashboard.py)
      - [Dashboard frontend (HTML + Tailwind + SocketIO client)](qa-dashboard/templates/index.html)
      - [Screenshot of dashboard running Selenium tests](qa-dashboard/Dashboard_Selenium_Preview.png)

Actively Updated: - January 2026
