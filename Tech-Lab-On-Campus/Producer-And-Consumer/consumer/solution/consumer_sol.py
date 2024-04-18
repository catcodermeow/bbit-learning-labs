from consumer_interface import mqConsumerInterface  # pylint: disable=import-error
import os
import pika


class mqConsumer(mqConsumerInterface):
    def __init__ (self, binding_key:str, exchange_name:str, queue_name:str):
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.setupRMQConnection()
    
    def setupRMQConnection(self):
        #The AMPQ_URL is a string which tells pika the package the URL of our AMPQ service in this scenario RabbitMQ.
        conParams = pika.URLParameters(os.environ['AMQP_URL'])
        self.connection = pika.BlockingConnection(parameters=conParams)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(self.exchange_name)
        self.channel.queue_declare(self.queue_name)

        self.channel.queue_bind(exchange=self.exchange_name, routing_key=self.binding_key, queue=self.queue_name)

        #We can then consume data to that exchange using the basic_consume method
        self.channel.basic_consume(self.queue_name, on_message_callback=self.on_message_callback)

        self.startConsuming()

    def on_message_callback(
        self, channel, method_frame, header_frame, body
    ) :
        self.channel.basic_ack(method_frame.delivery_tag, False)
        print(f"{header_frame}\n\t{body}")
        self.channel.close()
 

    def startConsuming(self) :
        # Print " [*] Waiting for messages. To exit press CTRL+C"
        print(" [*] Waiting for messages. To exit press CTRL+C")

        # Start consuming messages
        self.channel.start_consuming()
    
    def __del__(self) :
        # Print "Closing RMQ connection on destruction"
        print("Closing RMQ connection on destruction")
        
        # Close Channel
        self.channel.close()

        # Close Connection
        self.connection.close()




    
