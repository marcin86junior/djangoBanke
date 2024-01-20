from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (AccountViewSet, UserViewSet, TransactionViewSet, MyAccountViewSet, TransactionListViewSet,
                    UserListViewSet, TransferView)

router = DefaultRouter()
router.register(r'account', MyAccountViewSet, basename='account')
router.register(r'accounts_list', AccountViewSet, basename='accounts_list')
router.register(r'user_create', UserViewSet, basename='user_create')
router.register(r'users_list', UserListViewSet, basename='user_list')
router.register(r'transaction', TransactionViewSet, basename='transaction')
router.register(r'transactions_list', TransactionListViewSet, basename='transaction_list')

urlpatterns = [
    path('', include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path('transfer/', TransferView.as_view(), name='transfer'),
]
