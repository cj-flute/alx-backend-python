import logging
from datetime import datetime
import time
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from collections import defaultdict


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        # get_respose is the next middleware or the view
        self.get_response = get_response

        # configure logging: log into requests.log
        logging.basicConfig(
            filename="requests.log",
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


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        pass

    def __call__(self, request):
        # Get current hour in 24 hr format
        current_hour = datetime.now().hour

        # Allow only between 6AM(06:00) and 9PM(21:00)
        if not (6 <= current_hour < 21):
            return HttpResponseForbidden("Access retricted. Please try between 6AM and 9PM.")

        # Otherwise, continue witht request
        response = self.get_response(request)
        return response


# Block offensive messages and set message limitation
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # { ip: [timestamps_of_requests] }
        self.requests_log = defaultdict(list)

    def __call__(self, request):
        if request.method == "POST" and "/messages" in request.path:
            ip = self.get_client_ip(request)
            now = time.time()

            # Remove timestamp older than 60 seconds
            self.requests_log[ip] = [
                ts for ts in self.requests_log[ip] if now - ts < 60
            ]

        # Check how many requests remain within 60 seconds
        if len(self.requests_log[ip]) >= 5:
            return JsonResponse(
                {"detail": "Rate limit exceeded. Max 5 messages per minute."},
                status=429
            )

        # Log this request
        self.requests_log[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Help to extract client IP address"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARD_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        pass

    def __call__(self, request):
        # Only check when the user is authenticated
        if request.user.is_authenticated:
            # block access to admin-only endpoints
            if "/admin-only/" in request.path or "/restricted/" in request.path:
                if not (request.user.is_staff or request.user.is_superuser):
                    return JsonResponse(
                        {"detail": "You do not have permission to access this resource."},
                        status=403
                    )
        response = self.get_response(request)
        return response
