-- 1. Find trips with battery drop >50% in <10 minutes (potential anomaly)
-- Why: Detects potential battery faults, software bugs in energy estimation, or sensor errors.
--   ~: A healthy battery shouldn't drop this fast. Could indicate a safetyissue or bad firmware calibration. 
	SELECT trip_id, vehicle_id, battery_start, battery_end, duration_min
	FROM trips
	WHERE (battery_start - battery_end) > 50 AND duration_min < 10;
    
-- 2. Count Autopilot disengagements per vehicle
-- Why: AP/FSD reliability metric. 
--   ~: High disengagments on specific vehicles flag hardware issues, software regressions, or edge-case fail needing investigation before OTA releases.
	SELECT vehicle_id, COUNT(*) AS disengagements
	FROM autopilot_events
	WHERE event_type = 'disengagement'
	GROUP BY vehicle_id
	ORDER BY disengagements DESC
	LIMIT 10;
    
-- 3. Sessions with GPS latency >500ms (navigation issue)
-- Why: Critical for navigation and Autopilot.
--   ~: High latency causes poor positioning, phantom braking, or map errors. Which are common customer complaints and safety concerns. 
	SELECT session_id, MAX(gps_latency_ms) AS max_latency
	FROM telemetry
	WHERE gps_latency_ms > 500
	GROUP BY session_id;
    
-- 4. Vehicles with temperature >60°C in battery pack (overheat risk)
-- Why: Overheating risks fire or degraded battery life.
--   ~: Used to catch cooling system bugs or extreme-condition software failures before they affect real vehicles.
	SELECT vehicle_id, timestamp, battery_temp_c
	FROM battery_logs
	WHERE battery_temp_c > 60
	ORDER BY battery_temp_c DESC;
    
-- 5. Compare UI-reported range vs calculated from DB
-- Why: Ensures the dashboard range disply matches backend calculation.
--   ~: Mismatch equals customer confusion or wrong energy management decisions. ( i.e. running out of charge unexpectedly ) 
	SELECT v.vehicle_id, v.ui_range_km, 
       (b.battery_level * v.max_range_km / 100) AS calculated_range
	FROM vehicles v
	JOIN battery_status b ON v.vehicle_id = b.vehicle_id
	WHERE ABS(v.ui_range_km - (b.battery_level * v.max_range_km / 100)) > 10;

-- 6. Find charging sessions that ended with <100% (interrupted)
-- Why: Identifies failed or aborted Supercharger or Home chargin sessions.
--   ~: Helps find bugs in charging logic, communication drops, or payment issues.
	SELECT session_id, vehicle_id, start_soc, end_soc
	FROM charging_sessions
	WHERE end_soc < 100 AND interrupted = 1;

-- 7. Daily average Supercharger usage
-- Why: Monitors infrastructure health and vehicle charging behavior.
--   ~: Sudden drops or spikes could indicate software throttling bugs or hardware degradation acroos the fleet.
	SELECT DATE(start_time) AS charge_date, AVG(power_kw) AS avg_power
	FROM supercharger_sessions
	GROUP BY charge_date
	ORDER BY charge_date DESC;
    
-- 8. Vehicles with >5 error codes in last 24 hours
-- Why: Early warning for problematic vehicles. 
--   ~: High error rates often precede customer support tickets or recalls. Use for proactive fleet monitoring. 
	SELECT vehicle_id, COUNT(*) AS error_count
	FROM error_logs
	WHERE timestamp > DATE_SUB(NOW(), INTERVAL 24 HOUR)
	GROUP BY vehicle_id
	HAVING error_count > 5;

-- 9. Phantom drain: Battery drop while parked >2% overnight
-- Why: Excessive drain when parked points to background process bugs ( i.e. sentry mode, app polling ) 
--   ~: Directly impacts customer satisfaction and range anxiety
	SELECT vehicle_id, battery_start, battery_end, parked_hours
	FROM parked_sessions
	WHERE (battery_start - battery_end) > 2 AND parked_hours > 8;
    
-- 10. Top 10 vehicles by total mileage
-- Why: Identifies "High-milage" customers for targeted testing.
--   ~: These vehicles have the most real-world data. Would be great for regression testing new firmware on aged batteries/hardware.	
    SELECT vehicle_id, SUM(distance_km) AS total_mileage
	FROM trips
	GROUP BY vehicle_id
	ORDER BY total_mileage DESC
	LIMIT 10;
 