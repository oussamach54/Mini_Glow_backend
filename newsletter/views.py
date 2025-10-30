from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import NewsletterSubscriber

@api_view(['POST'])
def subscribe(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Adresse e-mail manquante.'}, status=status.HTTP_400_BAD_REQUEST)
    if NewsletterSubscriber.objects.filter(email=email).exists():
        return Response({'message': 'Déjà abonné !'}, status=status.HTTP_200_OK)
    NewsletterSubscriber.objects.create(email=email)
    return Response({'message': 'Merci pour votre inscription !'}, status=status.HTTP_201_CREATED)
