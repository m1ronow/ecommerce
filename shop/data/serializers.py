from rest_framework import serializers
from .models import CustomUser, UserAddress, UserProfile, Category, Product, Cart, CartItem, Order, OrderItem, \
    Payment, ShippingMethod, Promo, PaymentMethod, FavoritesItem, PromoActivation
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(label="Username", write_only=True)
    password = serializers.CharField(label="Password", style={'input_type': 'password'},
                                     trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        # Take username and password from request
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'url', 'email', 'password', 'date_joined', 'is_active', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserAddressSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserAddress
        fields = '__all__'


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = CustomUserSerializer()
    current_address = UserAddressSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class CartProductSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'
        extra_kwargs = {
            'cart': {'read_only': True}
        }


class CartItemDetailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product = CartProductSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'


class FavoritesItemSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = FavoritesItem
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }


class FavoritesItemDetailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product = CartProductSerializer()

    class Meta:
        model = FavoritesItem
        fields = '__all__'


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentMethodSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PaymentMethod
        fields = '__all__'


class ShippingMethodSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ShippingMethod
        fields = '__all__'


class PromoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Promo
        fields = ['code', 'multiplier', 'quantity']


class PromoActivationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PromoActivation
        fields = ['order', 'user', 'promo']
