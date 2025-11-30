Traffice Polie Securecheck
Step 1) Creating file named DSproject.ipynb in VS code, Import required libraries and load data to pandas df to work on dataset.
Step 2) Cleaning dataset by removing empty columns, filling missing values, and creating a proper timestamp column from date and time fields.
Step 3) Import pymysql to connect Python to a MySQL database.
Step 4) Connection from Python to your local MySQL server using your host, port, username, and password. Then, creating a database named securecheck.
Step 5) Creating a MySQL table named police_logs with columns matching your dataset, where each traffic stop will be stored as a structured row in the database.
Step 6) Again we are cleaning the dataset by removing any completely empty columns and filling missing values with defaults to ensure correct data before inserting into the database and displaying the cleaned data.
Step 7) Replacing all remaining NaN values in the DataFrame with None, ensuring the values can be inserted into MySQL without errors and converting the stop_date and stop_time columns into formatted strings to store correctly in MySQL.
Step 8) Creating a combined timestamp column by merging the cleaned stop_date and stop_time into a full datetime can be stored and used for time-based analysis.
Step 9) Preparing an SQL INSERT query that specifies how each row from my DataFrame will be inserted into the police_logs table in MySQL.
Step 10) Looping through each row of cleaned DataFrame and inserting that row into the MySQL table using INSERT query and saving all the inserted rows to the database, closing the MySQL connection, and confirming that the data was successfully stored.
Step 11) Once the final data is available, then moving on to SQL queries for solving one by one on the same file.
Step 12) As per project requirement, we are creating file named QNAstreamlit.py in VS code for displaying all the question and answer in Streamlit.
Step 13) Import required libraries  like streamlit, panda and mysql.connectorto connect my Streamlit app with the MySQL database.
Step 14) Creating a function that opens a connection to my MySQL database each time Streamlit needs to run a query.
Step 15) Creating a function that takes a SQL query, runs it on my MySQL database, converts the result into a DataFrame, and then closes the connection.
Step 16) Creating a function that takes a SQL query, runs it on my MySQL database, converts the result into a DataFrame, and then closes the connection. 
Step 17) Setting up the Streamlit page (Streamlit UI) by giving my dashboard a title and a short description so users can choose a question to run SQL analytics.
Step 18) Creating a dropdown menu that lets us choose which analytical question they want to run using SQL queries.
Step 19) Mention all question with matching SQL query to display it in streamlit.
Step 20) In terminal, run using the sentence “streamlit run QNAstreamlit.py (file_name). It will provide us with Streamlit app website link to access the given content.
