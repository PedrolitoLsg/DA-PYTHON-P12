from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from .models import Event, Contract, Customer, CustomUsers
from .serializers import ContractSerializer, CustomerSerializer, EventSerializer, CustomUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import HasCustomerPermission, HasEventPermission, HasContractPermission


class UserRegistrationView(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CustomUsers.objects.all()
    serializer_class = CustomUserSerializer

    '''creates a new user'''
    def create(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create_user(email=request.data['email'],
                                   last_name=request.data['last_name'],
                                   password=request.data['password'],
                                   first_name=request.data['first_name'],
                                   role=request.data['role'])
            userEmail = serializer.data.get('email')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class Customers(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # list all the customers
        instances = Customer.objects.all()
        serializer = CustomerSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.role != "Sales":
                message = str("Role is not correctly defined, note that Support can not create customers")
                return Response({'message':message}, status=status.HTTP_400_BAD_REQUEST)
            else:
                customer = serializer.save(sales=request.user)
                customer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Customer, id=kwargs['customer_id'])
        self.check_object_permissions(self.request, obj)
        instance = Customer.objects.get(id=kwargs['customer_id'])
        serializer = CustomerSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class SoloCustomer(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated, HasCustomerPermission]

    def retrieve(self, request, *args, **kwargs):
        instance = Customer.objects.get(id=kwargs['pk'])
        serializer = CustomerSerializer(instance, many=False)
        return Response(serializer, status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Customer, id=kwargs['customer_id'])
        self.check_object_permissions(self.request, obj)
        instance = Customer.objects.get(id=kwargs['customer_id'])
        serializer = CustomerSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        obj = get_object_or_404(Customer, id=kwargs['customer_id'])
        self.check_object_permissions(self.request, obj)
        self.perform_destroy(obj)
        message = 'You successfully deleted the Customer'
        return Response({'message': message},
                        status=status.HTTP_204_NO_CONTENT)


class Contracts(ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated]


    def list(self, request, *args, **kwargs):
        instances = Contract.objects.all()
        serializer = ContractSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.role != "Sales":
                message = str("Role is not correctly defined, not that Support can not create contracts")
                return Response({'message': message}, status=status.HTTP_200_OK)
            else:
                contract = serializer.save(sales=request.user)
                contract.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )


class SoloContract(ModelViewSet):
    serializer_class=ContractSerializer
    queryset = Contract.objects.all()
    permission_classes=[IsAuthenticated, HasContractPermission]

    def retrieve(self, request, *args, **kwargs):
        instance = Contract.objects.get(id=kwargs['contract_id'])
        serializer = ContractSerializer(instance, data=request.data)
        return Response(serializer, status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Contract, id=kwargs['contract_id'])
        self.check_object_permissions(self.request, obj)
        instance = Contract.objects.get(id=kwargs['contract_id'])
        serializer = ContractSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, ** kwargs):
        obj = get_object_or_404(Contract, id=kwargs['contract_id'])
        self.check_object_permissions(self.request, obj)
        self.perform_destroy(obj)
        message = 'You deleted the contract'
        return Response({'message': message},
                        status=status.HTTP_204_NO_CONTENT)




class Events(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        instances = Event.objects.all()
        serializer = EventSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.role != "Sales":
                message = str("Role is not correctly defined, not that Support can not create events")
                return Response({'message': message}, status=status.HTTP_200_OK)
            else:
                event = serializer.save()
                event.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )



class SoloEvent(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, HasEventPermission]

    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Event, id=kwargs['event_id'])
        self.check_object_permissions(self.request, obj)
        instance = Event.objects.get(id=kwargs['event_id'])
        serializer = EventSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, ** kwargs):
        obj = get_object_or_404(Event, id=kwargs['event_id'])
        self.check_object_permissions(self.request, obj)
        self.perform_destroy(obj)
        message = 'You deleted the event'
        return Response({'message': message},
                        status=status.HTTP_204_NO_CONTENT)

