from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

class ContactFormView(APIView):
    permission_classes = []  # public endpoint

    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        phone = request.data.get("phone", "N/A")
        subject = request.data.get("subject")
        message = request.data.get("message")

        if not name or not email or not message:
            return Response({"message": "Please fill in all required fields."}, status=status.HTTP_400_BAD_REQUEST)

        full_message = f"""
        New message from The Checklist Co. Contact Form
        
        Name: {name}
        Email: {email}
        Phone: {phone}
        Subject: {subject}
        
        Message:
        {message}
        """

        try:
            send_mail(
                subject=f"Contact Form Submission: {subject}",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,      # from your Zoho
                recipient_list=["css@thechecklistco.in"],   # to your Zoho inbox
                fail_silently=False,
            )
            return Response({"message": "Message sent successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)