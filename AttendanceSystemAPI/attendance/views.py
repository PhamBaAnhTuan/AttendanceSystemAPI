

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated

# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer

# from .models import Message


# class MessageSendAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         message_text = request.data.get("message", "")
#         if not message_text:
#             return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

#         # Lưu message
#         msg = Message.objects.create(user=request.user, message={"message": message_text})

#         # Gửi sự kiện tới consumer
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             f"{request.user.id}-message", {
#                 "type": "send_last_message",
#                 "text": "new message"
#             }
#         )

#         print(f"[View] Created Message ID: {msg.id}")
#         return Response({"status": True, "id": msg.id}, status=status.HTTP_201_CREATED)

# from rest_framework.viewsets import ModelViewSet
# from django.contrib.auth.models import User
# from user.serializers import UserSerializers


# class UserViewSet(ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializers