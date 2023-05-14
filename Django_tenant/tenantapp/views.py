import stripe
import datetime
from django.shortcuts import render, redirect
from sharedapp.forms import ProductForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from tenantapp.models import Product
from django.conf import settings
from django.db import transaction
from django.contrib import messages
from sharedapp.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY
    
@method_decorator(login_required(login_url='login/'), name='dispatch')
class HomeView(View):
    def get(self, request):
        product = Product.objects.all()
        email = f"{request.user.username}@gmail.com"
        customer_list = stripe.Customer.list(email=email).data
        if customer_list:
            customer_id = customer_list[0]["id"]
            subscription_list = stripe.Subscription.list(customer=customer_id).data
            cancel_at_period_end = subscription_list[0]['cancel_at_period_end']
            return render(request, 'tenantapp/home.html', {
                "products":product,
                "subscription":subscription_list,
                "cancel_at_period_end":cancel_at_period_end
                }
            )
        return render(request, 'tenantapp/home.html', {"products":product, "data":0})


class ProductView(View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'tenantapp/addproduct.html', {'form':form})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'tenantapp/addproduct.html', {'form':form})
    
    
class SubscriptionView(View):
    def get(self, request):
        return render(request, 'tenantapp/subscription.html')


class PurchaseView(View):

    @transaction.atomic
    def get(self, request):
        try:
            email = f"{request.user.username}@gmail.com"
            customer_list = stripe.Customer.list(email=email).data
            if not customer_list:
                customer = stripe.Customer.create(
                    email = f"{request.user.username}@gmail.com",
                    name = request.user.first_name
                    )
                
                payment_method = stripe.PaymentMethod.create(
                    type="card",
                    card={
                        "number": "4242424242424242",
                        "exp_month": 9,
                        "exp_year": 2025,
                        "cvc": "314",
                    },
                    )
                
                payment_method_attach = stripe.PaymentMethod.attach(
                    payment_method["id"],
                    customer=customer["id"],
                    )
                
                default_payment_method = stripe.Customer.modify(
                    customer["id"],
                    invoice_settings={"default_payment_method":payment_method["id"]},
                    )
                
                subscription = stripe.Subscription.create(
                    customer=customer["id"],
                    off_session = True,
                    items=[
                        {"price":settings.STRIPE_PRICE_ID},
                    ],
                    )
                
                user_company = User.objects.get(username=request.user).company
                user_company.subcreption_id = subscription["id"]
                user_company.paid_date = datetime.datetime.now()
                user_company.trial_end = None
                user_company.on_trial = True
                user_company.save()
                
                return render(request, 'tenantapp/purchase.html')
            else:
                messages.error(request, 'Subscription Already Exist')
                return redirect('subscription')
        except Exception as e:
            messages.error(request, e)
            return redirect('subscription')
    
    
class ReactiveSubscriptionView(View):
    def get(self, request):
        try:
            email = f"{request.user.username}@gmail.com"
            customer_list = stripe.Customer.list(email=email)
            customer_id = customer_list["data"][0]["id"]
            subscription = stripe.Subscription.list(customer=customer_id)
            subscription_id = subscription["data"][0]["id"]
            stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=False
                )
            
            return redirect('home')
        except Exception as e:
            messages.error(request, e)
            return redirect('home')    


class CancelSubscriptionView(View):
    def get(self, request):
        try:
            email = f"{request.user.username}@gmail.com"
            customer_list = stripe.Customer.list(email=email)
            customer_id = customer_list["data"][0]["id"]
            subscription = stripe.Subscription.list(customer=customer_id)
            subscription_id = subscription["data"][0]["id"]
            stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
                )
            return render(request, 'tenantapp/cancelsubscription.html')
        except Exception as e:
            messages.error(request, e)
            return redirect('home')
        