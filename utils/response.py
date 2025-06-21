from rest_framework.response import Response
from rest_framework import status

def success_response(data, code=status.HTTP_200_OK):
    return Response({'result': data, 'success': True}, status=code)
