import json
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import JsonResponse
from .documents import Product_Document
from Base_App.models import BookTable,AboutUs,feedback,ItemList,Items,Cart,CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect # type: ignore
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Address, Cart, CartItem, Items, Order, Review
from elasticsearch_dsl import Q
from django.contrib.auth.models import User
from  .forms import UserRegisterForm 
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
import stripe # type: ignore
from django.core.paginator import Paginator
# Create your views here.
def homeView(request):
    review = feedback.objects.all()
    items = Items.objects.all()
    list = ItemList.objects.all()
    return render(request, 'home.html',{'items':items,'list':list,'review':review})

def aboutView(request):
    data = AboutUs.objects.all()
    return render(request, 'about.html',{'data':data})

def menuView(request):
    items = Items.objects.all().order_by('id')
    list = ItemList.objects.all()
    
    # Adding pagination
    page = request.GET.get('page')
    paginator = Paginator(items, 6)
    items = paginator.get_page(page)
    return render(request, 'menu.html',{'items':items,'list':list})

@login_required(login_url='/login/')
def bookTableView(request):
    if request.method=='POST':
        user_name = request.POST.get('user_name')
        phone_number = request.POST.get('phone_number')
        user_email = request.POST.get('user_email')
        total_person = request.POST.get('total_person')
        booking_date = request.POST.get('booking_date')
        
        print("Received Data:", {
            "user_name": user_name,
            "phone_number": phone_number,
            "user_email": user_email,
            "total_person": total_person,
            "booking_date": booking_date,
        })  # This will print in the terminal

        if not booking_date:  # Check if the date is empty
            print("Booking date is missing!")

        BookTable.objects.create(
            user_name=user_name,
            phone_number=phone_number,
            user_email=user_email,
            total_person=total_person,
            booking_date=booking_date
        )
        
        return redirect("Booking_Success")
    return render(request, 'book_table.html')

def booking_success(request):
    
    return render(request, 'booking_success.html')


@login_required(login_url='/login/')
def feedbackView(request):
    return render(request, 'feedback.html')

# user login view
@csrf_exempt
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_exists = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "login.html", {'message': 'Invalid credentials! User does not exist. Please register.'})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Handle next parameter
            next_url = request.POST.get("next")
            if next_url and "/user_profile/0/" in next_url:
                next_url = next_url.replace("/user_profile/0/", f"/user_profile/{user.id}/")

            return redirect(next_url or reverse('User_Profile', args=[user.id]))

        return render(request, "login.html", {'message': 'Invalid credentials! Incorrect password.'})
    
    # Handle GET request for login page
    next_url = request.GET.get("next", "/")
    return render(request, "login.html", {'next': next_url})

@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Save the user instance
            user = form.save(commit=False)  # Don't save to DB yet
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Save the user to the DB
            login(request, user)  # Log the user in after registration
            
            # Handle 'next' parameter safely
            next_url = request.POST.get('next')
            if not next_url:  # If 'next' is None or empty, fallback to '/'
                next_url = '/'
            return redirect(next_url)
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def user_profile(request,user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_profile.html', {'user': user})

def search(request):
    query = request.GET.get('q', '').strip()

    #  Autocomplete Suggestions
    if request.GET.get('suggest') == 'true':
        try:
            suggestions = Product_Document.search().suggest(
                "product-suggest",
                query,
                completion={"field": "suggest", "size": 5}
            )
            response = suggestions.execute()

            # Extracting suggestion texts
            suggest_results = [
                option.text for option in response.suggest["product-suggest"][0].options
            ]
            return JsonResponse({"suggestions": suggest_results}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # Regular Search (with Fuzzy Search)
    if query:
        try:
            search_query = Product_Document.search().query(
                Q("multi_match", query=query, fields=["Item_name", "description"], fuzziness="AUTO")
            )
            response = search_query.execute()

            results = [
                {
                    'Item_name': hit.Item_name,
                    'description': hit.description,
                    'price': hit.price,
                    'Image': hit.Image,
                    'id': hit.meta.id,
                }
                for hit in response
            ]
            return render(request, 'search_results.html', {"results": results, "query": query})

        except Exception as e:
            return render(request, 'search_results.html', {"error": str(e)})

    # Default response if no query is provided
    return render(request, 'search_results.html', {"error": "Please enter a search term."})
# add to cart
def add_to_cart(request, product_id):
    if request.method == "POST":
        try:
            item = get_object_or_404(Items, id=product_id)
            user_cart, _ = Cart.objects.get_or_create(user=request.user)

            # ✅ Correct way to check and create a cart item
            cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=item)

            if not created:
                cart_item.quantity += 1
                cart_item.save()
                message = f"{item.Item_name} quantity updated in cart."
            else:
                message = f"{item.Item_name} added to cart."

            return JsonResponse({"success": True, "message": message})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"})

    return JsonResponse({"success": False, "message": "Invalid request."})

@login_required
def increase_quantity(request, product_id):
    cart_item = get_object_or_404(CartItem, cart__user=request.user, product_id=product_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def decrease_quantity(request,product_id):
    cart_item = get_object_or_404(CartItem, cart__user=request.user, product_id=product_id)
    if cart_item.quantity==1:
        cart_item.delete()
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart')

@login_required
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        cart_items = []
        total_price = 0
    else:
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.get_total_price() for item in cart_items)
        
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'user_cart.html', context)
# Update quantity

# Remove from cart
@login_required
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, cart__user=request.user, product_id=product_id)
    cart_item.delete()
    return redirect('cart')

def success(request):
    return render(request,'success.html')

def cancel(request):
    return render(request,'cancel.html')

@login_required
def update_cart(request, product_id):
    # Ensure this is a POST request
    if request.method == 'POST':
        try:
            print(f"Received POST request: {request.POST}")  # Debugging

            item = get_object_or_404(Items, id=product_id)
            user_cart, _ = Cart.objects.get_or_create(user=request.user)

            # Check for 'action' in POST data to determine whether to increase or decrease the quantity
            action = request.POST.get('action')
            if action == 'increase':
                cart_item = user_cart.items.filter(product=item).first()
                if cart_item:
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    user_cart.items.create(product=item, quantity=1)
            elif action == 'decrease':
                cart_item = user_cart.items.filter(product=item).first()
                if cart_item and cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    return JsonResponse({'success': False, 'message': 'Cannot decrease quantity further.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid action.'})
            # Render the updated cart HTML
            updated_cart_html = render_to_string("user_cart.html", {"cart_items": user_cart.items.all()})
            return JsonResponse({"success": True, "cart_html": updated_cart_html})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request.'})

@login_required
def add_address(request):
    # 
    if request.method == "POST":
        address_id = request.POST.get("id")
        name = request.POST.get("name")
        mobile_number = request.POST.get("mobile_number")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip_code")  
        country = request.POST.get("country")

        if not all([name, mobile_number, city, state, zip_code, country]):
            messages.error(request, "All fields are required.")
            return redirect("add_address")

        if address_id:  # Update existing address
            address = get_object_or_404(Address, id=address_id, user=request.user)
            address.name = name
            address.mobile_number = mobile_number
            address.city = city
            address.state = state
            address.zip_code = zip_code
            address.country = country
            address.save()
            messages.success(request, "Address updated successfully!")
        else:  # Add new address
            address = Address.objects.create(
                user=request.user,
                name=name,
                mobile_number=mobile_number,
                city=city,
                state=state,
                zip_code=zip_code,
                country=country,
            )
            messages.success(request, "Address added successfully!")

        # Store selected address in session for checkout
        request.session["selected_address"] = address.id

        # Check where to redirect the user: Buy Now or Cart Checkout
        if request.session.get("checkout_type") == "buy_now":
            item_id = request.session.get("buy_now_item")
            return redirect("checkout_buy_now", product_id=item_id)

        return redirect("add_address")  # Default to cart checkout

    # Fetch user's saved addresses
    addresses = Address.objects.filter(user=request.user)
    return render(request, "add_address.html", {"addresses": addresses})

@csrf_exempt
def delete_address(request, address_id):
    if request.method == "DELETE":
        address = get_object_or_404(Address, id=address_id, user=request.user)
        address.delete()
        return JsonResponse({"message": "Address deleted successfully"}, status=200)
    return JsonResponse({"error": "Invalid request"}, status=400)

def item_details(request,product_id):
    item = get_object_or_404(Items,id=product_id)
    return render(request,'item_details.html',{"item":item})

@csrf_exempt
@login_required
def add_review(request,product_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            item = Items.objects.get(id=product_id)
            
            # Save review to database
            review = Review.objects.create(
                item=item,
                user=request.user,
                rating=int(data["rating"]),
                comment=data["comment"]
            )
            
            return JsonResponse({
                "success": True,
                "username": request.user.username,
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at.strftime("%B %d, %Y")
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

@csrf_exempt
@login_required   
def edit_review(request,review_id):
    """Edit an existing review"""
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            review = get_object_or_404(Review, id=review_id, user=request.user)  # Ensure user owns the review
            review.rating = int(data["rating"])
            review.comment = data["comment"]
            review.save()

            return JsonResponse({
                "success": True,
                "rating": review.rating,
                "comment": review.comment
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

@csrf_exempt
@login_required   
def delete_review(request,review_id):
    """Delete a review"""
    if request.method == "POST":
        try:
            review = get_object_or_404(Review, id=review_id, user=request.user)  # Ensure user owns the review
            review.delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

stripe.api_key = settings.STRIPE_SECRET_KEY
@login_required
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            address_id = request.POST.get('address_id') or request.session.get("selected_address")
            print(f" Address ID: {address_id}")

            if not address_id:
                return JsonResponse({'error': 'Please select a valid address before checking out'}, status=400)

            address = Address.objects.filter(id=address_id, user=request.user).first()
            if not address:
                return JsonResponse({'error': 'Invalid address'}, status=400)

            #  Debug Buy Now Session
            buy_now_item = request.session.get('buy_now_item')
            print(f"Buy Now Item: {json.dumps(buy_now_item, indent=2)}")

            if buy_now_item:
                if not isinstance(buy_now_item, dict) or 'name' not in buy_now_item or 'price' not in buy_now_item:
                    return JsonResponse({'error': 'Invalid buy_now_item session data'}, status=400)

                line_items = [{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': buy_now_item['name']},
                        'unit_amount': int(buy_now_item['price'] * 100),
                    },
                    'quantity': 1,
                }]
                total_amount = buy_now_item['price']

            else:
                cart = Cart.objects.filter(user=request.user).first()
                if not cart:
                    return JsonResponse({'error': 'Cart is empty'}, status=400)

                cart_items = CartItem.objects.filter(cart=cart)
                line_items = []
                total_amount = 0

                for item in cart_items:
                    item_total = item.product.price * item.quantity  
                    total_amount += item_total  

                    line_items.append({
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {'name': item.product.Item_name},
                            'unit_amount': int(item.product.price * 100),
                        },
                        'quantity': item.quantity,
                    })

            print(f"Final Line Items: {json.dumps(line_items, indent=2)}")

            if total_amount <= 0:
                return JsonResponse({'error': 'Cart total must be greater than zero'}, status=400)

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')),
                cancel_url=request.build_absolute_uri(reverse('cart')),
                metadata={'address_id': address.id, 'checkout_type': 'buy_now' if buy_now_item else 'cart'}
            )

            request.session.pop('buy_now_item', None)

            return JsonResponse({'id': checkout_session.id, 'url': checkout_session.url})

        except Exception as e:
            print(f"Stripe Error: {e}")  # Show full error in terminal
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

stripe.api_key = settings.STRIPE_SECRET_KEY
@login_required
def buy_now(request, product_id):
    item = get_object_or_404(Items, id=product_id)

    # Store full product details in session
    request.session['buy_now_item'] = {
        'id': item.id,
        'price': float(item.price),  # Convert to float
        'name': item.Item_name
    }
    
    return redirect(reverse('add_address'))  # Redirect to address selection
