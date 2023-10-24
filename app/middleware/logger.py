from fastapi.routing import APIRoute
from fastapi import Request, Response
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('app.log')
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


class CustomAPIRoute(APIRoute):
    async def get_route_handler(self):
        original_route_handler = await super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            logger.info(f"route duration: {duration}")
            logger.info(f"route response: {response}")
            logger.info(f"route response headers: {response.headers}")
            return response

        return custom_route_handler
    

