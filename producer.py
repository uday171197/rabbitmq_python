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
    
    def __init__(self,queue = 'hello',host = 'localhost',exchange = '',routing_key = 'hello') -> None:
        self.queue = queue
        self.host = host
        self.exchange = exchange
        self.routing_key = routing_key
        pass

class RabbitMQ:
    __slots__ = ['_connection','_channel','config']
    def __init__(self,config) -> None:
        self.config = config
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.config.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.config.queue)
        
    def __enter__(self):
        print('__enter__ callling ..........')
        # self._connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.config.host))
        return self
        
    def __exit__(self,exc_type,exc_val,exc_tb):
        print('__exit__ callling ..........')
        self._connection.close()
        
    def producer(self,payload):
        self._channel.basic_publish(exchange = self.config.exchange,
                            routing_key = self.config.routing_key,
                            body = str(payload)
                            )
        
class Image(object):
    def __init__(self,filename) -> None:
        self._filename = filename
        
    @property
    def get(self):
        with open(self._filename,'rb') as f:
            data = f.read()
        return data
    
if __name__ == '__main__':
    config = RabbitMQConfigration(queue = 'hello',host = 'localhost',routing_key = 'hello')
    image = Image(filename = "/home/uday/Uday/pesonal/rabitmq/rabitmq_python/send.png")
    with RabbitMQ(config) as rabbitmqobject:
        rabbitmqobject.producer(payload=image.get)
    