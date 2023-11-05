from ads.filters import AdFilterSet
from ads.models import Ad, Comment
from ads.permissions import IsAdmin, IsOwner
from ads.serializers import AdCreateSerializer, AdDetailSerializer, AdSerializer, CommentCreateSerializer, CommentSerializer
from rest_framework import pagination, viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    filterset_class = AdFilterSet

    serializers = {'retrieve': AdDetailSerializer, 'create': AdCreateSerializer}
    default_serializer = AdSerializer

    permissions = {
        'create': [IsAuthenticated],
        'update': [IsOwner | IsAdmin],
        'partial_update': [IsOwner | IsAdmin],
        'destroy': [IsOwner | IsAdmin],
    }
    default_permission = [AllowAny]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def get_permissions(self):
        self.permission_classes = self.permissions.get(
            self.action, self.default_permission
        )
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        return super().create(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializers = {'create': CommentCreateSerializer}
    default_serializer = CommentSerializer

    permissions = {
        'create': [IsAuthenticated],
        'update': [IsOwner | IsAdmin],
        'partial_update': [IsOwner | IsAdmin],
        'destroy': [IsOwner | IsAdmin],
    }
    default_permission = [AllowAny]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def get_permissions(self):
        self.permission_classes = self.permissions.get(
            self.action, self.default_permission
        )
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        ad_pk = self.kwargs.get('ad_pk')
        queryset = self.queryset.filter(ad_id=ad_pk)
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def create(self, request, *args, **kwargs):
        ad_pk = self.kwargs.get('ad_pk')
        data = {
            'ad': ad_pk,
            'auhtor': request.user.pk,
            'text': request.data.get('text'),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserAdsListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(auhtor=request.user)
        return super().list(request, *args, *kwargs)


