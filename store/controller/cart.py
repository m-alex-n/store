from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from store.models import Cart, Product

def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id')) 
            product_check = Product.objects.get(id = prod_id)

            if product_check:
                if Cart.objects.filter(user = request.user.id, product_id = prod_id):
                    return JsonResponse({'status' : 'Product already in cart '})
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    
                    # check to see if the amount they are requsting is more than what is in the store
                    if product_check.quantity >= prod_qty : 
                        Cart.objects.create(user = request.user, product_id = prod_id , product_qty = prod_qty)
                        return JsonResponse({'status' : 'Product added successfully'})
                    else:
                        return JsonResponse({'status' : 'Only ' + str(product_check.quantity) + ' quantity available'})
                        
            else:
                return JsonResponse({'status' : 'No such product found '})
                    
        else:
            return JsonResponse({'status' : 'Login to continue'})
    return redirect ('home')

@login_required(login_url='loginpage')
# render items in cart 
def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    context = {'cart':cart}
    return render (request , 'store/cart.html' , context )

# update in cart page 
def updatecart(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user = request.user, product_id= prod_id):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id = prod_id, user = request.user)
            cart.product_qty = prod_qty 
            cart.save()
            return JsonResponse ({'status':'Updated successfully'})
    return redirect('/')

# delete in cart page
def deletecartitem(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user = request.user, product_id= prod_id):
            cartitem = Cart.objects.get(product_id = prod_id, user = request.user)
            cartitem.delete()
            return JsonResponse ({'status':'deleted successfully'})
    return redirect('/')
