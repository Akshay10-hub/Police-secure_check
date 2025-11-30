import streamlit as st
import pandas as pd
import mysql.connector

# --------------------------
# DATABASE CONNECTION
# --------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ak47@123",
        port=3306,     
        database="securecheck"
    )

# --------------------------
# RUN SQL AND RETURN DF
# --------------------------
def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --------------------------
# STREAMLIT UI
# --------------------------
st.title("🚓 Traffic Stop Analytics Dashboard")
st.write("Choose a question below to see the answer using SQL queries.")

menu = st.selectbox(
    "Select a Question",
    [
        "What are the top 10 vehicle_Number involved in drug-related stops?",
        "Which vehicles were most frequently searched?",
        "Which driver age group had the highest arrest rate?",
        "Gender distribution of drivers stopped in each country",
        "Which race and gender combination has the highest search rate?",
        "What time of day sees the most traffic stops?",
        "What is the average stop duration for different violations?",
        "Are stops during the night more likely to lead to arrests?",
        "Which violations are most associated with searches or arrests?",
        "Which violations are most common among younger drivers (<25)",
        "Is there a violation that rarely results in search or arrest?",
        "Which countries report the highest rate of drug-related stops?",
        "What is the arrest rate by country and violation?",
        "Which country has the most stops with search conducted?",
        "Yearly Breakdown of Stops and Arrests by Country",
        "Driver Violation Trends Based on Age and Race",
        "Time Period Analysis of Stops (Number of Stops by Year, Month, Hour of the Day",
        "Violations with High Search and Arrest Rate",
        "Driver Demographics by Country",
        "Top 5 Violations with Highest Arrest Rates"
    ]
)
# -----------------------------------------------------------
# QUERY HANDLING FOR EACH QUESTION
# -----------------------------------------------------------

# 1. Top 10 vehicle_Number involved in drug-related stops
if menu == "What are the top 10 vehicle_Number involved in drug-related stops?":
    query = """
SELECT 
    vehicle_number,
    COUNT(*) AS search_count
FROM police_logs
WHERE search_conducted = TRUE
GROUP BY vehicle_number
ORDER BY search_count DESC
LIMIT 10;
"""
    df = run_query(query)
    st.subheader("Top 10 vehicle_Number involved in drug-related stops")
    st.dataframe(df)

#2 Which vehicles were most frequently searched
if menu == "Which vehicles were most frequently searched?":
    query = """
SELECT 
    vehicle_number,
    COUNT(*) AS search_count
FROM police_logs
WHERE search_conducted = TRUE
GROUP BY vehicle_number
ORDER BY search_count DESC
LIMIT 1;
"""
    df = run_query(query)
    st.subheader("Most frequently searched vehicle")
    st.dataframe(df)

# 4. Driver Age group with highest arrest rate
elif menu == "Which driver age group had the highest arrest rate? ":
    query = """
SELECT 
    CASE
        WHEN driver_age < 18 THEN 'Under 18'
        WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
        WHEN driver_age BETWEEN 26 AND 35 THEN '26-35'
        WHEN driver_age BETWEEN 36 AND 45 THEN '36-45'
        WHEN driver_age BETWEEN 46 AND 60 THEN '46-60'
        WHEN driver_age > 60 THEN '60+'
    END AS age_group,
    COUNT(*) AS total_stops,
    SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS arrest_count,
    (SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) / COUNT(*)) * 100
        AS arrest_rate_percent

FROM police_logs
GROUP BY age_group
ORDER BY arrest_rate_percent DESC
LIMIT 1;
"""
    df = run_query(query)
    st.subheader("Driver Age Group With Highest Arrest Rate")
    st.dataframe(df)

# 5. Gender distribution of drivers stopped in each country
elif menu == "What is the gender distribution of drivers stopped in each country?":
    query = """
SELECT 
    country_name,
    driver_gender,
    COUNT(*) AS total_count
FROM police_logs
GROUP BY country_name, driver_gender
ORDER BY country_name, driver_gender;
"""
    df = run_query(query)
    st.subheader("Gender Distribution per Country")
    st.dataframe(df)

# 6. Which race and gender combination has the highest search rate?
elif menu == "Race & Gender combination with highest search rate":
    query = """
SELECT 
    driver_race,
    driver_gender,
    AVG(search_conducted) AS search_rate
FROM police_logs
GROUP BY driver_race, driver_gender
ORDER BY search_rate DESC
LIMIT 1;
"""
    df = run_query(query)
    st.subheader("Race + Gender Combination With Highest Search Rate")
    st.dataframe(df)

# 7. What time of day sees the most traffic stops?
elif menu == "What time of day sees the most traffic stops?":
    query = """
SELECT 
    HOUR(timestamp) AS hour_of_day,
    COUNT(*) AS stop_count
FROM police_logs
GROUP BY hour_of_day
ORDER BY stop_count DESC
LIMIT 1;
"""
    df = run_query(query)
    st.subheader("Traffic Stops by Hour of Day")
    st.bar_chart(df.set_index("hour"))

# 8. What is the average stop duration for different violations?
elif menu == "What is the average stop duration for different violations?":
    query = """
SELECT 
    violation,
    AVG(
        CASE stop_duration
            WHEN '0-5 Min' THEN 2.5
            WHEN '6-15 Min' THEN 10
            WHEN '16-30 Min' THEN 23
            WHEN '31-60 Min' THEN 45
            ELSE 10
        END
    ) AS avg_duration
FROM police_logs
GROUP BY violation
ORDER BY avg_duration DESC;
"""
    df = run_query(query)
    st.subheader("Average Stop Duration For Different Violation")
    st.dataframe(df)

# 9. Are stops during the night more likely to lead to arrests? 
elif menu == "Are stops during the night more likely to lead to arrests?":
    query = """
SELECT 
    CASE 
        WHEN TIME(stop_time) BETWEEN '19:00:00' AND '23:59:59' # Night 7pm to 12 pm
             OR TIME(stop_time) BETWEEN '00:00:00' AND '05:00:00' 
            THEN 'Night'
        ELSE 'Day'
    END AS time_period,
    
    COUNT(*) AS total_stops,
    
    SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS total_arrests
FROM police_logs
GROUP BY time_period;
"""
    df = run_query(query)
    st.subheader("Is Night more likely lead to arrest")
    st.bar_chart(df.set_index("hour"))

# 10. Which violations are most associated with searches or arrests?
elif menu == "Which violations are most associated with searches or arrests?":
    query = """
SELECT 
    violation,
    SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS search_count,
    SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS arrest_count,
    SUM(CASE 
        WHEN search_conducted = TRUE OR stop_outcome = 'Arrest' 
        THEN 1 ELSE 0 END
    ) AS total_associated
FROM police_logs
GROUP BY violation
ORDER BY total_associated DESC
LIMIT 3;
"""
    df = run_query(query)
    st.subheader("Most associated with searches or assets")
    st.dataframe(df)

# 11. Which violations are most common among younger drivers (<25)?
if menu == "Which violations are most common among younger drivers (<25)":
    query = """
SELECT 
    violation,
    COUNT(*) AS violation_count
FROM police_logs
WHERE driver_age < 25
GROUP BY violation
ORDER BY violation_count DESC
LIMIT 1;
""" 
    query_sample = """
SELECT 
    driver_age, driver_gender, violation, stop_time, 
    search_conducted, stop_outcome, stop_duration
FROM police_logs
WHERE driver_age < 25 AND violation = %s
LIMIT 1;
"""
    df = run_query(query)
    st.subheader("Most common violation among younder driver (<25)")
    st.dataframe(df)

# 12. Is there a violation that rarely results in search or arrest?
if menu == "Is there a violation that rarely results in search or arrest?":
    query = """
SELECT 
    violation,
    AVG(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS search_rate,
    AVG(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS arrest_rate
FROM police_logs
GROUP BY violation
ORDER BY (search_rate + arrest_rate) ASC
LIMIT 1;
"""
    df = run_query(query)
    st.subheader("Violation that rarely results in search or arrest")
    st.dataframe(df)

# 13.  Which countries report the highest rate of drug-related stops?
if menu == "Which countries report the highest rate of drug-related stops?":
    query = """
SELECT 
    country_name,
    COUNT(*) AS total_stops,
    SUM(CASE WHEN drugs_related_stop = TRUE THEN 1 ELSE 0 END) AS drug_related_stops,
    ROUND(
        SUM(CASE WHEN drugs_related_stop = TRUE THEN 1 ELSE 0 END) 
        / COUNT(*) * 100, 2
    ) AS drug_related_rate
FROM police_logs
GROUP BY country_name
ORDER BY drug_related_rate DESC;
"""
    df = run_query(query)
    st.subheader("Highest country rate of drug-related stops")
    st.dataframe(df)

# 14. What is the arrest rate by country and violation?
elif menu == "What is the arrest rate by country and violation?":
    query = """
    SELECT 
        country_name,
        violation,
        SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS arrest_count,
        COUNT(*) AS total_stops,
        ROUND(
            (SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) / COUNT(*)) * 100,2
        ) AS arrest_rate
    FROM police_logs
    GROUP BY country_name, violation
    ORDER BY arrest_rate DESC;
    """
    df = run_query(query)
    st.subheader("Arrest rate by country and violation")
    st.dataframe(df)

# 15. Which country has the most stops with search conducted?
if menu == "Which country has the most stops with search conducted?":
    query = """
SELECT 
    country_name,
    COUNT(*) AS total_searches
FROM police_logs
WHERE search_conducted = TRUE
GROUP BY country_name
ORDER BY total_searches DESC
LIMIT 1;
"""
    df = run_query(query)
    st.subheader("Most search conducted country")
    st.dataframe(df)

# Complex 1. Yearly Breakdown of Stops and Arrests by Country (Using Subquery & Window function)
elif menu == "Yearly Breakdown of Stops and Arrests by Country":
    query = """
    WITH yearly_data AS (
        SELECT
            YEAR(stop_date) AS year,
            COUNT(*) AS total_stops,
            SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS total_arrests
        FROM police_logs
        GROUP BY YEAR(stop_date)
    ),
    yearly_window AS (
        SELECT
            year,
            total_stops,
            total_arrests,
            total_arrests / total_stops AS arrest_rate,
            SUM(total_arrests) OVER (ORDER BY year) AS cumulative_arrests
        FROM yearly_data
    )
    SELECT *
    FROM yearly_window
    ORDER BY year;
    """
    df = run_query(query)
    st.subheader("Yearly Breakdown of Stops and Arrests by Country")
    st.dataframe(df)

# Complex 2. Driver Violation Trends Based on Age and Race (Join with Subquery)
elif menu == "Driver Violation Trends Based on Age and Race":
    query = """
SELECT 
    v.driver_age_group,
    v.driver_race,
    v.violation,
    v.total_stops,
    s.search_rate
FROM
    (SELECT 
        CASE 
            WHEN driver_age < 25 THEN 'Under 25'
            WHEN driver_age BETWEEN 25 AND 40 THEN '25-40'
            WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
            ELSE '60+' 
        END AS driver_age_group,
        driver_race,
        violation,
        COUNT(*) AS total_stops
     FROM police_logs
     GROUP BY driver_age_group, driver_race, violation
    ) AS v
LEFT JOIN
    (SELECT 
        CASE 
            WHEN driver_age < 25 THEN 'Under 25'
            WHEN driver_age BETWEEN 25 AND 40 THEN '25-40'
            WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
            ELSE '60+' 
        END AS driver_age_group,
        driver_race,
        violation,
        AVG(search_conducted) AS search_rate
     FROM police_logs
     GROUP BY driver_age_group, driver_race, violation
    ) AS s
ON v.driver_age_group = s.driver_age_group
AND v.driver_race = s.driver_race
AND v.violation = s.violation
ORDER BY total_stops DESC;
"""
    df = run_query(query)
    st.subheader("Most search conducted country")
    st.dataframe(df)

# Complex 3. Time Period Analysis of Stops (Joining with Date Functions) , Number of Stops by Year, Month, Hour of the Day
elif menu == "Time Period Analysis of Stops (Number of Stops by Year, Month, Hour of the Day)":
    query_year = """
SELECT 
    YEAR(stop_date) AS stop_year,
    COUNT(*) AS total_stops
FROM police_logs
GROUP BY YEAR(stop_date)
ORDER BY stop_year;
"""
    query_month = """
SELECT 
    MONTH(stop_date) AS stop_month,
    COUNT(*) AS total_stops
FROM police_logs
GROUP BY MONTH(stop_date)
ORDER BY stop_month;
"""
    query_hour = """
SELECT 
    HOUR(stop_time) AS stop_hour,
    COUNT(*) AS total_stops
FROM police_logs
GROUP BY HOUR(stop_time)
ORDER BY stop_hour;
"""
    df = run_query(query)
    st.subheader("Time period Analysis of stop")
    st.bar_chart(df.set_index("hour"),("month"),("year"))

# Complex 4. Violations with High Search and Arrest Rates (Window Function)
elif menu == "Violations with High Search and Arrest Rate":
    query = """
    WITH stats AS (
        SELECT
            violation,
            COUNT(*) AS total_stops,
            SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS total_searches,
            SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS total_arrests
        FROM police_logs
        GROUP BY violation
    ),
    rates AS (
         SELECT
             violation,
             total_stops,
             total_searches,
             total_arrests,
             (total_searches * 100.0 / total_stops) AS search_rate,
             (total_arrests * 100.0 / total_stops) AS arrest_rate,
             RANK() OVER (ORDER BY (total_searches * 100.0 / total_stops) DESC) AS search_rank,
             RANK() OVER (ORDER BY (total_arrests * 100.0 / total_stops) DESC) AS arrest_rank
        FROM stats
    )
    SELECT *
    FROM rates
    ORDER BY search_rank, arrest_rank;
    """
    df = run_query(query)
    st.subheader("Most search conducted country")
    st.dataframe(df)

# Complex 5. Driver Demographics by Country (Age, Gender, and Race)
elif menu == "Driver Demographics by Country":
    query = """
WITH age_groups AS (
    SELECT 
        id,
        CASE 
            WHEN driver_age < 18 THEN 'Under 18'
            WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
            WHEN driver_age BETWEEN 26 AND 40 THEN '26-40'
            WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
            ELSE '60+'
        END AS age_group,
        driver_age,
        driver_race,
        violation,
        search_conducted
    FROM police_logs
),
race_violations AS (
    SELECT 
        age_group,
        driver_race,
        violation,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS searches,
        (SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS search_rate
    FROM age_groups
    GROUP BY age_group, driver_race, violation
)
SELECT 
    age_group,
    driver_race,
    violation,
    total_stops,
    searches,
    ROUND(search_rate, 2) AS search_rate
FROM race_violations
ORDER BY search_rate DESC
LIMIT 10;
"""
    df = run_query(query)
    st.subheader("Driver Demographics by Country")
    st.dataframe(df)

# Complex 6. Top 5 Violations with Highest Arrest Rates
elif menu == "Top 5 Violations with Highest Arrest Rates":
    query = """
SELECT 
    violation,
    COUNT(*) AS total_stops,
    SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS arrest_count,
    ROUND(
        (SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) / COUNT(*)) * 100,
        2
    ) AS arrest_rate
FROM police_logs
GROUP BY violation
ORDER BY arrest_rate DESC
LIMIT 5;
"""
    df = run_query(query)
    st.subheader("Top 5 Violations with Highest Arrest Rate")
    st.dataframe(df)
















