from django.urls import path
from tenantapp import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/', views.ProductView.as_view(), name='product'),
    path('purchase/', views.PurchaseView.as_view(), name='purchase'),
    path('subscription/', views.SubscriptionView.as_view(), name='subscription'),
    path('reactive_subscription/', views.ReactiveSubscriptionView.as_view(), name='reactive_subscription'),
    path('cancel_subscription/', views.CancelSubscriptionView.as_view(), name='cancel_subscription'),
]