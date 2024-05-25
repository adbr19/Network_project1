from influxdb import InfluxDBClient
import time
import psutil

client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('memory_data')

while True:

    memory_usage = psutil.virtual_memory().percent

    data = [
        {
            "measurement": "memory_usage",
            "tags": {
                "location": "memory"
            },
            "fields": {
                "value": memory_usage
            }
        }
    ]
    client.write_points(data)
    print(f"Written: {memory_usage} %")

    time.sleep(10)