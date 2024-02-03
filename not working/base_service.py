import json
import random

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


class BaseService:
    def __init__(self, service_name, input_topic, loop):
        self.service_name = service_name
        self.loop = loop
        self._requests = {}
        self.input_topic = input_topic
        self.consumer = AIOKafkaConsumer(input_topic, loop=loop, group_id=service_name)
        self.producer = AIOKafkaProducer(loop=loop, bootstrap_servers='localhost:9092')

    async def process_message(self, data: dict, key):
        if key in self._requests:
            future = self._requests.pop(key)
            future.set_result(data)
            return
        if method := data.pop("method", None):
            if answer_to_topic := data.pop("answer_to_topic", None):
                method_result = await getattr(self, f"{method}")(data)
                print(f"Answer was sent to {answer_to_topic} with data: {method_result}")
                await self.producer.send_and_wait(answer_to_topic, json.dumps(method_result).encode("utf-8"), key=key)

    async def request(self, topic: str, data: dict, key: bytes = None):
        if key is None:
            key = random.randbytes(16)
        future = self.loop.create_future()
        self._requests[key] = future
        await self.producer.send_and_wait(topic, value=json.dumps(data).encode("utf-8"), key=key)
        return future

    async def listen_and_respond(self):
        await self.consumer.start()
        print("Consumer working ...")
        await self.producer.start()
        print("Producer working ...")
        try:
            async for message in self.consumer:
                message_value = message.value.decode('utf-8')
                message_data = json.loads(message_value)
                print("Topic:", self.input_topic, "Message:", message_data)
                await self.process_message(message_data, message.key)
        finally:
            await self.consumer.stop()
            await self.producer.stop()

