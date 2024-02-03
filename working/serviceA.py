import asyncio

from base_service import BaseService


class ServiceA(BaseService):
    async def transit_calc(self, data: dict):
        data.update({"answer_to_topic": "topic_A", "method": "calculation"})
        response = await self.request("topic_B", data)
        response.update({"transit": "topic_A"})
        return response


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    service_a = ServiceA("ServiceA", "topic_A", loop)
    loop.run_until_complete(service_a.listen_and_respond())
