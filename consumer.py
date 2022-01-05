from producer import RabbitMQConfigration


try:
    import pika 
    print('Library installed')
except:
    raise MemoryError('The pika module is not install , `python3 -m pip  install pika`')

class MetaClass(type):
    _instance = {}
    def __call__(cls,*args,**krgs):
        """Singletone design pattern"""
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass,cls).__call__(*args,**krgs)
            return cls._instance[cls]

class RabbitMQConfigration(metaclass = MetaClass):
    def __init__(self,queue = 'hello',host = 'localhost') -> None:
        self.queue = queue
        self.host = host
        self.auto_ack = True
        pass

class RabbitMQConsumer:
    def __init__(self,config) -> None:
        self.config = config
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.config.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue = self.config.queue)

    def callback(self,ch,method,properties,body):
        print(f" [x] Recieved {body}")
        
    def consume(self):
        self.channel.basic_consume(
            queue = self.config.queue,
            on_message_callback = self.callback,
            auto_ack = self.config.auto_ack
        )
        print('[*] Waiting for message. To exit press CTRL+C')
        self.channel.start_consuming()
    
if __name__ == '__main__':
    conf = RabbitMQConfigration(queue = 'hello',host = 'localhost')
    consumer_obj = RabbitMQConsumer(conf)
    consumer_obj.consume()
    