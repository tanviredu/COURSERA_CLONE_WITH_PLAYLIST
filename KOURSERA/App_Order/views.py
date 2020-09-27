from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required

from App_Order.models import Cart,Order
from App_Shop.models import Product

from django.contrib import messages

@login_required
def add_to_cart(request,pk):
    item = get_object_or_404(Product,pk=pk)
    print("item :"+str(item))
    # this will also make a list if the product is selected before
    # idexing
    order_item = Cart.objects.get_or_create(item=item,user=request.user,purchased=False)
    print("order Item :"+str(order_item))
    # get the order object that is yet not paid
    # and try to add the cart in it
    # other wise create it
    # it will return a list even it is only one
    # so make indexing
    order_qs = Order.objects.filter(user=request.user,ordered=False)

    ## chek if you even create any unpaid order yet
    if order_qs.exists():
        order = order_qs[0]
        print("Order Exists adding to it")
        print(order)
        if order.orderitems.filter(item=item).exists():
            # the product exists in the order
            # so increase the cart
            # orderitem[0] is the cart that is matched because it return a list even
            # it is only one element
            # we checked all the cart in a order to seach the duplicate
            # then increase it
            # we are increasing the cart
            order_item[0].quantity +=1
            order_item[0].save()
            messages.info(request,"This Item Quantity was updated")
            return redirect("App_Shop:home")
        else:
            ## add to the cart that belongs 
            ##  order object that has (ordered=False)
            order.orderitems.add(order_item[0])
            messages.info(request,"This item is added to the cart")
            return redirect("App_Shop:home")
    else:
        ## first time 
        ## never created a order
        ## so create the order object then add the cart
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request,"Item added To the Cart")
        return redirect('App_Shop:home')



@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user,purchased=False)
    ## at a time there will be one order that is
    ## has ordered=False because after payment 
    ## this flag wil change
    ## then as long there is Order(ordered=False) exists
    ## the cart that you add will join this
    ## so when you search for orders(order=False)
    ## you will get one order but in a list
    ## so do indexing [0] to get that
    orders = Order.objects.filter(user=request.user,ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request,'App_Order/cart.html',{'carts':carts,'order':order})
    else:
        messages.warning(request,"You Don't have any item in your cart")
        return redirect("App_Shop:home")

@login_required
def remove_form_cart(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        ## seach for specfic product in the order
        if order.orderitems.filter(item=item).exists():
            ## now find the cart object of the product
            ## then remove from the Order object
            ## since order object has list of cart objects
            ## we need to remove the cart object thats why we are seaching 
            ## the cart too
            ## it will also be one item in one list so do the indexing
            order_item = Cart.objects.filter(item=item,user=request.user,purchased=False)[0]
            order_item.delete()
            messages.warning(request,"This Item is Removed from the cart")
            return redirect('App_Order:cart')
        else:
            messages.info(request,"This item is not in your cart")
            return redirect('App_Shop:home')
    else:
        ## this means the order is not active 
        ## because we are searcing for ordered=False
        messages.info(request,"You dont Have any active Order")
        return redirect("App_Shop:home")
