from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from marketplace.serializers import ConsumerRegistrationSerializer

class ConsumerRegistrationView(CreateAPIView):
    serializer_class = ConsumerRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"datail": "successfully created consumer"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
