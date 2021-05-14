from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import viewsets, status, generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from auth_.serializers import RegisterUserSerializer, RegisterSellerSerializer, UserSerializer,  SellerSerializer, \
    ProfileSerializer, EditProfile
import logging
logger = logging.getLogger('authorization')


class UserRegisterView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = RegisterUserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                logger.info(f"{user.username} registered")
                ser = UserSerializer(instance=user)
                return JsonResponse(ser.data, status=status.HTTP_200_OK)
            else:
                logger.error(serializer.errors)
                return JsonResponse({'errors': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"{e} error")
            return JsonResponse({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


class SellerRegisterView(generics.GenericAPIView):
    serializer_class = RegisterSellerSerializer

    @permission_classes(IsAuthenticated)
    def post(self, request, *args, **kwargs):
        if request.user.is_seller:
            print(request.user.seller)
            try:
                seller = request.user.seller
            except ObjectDoesNotExist as e1:
                return JsonResponse({'message': "Can not get a seller"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return JsonResponse({'message': 'You are seller'})
        else:
            try:
                serializer = RegisterSellerSerializer(data=request.data, context={'request': request})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    logger.info(f"{request.user} is now seller")
                    return JsonResponse(serializer.data, status=status.HTTP_200_OK)
                else:
                    logger.info(f"{serializer.errors}")
                    return JsonResponse({'message': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(e)
                return JsonResponse({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)


class ProfileUpdate(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        user_profile = self.request.user.profile
        ser = EditProfile(user_profile, data={'picture': request.FILES.get('picture')})
        ser.update(user_profile, request.FILES)
        if ser.is_valid(raise_exception=True):
            user_profile.save()
            ser = ProfileSerializer(user_profile)
            return JsonResponse(ser.data, safe=False)
        return JsonResponse({'error': ser.errors})

    def delete(self, request, *args, **kwargs):
        user_profile = self.request.user.profile
        if user_profile.picture:
            user_profile.picture.delete()
            ser = ProfileSerializer(user_profile)
            return JsonResponse(ser.data, safe=False)
        return JsonResponse({'error': 'Your image is null'})
