import asyncio

from base_service import BaseService


class ServiceA(BaseService):
    @staticmethod
    async def calculation(data: dict):
        data = {"sum": {"a": 1, "b": 3, "equal": 4}}
        return data


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    service_a = ServiceA("ServiceB", "topic_B", loop)
    loop.run_until_complete(service_a.listen_and_respond())
