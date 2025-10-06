# clients/api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password

from .models import Client, Service, ClientToken
from .serializers import ServiceSerializer, TimelineTaskSerializer

# Helper to get client from token header
def get_client_from_request(request):
    token_key = request.headers.get('X-Client-Token') or request.META.get('HTTP_X_CLIENT_TOKEN')
    if not token_key:
        return None
    try:
        token = ClientToken.objects.get(key=token_key)
    except ClientToken.DoesNotExist:
        return None
    return token.client

class ClientLoginView(APIView):
    permission_classes = []  # allow public

    def post(self, request):
        reference_id = request.data.get('reference_id')
        password = request.data.get('password')
        if not reference_id or not password:
            return Response({'message': 'reference_id and password required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = Client.objects.get(reference_id=reference_id, active=True)
        except Client.DoesNotExist:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, client.password):
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # create a fresh token and return
        # optional: clean old tokens for this client
        ClientToken.objects.filter(client=client).delete()
        token = ClientToken.objects.create(client=client)
        

        return Response({
            'token': token.key,
            'client': {'name': client.name, 'reference_id': client.reference_id}
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
def client_services(request, ref):
    """
    GET /api/client/<ref>/services/
    Require header: X-Client-Token: <token>
    """
    client = get_object_or_404(Client, reference_id=ref, active=True)
    # validate token
    token_key = request.headers.get('X-Client-Token') or request.META.get('HTTP_X_CLIENT_TOKEN')
    if not token_key:
        return Response({'message': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        token = ClientToken.objects.get(key=token_key, client=client)
    except ClientToken.DoesNotExist:
        return Response({'message': 'Invalid token.'}, status=status.HTTP_403_FORBIDDEN)

    services = Service.objects.filter(client=client).prefetch_related('timeline_tasks')
    serializer = ServiceSerializer(services, many=True)
    return Response({'services': serializer.data})


@api_view(['GET'])
def service_timeline(request, ref, service_id):
    """
    GET /api/client/<ref>/services/<service_id>/timeline/
    """
    client = get_object_or_404(Client, reference_id=ref, active=True)
    token_key = request.headers.get('X-Client-Token') or request.META.get('HTTP_X_CLIENT_TOKEN')
    if not token_key:
        return Response({'message': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        token = ClientToken.objects.get(key=token_key, client=client)
    except ClientToken.DoesNotExist:
        return Response({'message': 'Invalid token.'}, status=status.HTTP_403_FORBIDDEN)

    service = get_object_or_404(Service, id=service_id, client=client)
    milestones = service.timeline_tasks.all()
    mser = TimelineTaskSerializer(milestones, many=True)
    return Response({'service': {'id': service.id, 'title': service.title, 'status': service.status, 'milestones': mser.data}})