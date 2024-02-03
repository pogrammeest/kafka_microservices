import asyncio

from base_service import BaseService


class ServiceA(BaseService):
    async def transit_calc(self, data: dict):
        data.update({"answer_to_topic": "topic_A", "method": "calculation"})
        future = await self.request("topic_B", data)
        print("STOP")
        # тут всё останавливается
        response = await future
        print("PLAY")
        print(f'Результат из `future`: {future.result()!r}')
        response.update({"transit": "topic_A"})
        return response


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    service_a = ServiceA("ServiceA", "topic_A", loop)
    loop.run_until_complete(service_a.listen_and_respond())

