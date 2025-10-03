import logging
from datetime import datetime


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        # get_respose is the next middleware or the view
        self.get_response = get_response

        # configure logging: log into request_logs.log
        logging.basicConfig(
            filename="resquest_logs.log",
            level=logging.INFO,
            format="%(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        # Get user (if authenticated) else "Anonymous"
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Prepare the log message
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"

        # Write to log file
        self.logger.info(log_message)

        # Continue processing the request
        response = self.get_response(request)
        return response
