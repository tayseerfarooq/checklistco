# documents/api.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from clients.models import Client, ClientToken
from .models import Document

@api_view(['GET'])
def client_documents(request, ref):
    client = get_object_or_404(Client, reference_id=ref, active=True)
    token_key = request.headers.get('X-Client-Token') or request.META.get('HTTP_X_CLIENT_TOKEN')
    if not token_key:
        return Response({'message': 'Authentication credentials were not provided.'}, status=401)
    try:
        token = ClientToken.objects.get(key=token_key, client=client)
    except ClientToken.DoesNotExist:
        return Response({'message': 'Invalid token.'}, status=403)

    docs = Document.objects.filter(client=client).order_by('-uploaded_at')
    data = [{
        "id": d.id,
        "name": d.title,
        "category": getattr(d, 'category', ''),
        "uploaded_date": d.uploaded_at.isoformat(),
        "file_size": f"{d.file.size/1024:.2f} KB",
        "file_url": request.build_absolute_uri(d.file.url)
    } for d in docs]
    return Response({'documents': data})