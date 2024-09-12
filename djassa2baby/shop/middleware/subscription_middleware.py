import datetime
from django.utils.timezone import now
from django.shortcuts import redirect
from django.conf import settings

from shop.models.shop import Shop
from shop.models.subscription import SubscriptionHistory

class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            shop = Shop.objects.filter(user=request.user).first()

            if shop:
                # Check if the user is within the one-month free period
                one_month_after_registration = shop.date_added + datetime.timedelta(days=30)
                if now() <= one_month_after_registration:
                    # User is still in the free period, skip further checks
                    return self.get_response(request)

                # After the free period, check if the user has paid for the current month
                last_payment = SubscriptionHistory.objects.filter(shop=shop).order_by('-payment_date').first()

                if last_payment:
                    next_due_date = last_payment.payment_date + datetime.timedelta(days=30)
                    if now() > next_due_date:
                        # Subscription has expired, redirect to payment page or notify the user
                        return redirect('subscription_payment_page')

                else:
                    # No payment history, redirect to payment page
                    return redirect('subscription_payment_page')

        response = self.get_response(request)
        return response
