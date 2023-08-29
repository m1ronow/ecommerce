import json
import uuid

import requests
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout, update_session_auth_hash

from .serializers import CustomUserSerializer, PaymentSerializer, ProductSerializer, CategorySerializer, \
    OrderSerializer, CartSerializer, CartItemSerializer, CartItemDetailSerializer, OrderItemSerializer, \
    LoginSerializer, UserProfileSerializer, UserAddressSerializer, ShippingMethodSerializer, PromoSerializer, \
    PaymentMethodSerializer, FavoritesItemSerializer, FavoritesItemDetailSerializer, ChangePasswordSerializer, \
    PromoActivationSerializer
from .models import CustomUser, UserAddress, UserProfile, Category, Product, Cart, CartItem, FavoritesItem, Order, \
    OrderItem, Payment, ShippingMethod, Promo, PaymentMethod, PromoActivation
from rest_framework import viewsets, status
from rest_framework import permissions
from .utils import create_assessment, check_email_syntax, validate_webhook_signature, create_coinbase_payment

import environ
env = environ.Env()
env.read_env()


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class LogoutView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        logout(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class AuthVerifyView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            return Response({'isAuthenticated': True})
        else:
            return Response({'isAuthenticated': False})


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        errors = []

        # Check email syntax
        if not check_email_syntax(email):
            errors.append('Email is not valid.')

        # Check password requirements
        if len(password) < 8 or not (any(c.islower() for c in password) and any(c.isupper() for c in password)):
            errors.append('Invalid password format.')

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        # Validate reCAPTCHA token
        recaptcha_token = request.data.get('captcha')
        recaptcha_action = 'submit'
        recaptcha_assessment_response = create_assessment(recaptcha_token, recaptcha_action)

        if recaptcha_assessment_response['tokenProperties']['valid']:
            self.perform_create(serializer)
            UserProfile.objects.create(user=serializer.instance)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'errors': ['reCAPTCHA validation failed']}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def me(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        else:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    # authenticates the user after creation
    def perform_create(self, serializer):
        user = serializer.save()
        login(self.request, user)

    @action(detail=False, methods=['patch'])
    def update_password(self, request):
        self.serializer_class = ChangePasswordSerializer
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = CustomUser.objects.get(id=request.user.id)

            # Check old password
            if not user.check_password(serializer.data.get("current_password")):
                response = {
                    'status': 'failed',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Wrong password',
                    'data': [],
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()
            update_session_auth_hash(request, user)
            response = {
                'status': 'success',
                'code': status.HTTP_202_ACCEPTED,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAddressViewSet(viewsets.ModelViewSet):
    serializer_class = UserAddressSerializer
    queryset = UserAddress.objects.all()

    @action(detail=False, methods=['get'])
    def me(self, request):
        queryset = UserAddress.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def update_me(self, request):
        data = request.data
        keys_list = ['id', 'user', 'url']
        for key in keys_list:
            data.pop(key, None)

        user_address, created = UserAddress.objects.update_or_create(user=request.user, defaults=data)
        serializer = self.get_serializer(user_address)

        if created:
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.current_address = serializer.instance
            user_profile.save()

        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user
        queryset = UserProfile.objects.filter(user=user)
        serializer = self.get_serializer(queryset.first())
        return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def update_me(self, request):
        data = request.data
        keys_list = ['id', 'user', 'url']
        for key in keys_list:
            data.pop(key, None)

        user_profile, created = UserProfile.objects.update_or_create(user=request.user, defaults=data)
        serializer = self.get_serializer(user_profile)

        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = None
        params = self.request.query_params
        if params:
            # firstly filtering
            category_id = params.get('category', None)
            min_price = params.get('min_price', None)
            max_price = params.get('max_price', None)
            filters = [
                Q(category=category_id) if category_id else None,
                Q(price__gte=min_price) if min_price else None,
                Q(price__lte=max_price) if max_price else None,
            ]
            # deleting None values
            filters = [i for i in filters if i is not None]

            queryset = Product.objects.filter(*filters)

            # then ordering
            order_by = params.get('order_by', None)
            if order_by:
                queryset = Product.objects.order_by(order_by) if queryset is None else queryset.order_by(order_by)

        if queryset is None:
            queryset = Product.objects.all()

        return queryset

    # overriding to add 'in_cart' and 'in_favorites' field
    def list(self, request, *args, **kwargs):
        products = self.get_queryset()

        page = self.paginate_queryset(products)
        cart_items = CartItem.objects.filter(cart__user=request.user.id).values_list('product_id', flat=True)
        favorites = FavoritesItem.objects.filter(user=request.user.id).values_list('product_id', flat=True)
        serializer = self.get_serializer(page, many=True)

        products_data = serializer.data
        for product in products_data:
            product['in_cart'] = product['id'] in cart_items
            product['in_favorites'] = product['id'] in favorites

        response_data = {
            'data': products_data,
            'currency': env('CURRENCY_CODE'),
        }

        return self.get_paginated_response(response_data)

    # the regex here matches any non-empty string that does not contain a slash or a period
    # @action(detail=False, methods=['GET'], url_path='filtered_by_category/(?P<category_id>[^/.]+)')
    # def filtered_by_category(self, request, category_id=None):
    #     queryset = self.filter_queryset(self.get_queryset().filter(category=category_id))
    #     serializer = self.get_serializer(queryset, many=True)
    #
    #     cart_items = CartItem.objects.filter(cart__user=request.user.id).values_list('product_id', flat=True)
    #     favorites = FavoritesItem.objects.filter(user=request.user.id).values_list('product_id', flat=True)
    #
    #     products_data = serializer.data
    #     for product in products_data:
    #         product['in_cart'] = product['id'] in cart_items
    #         product['in_favorites'] = product['id'] in favorites
    #
    #     return Response(products_data)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (permissions.AllowAny,)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return CartItemSerializer
        return CartItemDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(cart__user=self.request.user))
        serializer = self.get_serializer(queryset, many=True)

        # Get the currency value from the environment variable
        currency = env('CURRENCY_CODE')

        # Create the response dictionary with 'data' and 'currency' fields
        response_data = {
            'cart': serializer.data,
            'currency': currency,
        }

        return Response(response_data)

    def get_cart(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def perform_create(self, serializer):
        cart = self.get_cart()
        serializer.save(cart=cart)

    @action(detail=False, methods=['PATCH'], url_path='update_quantity')
    def update_quantity(self, request):
        cart = request.data
        user_cart = self.get_cart()

        updated_count = 0
        for product in cart:
            product_id = product.get('id')
            product_quantity = product.get('quantity')

            try:
                cart_item = CartItem.objects.get(cart=user_cart, id=product_id)
                if cart_item.quantity != product_quantity:
                    cart_item.quantity = product_quantity
                    cart_item.save()
                updated_count += 1
            except CartItem.DoesNotExist:
                pass

        return Response({'updated_count': updated_count})

    @action(detail=False, methods=['DELETE'], url_path='delete')
    def delete_items(self, request):
        product_ids = request.data.get('product_ids', [])
        cart = self.get_cart()
        deleted_count = CartItem.objects.filter(cart=cart, product__id__in=product_ids).delete()

        return Response({'deleted_count': deleted_count[0]})

    # only for admin
    @action(detail=False, methods=['GET'])
    def get_all(self, request):
        products = self.get_queryset()
        serializer = self.get_serializer(products, many=True)

        return Response(serializer.data)


class FavoritesItemViewSet(viewsets.ModelViewSet):
    queryset = FavoritesItem.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return FavoritesItemSerializer
        return FavoritesItemDetailSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        cart_items = CartItem.objects.filter(cart__user=request.user.id).values_list('product_id', flat=True)

        products_data = serializer.data
        for fav_product in products_data:
            fav_product['product']['in_cart'] = fav_product['product']['id'] in cart_items

        # Get the currency value from the environment variable
        currency = env('CURRENCY_CODE')

        # Create the response dictionary with 'data' and 'currency' fields
        response_data = {
            'favorites': products_data,
            'currency': currency,
        }

        return Response(response_data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['DELETE'], url_path='delete')
    def delete_items(self, request):
        product_ids = request.data.get('product_ids', [])
        deleted_count = FavoritesItem.objects.filter(user=request.user, product__id__in=product_ids).delete()

        return Response({'deleted_count': deleted_count[0]})


class ShippingMethodViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingMethodSerializer
    queryset = ShippingMethod.objects.all()
    permission_classes = (permissions.AllowAny,)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def create(self, request, *args, **kwargs):
        # To ensure that all database operations performed within the block
        # are treated as a single atomic transaction. If an exception occurs
        # during the block execution, the transaction is rolled back, undoing
        # any changes made so far.
        with transaction.atomic():
            # generate unique id for the order
            order_uuid = str(uuid.uuid4())
            request.data['uuid'] = order_uuid
            # assigning user instance url to future order
            user_url = reverse('customuser-detail', args=[request.user.id])
            request.data['user'] = user_url

            # creating new order
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            # getting instance of the created order
            order = serializer.instance

            # activating promo code if it entered by user
            promo = Promo.objects.filter(code__iexact=request.data['promo_code']).first()
            if promo:
                # check if promo already used by user
                activations = PromoActivation.objects.filter(user=request.user, promo=promo).first()
                if not activations:
                    PromoActivation.objects.create(
                        order=order,
                        user=request.user,
                        promo=promo,
                    )
                    promo.quantity -= 1
                    promo.save()

            # moving CartItems to OrderItems
            cart_items = CartItem.objects.filter(cart__user=request.user)
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )

            try:
                payment_amount = round(float(order.total_price), 2)
                coinbase_response = create_coinbase_payment(payment_amount, order_uuid)
            except Exception as e:
                print('Failed to create a payment')

            # if coinbase payment creation is successful - create new payment instance
            Payment.objects.create(
                order=order,
                amount=order.total_price,
                payment_method=get_object_or_404(PaymentMethod, id=request.data['payment_method_id']),
                payment_id=coinbase_response['data']['id'],
                payment_code=coinbase_response['data']['code'],
                hosted_url=coinbase_response['data']['hosted_url'],
            )

            # clear the cart
            cart_items.delete()

            headers = self.get_success_headers(serializer.data)
            return Response({'payment_url': coinbase_response['data']['hosted_url']}, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'], url_path='cancel')
    def cancel(self, request):
        order_id = request.data.get('order_id', None)
        order = Order.objects.filter(uuid=order_id, user=request.user).first()

        if order:
            if order.status == 'PENDING' or order.status == 'PROCESSING':
                order.status = 'CANCELLED'
                order.save()

                promo_act = PromoActivation.objects.filter(order=order).first()
                if promo_act:
                    promo = promo_act.promo
                    promo.quantity += 1
                    promo.save()
                    promo_act.delete()
                return Response({'status': 'success'}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'status': 'error', 'message': 'Unable to cancel this order'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()


class PaymentMethodViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()
    permission_classes = (permissions.AllowAny,)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get_permissions(self):
        allowed_any = ['new', 'donate', 'webhook_handler']
        if self.action in allowed_any:
            # AllowAny permission for some of the actions
            permission_classes = [permissions.AllowAny]
        else:
            # SessionAuthentication permission for other actions
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def new(self, request):
        # print(request.data)

        # url = 'https://api.commerce.coinbase.com/charges/'
        # headers = {
        #     'Content-Type': 'application/json',
        #     'X-CC-Api-Key': env('COINBASE_COMMERCE_API_KEY'),
        #     'X-CC-Version': env('COINBASE_COMMERCE_VERSION'),
        # }
        # data = json.dumps({
        #     'name': 'Payment',
        #     'description': 'Payment',
        #     'pricing_type': 'fixed_price',
        #     'local_price': {
        #         'amount': amount,
        #         'currency': env('CURRENCY_CODE'),
        #     },
        #     'metadata': {
        #         'order_id': order_id,
        #     },
        #     # 'redirect_url': '',
        #     # 'cancel_url': '',
        # })
        # response = requests.post(url, headers=headers, data=data)

        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def donate(self):
        url = 'https://api.commerce.coinbase.com/charges/'
        headers = {
            'Content-Type': 'application/json',
            'X-CC-Api-Key': env('COINBASE_COMMERCE_API_KEY'),
            'X-CC-Version': env('COINBASE_COMMERCE_VERSION'),
        }
        data = json.dumps({
            'name': 'Donation',
            'description': 'Just a donation',
            'pricing_type': 'no_price',
        })
        response = requests.post(url, headers=headers, data=data)

        return Response(response.json())

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def webhook_handler(self, request):
        raw_request_payload = request.body
        webhook_signature = request.headers['X-Cc-Webhook-Signature']
        signature_valid = validate_webhook_signature(raw_request_payload, webhook_signature)

        if signature_valid:
            '''
            charge:created	    New charge is created
            charge:confirmed	Charge has been confirmed and the associated payment is completed
            charge:failed	    Charge failed to complete
            charge:delayed	    Charge received a payment after it had been expired
            charge:pending	    Charge has been detected but has not been confirmed yet
            charge:resolved	    Charge has been resolved
            '''

            event_type = request.data['event']['type']
            order_uuid = request.data['event']['data']['metadata']['order_id']

            if event_type and order_uuid:
                payment = get_object_or_404(Payment, uuid=order_uuid)

                if event_type == 'charge:created':
                    # each required instance is already created in OrderViewSet so pass this statement
                    pass

                elif event_type == 'charge:confirmed':
                    payment.status = 'COMPLETED'
                    payment.save()

                elif event_type == 'charge:failed':
                    payment.status = 'FAILED'
                    payment.save()

                elif event_type == 'charge:delayed':
                    payment.status = 'COMPLETED'
                    payment.save()

                elif event_type == 'charge:pending':
                    payment.status = 'PROCESSING'
                    payment.save()

                elif event_type == 'charge:resolved':
                    # payment resolved by merchant so don't do anything here
                    return Response(status=status.HTTP_200_OK)

                else:
                    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

                return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PromoViewSet(viewsets.ModelViewSet):
    serializer_class = PromoSerializer
    queryset = Promo.objects.all()

    @action(detail=False, methods=['post'])
    def check(self, request):
        promo_code = request.data.get('promo')
        if promo_code:
            promo_data = Promo.objects.filter(code__iexact=promo_code).first()
            if promo_data:
                activations = PromoActivation.objects.filter(user=request.user, promo=promo_data).first()
                if activations:
                    return Response({'error': 'Promo code is already used'}, status=status.HTTP_403_FORBIDDEN)
                else:
                    serializer = self.get_serializer(promo_data)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Promo doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'No promo code given'}, status=status.HTTP_400_BAD_REQUEST)


class PromoActivationViewSet(viewsets.ModelViewSet):
    serializer_class = PromoActivationSerializer
    queryset = PromoActivation.objects.all()
