import os
import sys
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from house import models
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Add ml_engine to path
sys.path.insert(0, os.path.join(settings.BASE_DIR, 'ml_engine'))
from ml_engine.predict import predict_house_price


def userDashboard(request):
    if 'semail' not in request.session:
        return redirect('login')
    
    uname = request.session['semail']
    udata = models.Register.objects.get(email=uname)
    
    # Statistics
    user_properties = models.AddProperty.objects.filter(fk_reg_id=udata.user_id)
    listed_count = user_properties.count()
    
    # Total sales from transactions related to user's properties
    property_ids = user_properties.values_list('property_id', flat=True)
    transactions = models.BrokerTransaction.objects.filter(fk_property_id__in=property_ids, status='paid')
    total_sales = sum(t.amount for t in transactions)
    
    # Enquiries/Requests for user's properties (RECEIVED)
    enquiries_received = models.PropertyRequest.objects.filter(fk_property_id__in=property_ids).count()
    
    # Enquiries MADE by user
    my_requests_count = models.PropertyRequest.objects.filter(fk_user_id=udata.user_id).count()
    
    context = {
        'user': udata,
        'listed_count': listed_count,
        'total_sales': total_sales,
        'enquiries_received': enquiries_received,
        'my_requests_count': my_requests_count,
        'properties': user_properties[:5] , # Show recent 5

    }
    return render(request, 'user/userDashboard.html', context)

def userProfile(request):
    uname = request.session['semail']
    udata = models.Register.objects.get(email = uname)
    context = {
        'ulist': udata
    }
    return render(request,'user/profile.html',context)

def editUserProfile(request,uid):
    udata = models.Register.objects.get(user_id=uid)
    context ={
        'ulist' : udata
    }
    return render(request, 'user/editProfile.html',context)

def updateUserProfile(request):
    uid = request.POST['uid']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    address = request.POST['address']
    location = request.POST['location']

    udata=models.Register.objects.get(user_id=uid)

    udata.full_name = name
    udata.email = email
    udata.phone_number = phone
    udata.address = address
    udata.location = location
    udata.save()
    return redirect('userProfile') 

def changeUserPassword(request):
     return render(request,'user/userPassword.html')

def updateUserPassword(request):
    npass = request.POST['new_password']
    cpass = request.POST['confirm_password']
    uname = request.session['semail']
    ldata = models.Login.objects.get(user_name=uname)
    rdata = models.Register.objects.get(email=uname)

    if npass ==cpass:
        hashed_password = make_password(npass)
        ldata.password = hashed_password
        rdata.password = hashed_password
        ldata.save()
        rdata.save()
        return redirect('login')
    return redirect("changeUserPassword")

def addProperty(request):
    return render(request,'user/property/addproperty.html')

def saveProperty(request):
    unname = request.session['semail']
    udata = models.Register.objects.get(email=unname)

    image = request.FILES.get('property_image')
    image_name = None

    if image:
        ext = image.name.split('.')[-1]
        image_name = datetime.now().strftime("%Y%m%d%H%M%S") + "." + ext

        fs = FileSystemStorage(location='media/property_images')
        fs.save(image_name, image)
    else:
        messages.error(request, 'You must upload a property image to list a property.')
        return redirect('addProperty')

    property_name=request.POST['property_name']
    property_desc=request.POST['property_desc']
    property_image=f"property_images/{image_name}" if image else None
    property_loc=request.POST['property_loc']
    property_district=request.POST['property_district']
    property_latitude=request.POST['property_latitude']
    property_longitude=request.POST['property_longitude']
    property_area=request.POST['property_area']
    no_of_bed_rooms=request.POST['no_of_bed_rooms']
    price_listed=request.POST['price_listed']
    property_status=request.POST['property_status']
    fk_reg_id=udata.user_id

    # ✅ ADDED VALIDATION: Prevent HTTP 500 if user types non-numbers
    if not str(property_area).isdigit() or not str(no_of_bed_rooms).isdigit() or not str(price_listed).isdigit():
        messages.error(request, 'Area, Bedrooms, and Listed Price must be valid numbers (no text or commas).')
        return redirect('addProperty')

    # 🤖 ML PRICE PREDICTION
    predicted_price = None
    try:
        predicted_price = predict_house_price(
            district=property_district,
            area=int(property_area),
            bedrooms=int(no_of_bed_rooms),
            location=property_loc
        )
        print(f"✅ ML Predicted Price: ₹{predicted_price:,.2f}")
    except Exception as e:
        print(f"⚠️ ML Prediction failed: {e}")
        predicted_price = None

    pdata = models.AddProperty(
        property_name=property_name,
        property_desc=property_desc,
        property_image=property_image,
        property_loc=property_loc,
        property_district=property_district,
        property_latitude=property_latitude,
        property_longitude=property_longitude,
        property_area=property_area,
        no_of_bed_rooms=no_of_bed_rooms,
        price_listed=price_listed,
        price_predicted=predicted_price,  # Save ML predicted price
        property_status=property_status,
        fk_reg_id=fk_reg_id
    )
    pdata.save()
    return redirect('userDashboard')

def browseProperty(request):
    uname = request.session['semail']
    udata = models.Register.objects.get(email=uname)
    
    districts = models.District.objects.all()
    selected_district = request.GET.get('district', '')
    selected_status = request.GET.get('status', '')
    
    properties = models.AddProperty.objects.exclude(fk_reg_id=udata.user_id)
    
    if selected_district:
        properties = properties.filter(property_district=selected_district)

    if selected_status:
        properties = properties.filter(property_status=selected_status)
        
    prop_list = list(properties)
    for p in prop_list:
        try:
            if p.price_predicted and float(p.price_predicted) > 0:
                diff = float(p.price_listed) - float(p.price_predicted)
                pct = (diff / float(p.price_predicted)) * 100
                
                # For a Buyer: Lower list price = Amazing Deal.
                if pct <= -10:
                    p.deal_status = {'text': f'Amazing Deal: {abs(int(pct))}% below market', 'color': 'success'}
                elif pct >= 10:
                    p.deal_status = {'text': f'Overvalued: {abs(int(pct))}% above market', 'color': 'danger'}
                else:
                    p.deal_status = {'text': 'Fair Price', 'color': 'primary'}
            else:
                p.deal_status = None
        except (ValueError, TypeError):
            p.deal_status = None
            
    context = {
        'properties': prop_list,
        'districts': districts,
        'selected_district': selected_district,
        'selected_status': selected_status,
    }
    return render(request, 'user/property/browseProperty.html', context)  

def myProperty(request):
    uname = request.session['semail']
    udata = models.Register.objects.get(email=uname)
    properties = models.AddProperty.objects.filter(fk_reg_id=udata.user_id)
    context = {
        'properties': properties
    }
    return render(request,'user/property/myProperty.html',context)  

def editProperty(request,pid):
    pdata = models.AddProperty.objects.get(property_id=pid)
    context = {
        'property': pdata
    }
    return render(request,'user/property/editProperty.html',context)
    

def updateProperty(request):
    pid = request.POST['property_id']
    pdata = models.AddProperty.objects.get(property_id=pid)

    # 1. Capture inputs
    property_name = request.POST['property_name']
    property_desc = request.POST['property_desc']
    property_loc = request.POST['property_loc']
    property_district = request.POST['property_district']
    no_of_bed_rooms = request.POST['no_of_bed_rooms']
    property_area = request.POST['property_area']
    price_listed = request.POST['price_listed']
    property_status = request.POST['property_status']

    # 2. Add server-side validation to prevent crashes if numeric string is not valid
    if not str(property_area).isdigit() or not str(no_of_bed_rooms).isdigit() or not str(price_listed).isdigit():
        messages.error(request, 'Area, Bedrooms, and Listed Price must be valid numbers.')
        return redirect('editProperty', pid=pid)

    # 3. 🤖 Re-Calculate ML Price Prediction
    predicted_price = pdata.price_predicted
    try:
        predicted_price = predict_house_price(
            district=property_district,
            area=int(property_area),
            bedrooms=int(no_of_bed_rooms),
            location=property_loc
        )
    except Exception as e:
        print(f"⚠️ ML Prediction failed during edit: {e}")

    # 4. Save updates
    pdata.property_name = property_name
    pdata.property_desc = property_desc
    pdata.property_loc = property_loc
    pdata.property_district = property_district
    pdata.no_of_bed_rooms = no_of_bed_rooms
    pdata.property_area = property_area
    pdata.price_listed = price_listed
    pdata.property_status = property_status
    pdata.price_predicted = predicted_price

    # 5. Image Update Option
    image = request.FILES.get('property_image')
    if image:
        ext = image.name.split('.')[-1]
        image_name = datetime.now().strftime("%Y%m%d%H%M%S") + "." + ext
        fs = FileSystemStorage(location='media/property_images')
        fs.save(image_name, image)
        pdata.property_image = f"property_images/{image_name}"

    pdata.save()
    return redirect('myProperty')


def deleteProperty(request,pid):
    pdata = models.AddProperty.objects.get(property_id=pid)
    if models.Bid.objects.filter(fk_property_id=pid).exists():
        # If there are associated bids, do not delete the property
        return redirect('myProperty')
    
    # Delete image file from media folder
    if pdata.property_image:
        image_path = os.path.join(settings.MEDIA_ROOT, pdata.property_image)
        if os.path.exists(image_path):
            os.remove(image_path)
            
    pdata.delete()

    return redirect('myProperty')

def viewPropertyDetails(request, pid):
    pdata = models.AddProperty.objects.get(property_id=pid)
    uname = request.session['semail']
    udata = models.Register.objects.get(email=uname)
    bid = models.Bid.objects.filter(
        fk_property_id=pid,
        fk_user_id=udata.user_id
    ).first()

    preq = models.PropertyRequest.objects.filter(
        fk_property_id=pid,
        fk_user_id=udata.user_id
    ).first()

    # Fetch broker and chat messages if bid exists
    broker = None
    messages_list = []
    if bid:
        # Get assigned broker for this property
        assigned = models.ScheduleBroker.objects.filter(fk_property_req_id=pid).first()
        if assigned:
            broker = models.Broker.objects.get(broker_id=assigned.fk_broker_id)

        # Get chat history
        messages_list = models.ChatBox.objects.filter(fk_bid_id=bid.bid_id).order_by('chat_time')

    context = {
        'property': pdata,
        'prequest': preq,
        'bid': bid,
        'broker': broker,
        'messages': messages_list,
        'user': udata
    }
    return render(request, 'user/property/viewPropertyDetails.html', context)

def userSendMessage(request):
    if request.method == 'POST':
        bid_id = request.POST.get('bid_id')
        message_text = request.POST.get('message', '').strip()
        broker_id = request.POST.get('broker_id')  # ✅ use broker_id sent by form
        pid = request.POST.get('pid')

        uname = request.session['semail']
        udata = models.Register.objects.get(email=uname)  # ✅ get sender from session

        if message_text and bid_id and broker_id:
            chat = models.ChatBox(
                message=message_text,
                chat_time=datetime.now(),
                fk_bid_id=bid_id,
                fk_chat_sender_id=udata.user_id,   # ✅ user's actual ID
                fk_chat_receiver_id=broker_id       # ✅ broker_id from form
            )
            chat.save()
        
        return redirect('viewPropertyDetails', pid=pid)
    return redirect('userDashboard')

def sendPropertyRequest(request):
    pid = request.POST['pid']
    uname = request.session['semail']
    udata = models.Register.objects.get(email=uname)

    # Prevent duplicate request
    if models.PropertyRequest.objects.filter(
        fk_property_id=pid,
        fk_user_id=udata.user_id
    ).exists():
        return redirect('viewPropertyDetails', pid=pid)

    prequest = models.PropertyRequest(
        fk_property_id = pid,
        fk_user_id = udata.user_id,
        property_req_status = "requested",
        request_date = datetime.now()
    )

    prequest.save()

    return redirect('viewPropertyDetails', pid=pid)

def placeBid(request):
    pid = request.POST['pid']
    bid_amount = request.POST['bid_amount']
    uname = request.session['semail']
    udata = models.Register.objects.get(email=uname)

    # ✅ ADDED VALIDATION: Prevent Negative or Zero bids
    try:
        if float(bid_amount) <= 0:
            messages.error(request, 'Bid amount must be greater than zero.')
            return redirect('viewPropertyDetails', pid=pid)
    except ValueError:
        messages.error(request, 'Invalid bid amount.')
        return redirect('viewPropertyDetails', pid=pid)

    bid = models.Bid(
        fk_property_id = pid,
        fk_user_id = udata.user_id,
        bid_amount = bid_amount,
        bid_date = datetime.now()
    )
    bid.save()

    return redirect('viewPropertyDetails', pid=pid)

def uploadProfileImage(request):

    email = request.session['semail']

    if request.method == "POST":

        file = request.FILES['profile_image']
        if not file:
            return HttpResponse("No file uploaded")

        allowed_types = ['jpg','jpeg','png','webp']

        ext = file.name.split('.')[-1].lower()

        if ext not in allowed_types:
            return HttpResponse("Upload JPG, jpeg,PNG or WEBP only")

        # filename = str(datetime.now().timestamp()).replace(".","") + "." + ext
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + "." + ext

        path = os.path.join(settings.MEDIA_ROOT,"user_profile_images",filename)


        with open(path,'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        models.Register.objects.filter(email=email).update(
            profile_image=filename
        )

        return redirect('userProfile')

    return render(request,'user/uploadProfileImage.html')

def myEnquiries(request):
    uname = request.session['semail']
    udata = models.Register.objects.get(email=uname)
    
    preqs = models.PropertyRequest.objects.filter(fk_user_id=udata.user_id)
    enquiries_list = []
    
    for req in preqs:
        prop = models.AddProperty.objects.get(property_id=req.fk_property_id)
        broker = None
        schedule = models.ScheduleBroker.objects.filter(fk_property_req_id=req.property_req_id).first()
        if schedule:
            broker = models.Broker.objects.get(broker_id=schedule.fk_broker_id)
            
        enquiries_list.append({
            'enquiry': req,
            'property': prop,
            'broker': broker
        })
        
    context = {'enquiries': enquiries_list}
    return render(request, 'user/property/myEnquiries.html', context)

def openChat(request, bid):
    uname = request.session['semail']
    udata = models.Register.objects.get(email=uname)
    
    bid_obj = models.Bid.objects.get(bid_id=bid)
    prop = models.AddProperty.objects.get(property_id=bid_obj.fk_property_id)
    
    # ✅ FIX: schedule_broker stores property_id in fk_property_req_id,
    # so look up by property_id directly — NOT by property_req_id
    broker = None
    schedule = models.ScheduleBroker.objects.filter(fk_property_req_id=prop.property_id).first()
    if schedule:
        broker = models.Broker.objects.get(broker_id=schedule.fk_broker_id)
            
    msgs = models.ChatBox.objects.filter(fk_bid_id=bid).order_by('chat_time')
    
    context = {
        'broker': broker,
        'property': prop,
        'messages': msgs,
        'user': udata,
        'bid_id': bid,
        'broker_id': broker.broker_id if broker else '',
        'pid': prop.property_id
    }
    return render(request, 'user/property/chat.html', context)

def send_user_message(request):
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        bid_id = request.POST.get('bid_id')
        broker_id = request.POST.get('broker_id')
        
        uname = request.session['semail']
        udata = models.Register.objects.get(email=uname)
        
        if message and bid_id and broker_id:
            chat = models.ChatBox(
                message=message,
                fk_chat_sender_id=udata.user_id,
                fk_chat_receiver_id=broker_id,
                fk_bid_id=bid_id,
                chat_time=datetime.now()
            )
            chat.save()
            
        return redirect('openChat', bid=int(bid_id))  # ✅ cast to int for URL pattern
    return redirect('userDashboard')

def predict_price_api(request):
    """
    API endpoint for asynchronous AI price prediction on the frontend.
    Retrieves latest user input via GET params and returns prediction as JSON.
    """
    # 1. Grab frontend form parameters
    district = request.GET.get('district')
    location = request.GET.get('location')
    area = request.GET.get('area')
    bedrooms = request.GET.get('bedrooms')

    # 2. Validate inputs
    if not district or not location or not area or not bedrooms:
        return JsonResponse({'error': 'Missing required fields for prediction'}, status=400)

    try:
        area_val = int(area)
        bedrooms_val = int(bedrooms)
    except ValueError:
         return JsonResponse({'error': 'Area and Bedrooms must be numbers'}, status=400)

    # 3. Use Singleton ML Model to Predict
    try:
        predicted_price = predict_house_price(
            district=district,
            area=area_val,
            bedrooms=bedrooms_val,
            location=location
        )
        return JsonResponse({'predicted_price': predicted_price, 'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
