from producer import RabbitMQConfigration


try:
    import pika 
    import ast
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
    __slots__ = ['_config','_connection','_channel']
    def __init__(self,config) -> None:
        self._config = config
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host = self._config.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue = self._config.queue)
        # print('send Message.............')

    def callback(self,ch,method,properties,body):
        print(f" Message Recieved !")
        data = body.decode('utf-8')
        payload = ast.literal_eval(data)
        with open('recieved1.png','wb') as f:
            f.write(payload)
        
    def consume(self):
        self._channel.basic_consume(
            queue = self._config.queue,
            on_message_callback = self.callback,
            auto_ack = self._config.auto_ack
        )
        print('[*] Waiting for message. To exit press CTRL+C')
        self._channel.start_consuming()
    
if __name__ == '__main__':
    conf = RabbitMQConfigration(queue = 'hello',host = 'localhost')
    consumer_obj = RabbitMQConsumer(conf)
    consumer_obj.consume()
    