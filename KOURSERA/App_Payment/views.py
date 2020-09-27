from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse
from django.urls import reverse
from django.contrib import messages

from .models import BillingAddress
from .forms import BillingForm

from App_Order.models import Order,Cart

from django.contrib.auth.decorators import login_required


import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket
from django.views.decorators.csrf import csrf_exempt


## adding content
from App_Login.models import Video_Content



@login_required
def checkout(request):
    ## get the billing address object or if not then
    ## create a empty Billing Address object with the user instance
    ## like init the system 
    ## this will return one element in one list
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    print(saved_address)
    ## billing form is created from Billing address
    form = BillingForm(instance=saved_address)

    ## prompt the user to fill the rest of the information
    if request.method == "POST":
        form = BillingForm(request.POST,instance=saved_address)
        if form.is_valid():
            form.save()
            ## reset the form
            form = BillingForm(instance=saved_address)
            messages.success(request,"Shipping Address is Saved")
    
    ## giving addtional information with the form
    ## only one order inside a list do the indexing
    ## there is only one Order with (ordered=False)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    ## fetch all the cart
    order_items = order_qs[0].orderitems.all()
    order_total = order_qs[0].get_totals()
    return render(request,'App_Payment/checkout.html',{'form':form,'order_items':order_items,'order_total':order_total,'saved_address':saved_address})
        

@login_required
def payment(request):
    ## get the Billing address
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    ## check again that it is fully filled
    if not saved_address.is_fully_filled():
        messages.info(request,"Please Complete Shipping Address")
        return redirect('App_Payment:chekout')
    
    ## check the profile is filled too
    if not request.user.profile.is_fully_filled():
        messages.info(request,"Please Complete Profile Details")
        return redirect('App_Login:profile')

    store_id = "test5f63e7c01865f"
    API_Key  = "test5f63e7c01865f@ssl"

    mypayment = SSLCSession(sslc_is_sandbox=True,sslc_store_id=store_id,sslc_store_pass=API_Key)
    ## give the redirect url to check the status
    ## when it done where i goes
    status_url = request.build_absolute_uri(reverse('App_Payment:complete'))
    mypayment.set_urls(success_url=status_url,fail_url=status_url,cancel_url=status_url,ipn_url=status_url)

    order_qs = Order.objects.filter(user=request.user,ordered=False)
    order_qs = order_qs[0]

    ## get all the Carts
    order_items = order_qs.orderitems.all()
    ## get how many cart did you get
    order_items_counts = order_qs.orderitems.count()
    ## get the total price
    order_total = order_qs.get_totals()
    mypayment.set_product_integration(total_amount=Decimal(order_total),currency="BDT",product_category='Mixed',product_name=order_items,num_of_item=order_items_counts,shipping_method='Courier',product_profile='None')

    ## now we need to set the customer info
    ## and the shippign address both
    current_user = request.user
    mypayment.set_customer_info(name=current_user.profile.full_name,email=current_user.email,address1=current_user.profile.address_1,address2=current_user.profile.address_1,city=current_user.profile.city,postcode=current_user.profile.zipcode,country=current_user.profile.country,phone=current_user.profile.phone)
    mypayment.set_shipping_info(shipping_to=current_user.profile.full_name,address=saved_address.address,city=saved_address.city,postcode=saved_address.zipcode,country=saved_address.country)
    response_data = mypayment.init_payment()
    print(response_data)
    return redirect(response_data['GatewayPageURL'])



@csrf_exempt
def complete(request):
    if request.method == "POST" or request.method == "post":
        payment_data = request.POST
        status = payment_data['status']
        if status == "VALID":
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(request,"Payment Successfull")
            ## it will call the purchage method
            ## that will change the 
            return HttpResponseRedirect(reverse('App_Payment:purchase',kwargs={'val_id':val_id,'tran_id':tran_id}))
        elif status == "FAILED":
            messages.success(request,'payment Failed')
        return render(request,'App_Payment/complete.html',{})

@login_required
def purchase(request,val_id,tran_id):
    ## in here we change the flag of the cart to purchased = True
    ## Order (ordered = True)
    ## add the video slug with the video contaent and the user
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    order = order_qs[0]
    orderId = tran_id
    order.ordered = True ## change the first flag
    order.orderId = tran_id
    order.paymentId = val_id
    order.save()

    ## get all the cart items
    cart_items = Cart.objects.filter(user=request.user,purchased=False)
    current_user = request.user

    for item in cart_items:
        item.purchased = True ## change the second flag
        item.save()
        vc = Video_Content(user=current_user)
        vc.video_slug = item.item.slug
        vc.save()
    return HttpResponseRedirect(reverse('App_Shop:home'))



@login_required
def order_view(request):
    try:
        ## search for the order that is processed
        orders = Order.objects.filter(user=request.user,ordered=True)
        context = {'orders':orders}
    except:
        messages.warning(request,"You Do not Have Active order")
        return redirect('App_Shop:home')
    return render(request,"App_Payment/order.html",context=context)