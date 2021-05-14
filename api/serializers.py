from datetime import datetime
from rest_framework import serializers
from auth_.models import Seller, User
from auth_.serializers import UserSimpleSerializer, SellerSimpleSerializer
from .models import Gadget, DeliveryAddress, Category, Comment, Order


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    seller = SellerSimpleSerializer(read_only=True)
    is_active = serializers.BooleanField()

    class Meta:
        model = Gadget
        fields = ['id', 'name', 'category', 'description', 'price', 'amount', 'image', 'seller', 'is_active']


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gadget
        fields = ['name', 'category', 'price', 'is_active']


class ProductSimpleSerializer(OrderProductSerializer):
    seller = SellerSimpleSerializer()

    class Meta:
        model = Gadget
        fields = OrderProductSerializer.Meta.fields + ['seller']


class ProductCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    seller = SellerSimpleSerializer(read_only=True)

    class Meta:
        model = Gadget
        fields = ['name', 'category', 'description', 'price', 'amount', 'image', 'seller']

    def validate(self, attrs):
        print(attrs)
        if not attrs.__contains__('name'):
            raise serializers.ValidationError('Name is required')
        if not attrs.__contains__('category'):
            raise serializers.ValidationError('Category is required')
        if not attrs.__contains__('description'):
            raise serializers.ValidationError('Description is required')
        if not attrs.__contains__('price'):
            raise serializers.ValidationError('Price is required')
        if not attrs.__contains__('amount'):
            raise serializers.ValidationError('Amount is required')
        return attrs

    def create(self, validated_data):
        return Gadget.objects.create(
            name=validated_data['name'],
            category=validated_data['category'],
            description=validated_data['description'],
            price=validated_data['price'],
            amount=validated_data['amount'],
            seller=self.context['request'].user.seller
        )


class ProductUpdateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    is_active = serializers.BooleanField(required=False)
    price = serializers.IntegerField(required=False)
    amount = serializers.IntegerField(required=False)

    class Meta:
        model = Gadget
        fields = ['description', 'price', 'amount', 'image', 'is_active']

    def validate(self, attrs):
        if not attrs.contains('description') and not attrs.contains('price') and\
                not attrs.contains('amount') \
                and not attrs.contains('is_active') and not self.context['picture']:
            raise serializers.ValidationError('No data to update')

        return attrs

    def update(self, instance, validated_data):
        # print(self.context['request'])
        # if self.context['request'].FILES['picture']:
        #     instance.image = self.context['request'].FILES['picture']
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        if self.context['picture'] is not False:
            instance.image = self.context['picture']
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    def delete(self, instance):
        print('delete', instance)
        return instance


class CommentSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    published = serializers.DateField()

    class Meta:
        model = Comment
        fields = ['user', 'body', 'published']


class CommentCreateSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    product = ProductSimpleSerializer(read_only=True)
    published = serializers.DateField(required=False)
    body = serializers.CharField()

    class Meta:
        model = Comment
        fields = ['user', 'product', 'published', 'body']

    def validate(self, attrs):
        if not attrs.__contains__('body'):
            raise serializers.ValidationError('Body of comment is required')
        return attrs

    def create(self, validated_data):
        comment = Comment.objects.create(
            user=self.context['request'].user,
            product=self.context['product'],
            body=validated_data['body'],
        )
        comment.save()
        return comment


class DeliveryAddressSerializer(serializers.Serializer):
    address = serializers.CharField()

    class Meta:
        model = DeliveryAddress
        fields = ['region', 'address']


class OrderSerializer(serializers.ModelSerializer):
    shipping_address = DeliveryAddressSerializer(read_only=True)
    products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'products', 'total', 'date_created', 'shipping_address']


class OrderCreateSerializer(serializers.ModelSerializer):
    customer = UserSimpleSerializer(read_only=True)
    shipping_address = DeliveryAddressSerializer(read_only=True)
    products = ProductSimpleSerializer(read_only=True, many=True)
    total = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ['customer', 'products', 'total', 'shipping_address']

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        customer = validated_data['customer']
        add = validated_data['shipping_address']
        products = validated_data['products']
        order = Order.objects.create(
            customer=customer,
            address=add,
            total=100)
        order.products.set(products)
        return order


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)

    def validate(self, attrs):
        if not attrs.__contains__('name'):
            raise serializers.ValidationError('Name field is required')
        try:
            Category.objects.get(name=attrs['name'])
        except Category.DoesNotExist:
            return attrs
        raise serializers.ValidationError('Category with that name already exists')
        # return attrs

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
