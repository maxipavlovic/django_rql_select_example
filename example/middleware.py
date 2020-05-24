from django.db import connection
from django.http import HttpResponse


class ProfileSQLMiddleware:
    @staticmethod
    def can_profile(request):
        return 'profile_sql=true' in request.META['QUERY_STRING']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if self.can_profile(request):
            return HttpResponse('\n'.join([
                sql_row['sql'] for sql_row in connection.queries
            ]))

        return response
