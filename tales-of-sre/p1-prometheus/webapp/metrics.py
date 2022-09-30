from flask import Flask, jsonify, request
import http.client
import time

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client import Counter, Gauge

# Metrics definition

# HELP requests_total Count of requests
# TYPE requests_total counter
requests_counter = Counter('requests', 'Count of requests')
# HELP fetch_time_ms Time to fetch in milliseconds
# TYPE fetch_time_ms gauge
fetch_time_ms = Gauge('fetch_time_ms', 'Time to fetch in milliseconds')

app = Flask(__name__)

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

# Get something from the dummy service
def fetchSomething():
    connection = http.client.HTTPSConnection("httpbin.org")
    connection.request("GET", "/anything")
    response = connection.getresponse()
    print("Status: {} and reason: {}".format(response.status, response.reason))
    connection.close()

@app.route('/', methods = ['GET'])
def home():
    if(request.method == 'GET'):  
        # increment the request counter
        requests_counter.inc()

        # do something and record time
        start = time.time()
        fetchSomething()
        end = time.time()
        t = (end - start)*1000
        
        # set the metric value to time elapsed
        fetch_time_ms.set(t)

        data = f"fetch took {t} ms" 
        return jsonify({'msg': data})
  
  
# driver function
if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=9092)


