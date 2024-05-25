import pika
from influxdb import InfluxDBClient

rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
rabbitmq_channel = rabbitmq_connection.channel()
rabbitmq_channel.queue_declare(queue='performance')


influx_client = InfluxDBClient(host='localhost', port=8086)
influx_client.switch_database('memory_data')

def callback(ch, method, properties, body):
    performance_metric = float(body)
    data = [
        {
            "measurement": "memory_usage",  
            "tags": {
                "location": "server"
            },
            "fields": {
                "value": memory_data
            }
        }
    ]
    influx_client.write_points(data)
    print(f"Written to InfluxDB: {memory_data}")

rabbitmq_channel.basic_consume(queue='performance', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
rabbitmq_channel.start_consuming()