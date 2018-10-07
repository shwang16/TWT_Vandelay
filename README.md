# TWT_Vandelay
application uses Flask and mysql, both hosted locally

to run application, type on command line:

export FLASK_APP=routing.py
flask run

application should show 
 * Serving Flask app "routing.py"
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

open http://127.0.0.1:5000/ on web browser
other endpoints include
/summary
/country/<country_name>
/make/<make_name>
/pr/less
/pr/more

Every time the home page is loaded, new data is retrieved from the API
From the home page, certain filters can be applied 
   showing data for a specific country
   showing data for a specific make
   showing data for a specific price range
The summary page includes graphs displaying data by country
   number of cars sold
   total profit
   average sale price

