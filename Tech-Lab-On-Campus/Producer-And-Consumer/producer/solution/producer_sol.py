from producer_interface import mqProducerInterface
import pika
import os


class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str):
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        
    def setupRMQConnection(self):
        #Build our connection to the RMQ Connection.
        #The AMPQ_URL is a string which tells pika the package the URL of our AMPQ service in this scenario RabbitMQ.
        conParams = pika.URLParameters(os.environ['AMQP_URL'])
        self.connection = pika.BlockingConnection(parameters=conParams)
        self.channel = self.connection.channel()
        self.channel.exchange_declare('Test Exchange')

    # def publishOrder(self, message: str):
        #We can then publish data to that exchange using the basic_publish method
        # self.channel.basic_publish('Test Exchange', 'Test_route', 'Hi',...)

        # print(f'Message Published {self.routing_key}')
        
        # self.channel.close()
        
        
        