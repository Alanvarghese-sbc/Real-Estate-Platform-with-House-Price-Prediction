import os
from django.http import HttpResponse
from django.shortcuts import render,redirect
from house import models
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from datetime import datetime

# from django.core.files.storage import FileSystemStorage
from django.conf import settings

def dashboardBroker(request):
    if 'semail' not in request.session:
        return redirect('login')
    
    uname = request.session['semail']
    broker = models.Broker.objects.get(broker_email=uname)
    
    # Statistics
    # 1. Total Assigned Properties
    assigned_count = models.ScheduleBroker.objects.filter(fk_broker_id=broker.broker_id).count()
    
    # 2. Total Commission Earned
    transactions = models.BrokerTransaction.objects.raw("""
        SELECT t.broker_transaction_id, SUM(t.commission) as total_comm
        FROM broker_transaction as t
        JOIN schedule_broker as s ON s.fk_property_req_id = t.fk_property_id
        WHERE s.fk_broker_id = %s
    """, [broker.broker_id])
    
    total_commission = 0
    for row in transactions:
        if row.total_comm:
            total_commission = row.total_comm
            
    # 3. Total Bids to Review for assigned properties
    # Get all property IDs assigned to this broker
    assigned_pids = models.ScheduleBroker.objects.filter(fk_broker_id=broker.broker_id).values_list('fk_property_req_id', flat=True)
    pending_bids_count = models.Bid.objects.filter(fk_property_id__in=assigned_pids).count()
    
    # Recent Scheduled Properties
    sch_data = models.ScheduleBroker.objects.raw("""
        SELECT * from add_property as p 
        JOIN schedule_broker as s on p.property_id = s.fk_property_req_id 
        JOIN register as r on r.user_id = p.fk_reg_id 
        WHERE s.fk_broker_id = %s 
        LIMIT 5
    """, [broker.broker_id])
    
    context = {
        'broker': broker,
        'assigned_count': assigned_count,
        'total_commission': total_commission,
        'pending_bids_count': pending_bids_count,
        'plist': sch_data
    }
    return render(request, 'broker/dashboardBroker.html', context)

def brokerProfile(request):
     uname =  request.session['semail']
     udata = models.Broker.objects.get(broker_email=uname)
     context = {
        'ulist': udata
    }
     return render(request,'broker/profile.html',context)

def  editBrokerProfile(request,bid):
     district= models.District.objects.all()
     bdata = models.Broker.objects.get(broker_id=bid)
     context ={
          'blist' : bdata,
          'districts': district
     }
     return render(request, 'broker/editProfile.html',context)

     
def updateBrokerProfile(request):
    bid = request.POST['bid']
    name = request.POST['name']
    email = request.POST['email']
    gender = request.POST['gender']
    phone = request.POST['phone']
    district = request.POST['district']

    bdata = models.Broker.objects.get(broker_id=bid)
    old_email = bdata.broker_email

    bdata.broker_name = name
    bdata.broker_email = email
    bdata.broker_gender = gender
    bdata.broker_phone = phone
    bdata.broker_district = district
    bdata.save()

    # Update corresponding Login username if it exists
    try:
        ldata = models.Login.objects.get(user_name=old_email)
        ldata.user_name = email
        ldata.save()
    except models.Login.DoesNotExist:
        pass

    # If the current session belongs to this broker, update session email
    if request.session.get('semail') == old_email:
        request.session['semail'] = email

    return redirect('brokerProfile') 

def changeBrokerPassword(request):
     return render(request,'broker/changeBrokerPassword.html')

def updateBrokerPassword(request):
    npass = request.POST['new_password']
    cpass = request.POST['confirm_password']
    uname = request.session['semail']
    udata = models.Login.objects.get(user_name=uname)
    if npass ==cpass:
        udata.password = make_password(npass)
        udata.save()
        return redirect('login')
    return redirect("changeBrokerPassword")

# def brokerScheduledProperties(request):
#     uname = request.session['semail']
#     if not uname:
#         return redirect('login')
#     bdata = models.Broker.objects.get(broker_email=uname)
#     scheduled_properties = models.ScheduleBroker.objects.filter(fk_broker_id=bdata.broker_id)
#     property_list = []
#     for schedule in scheduled_properties:
#         property = models.AddProperty.objects.get(property_id=schedule.fk_property_req_id)
#         property_list.append(property)


#     context = {
#         'scheduled_properties': scheduled_properties,
#         'property_list': property_list
#     }
#     return render(request, 'broker/scheduledPlots.html', context)

def viewSchdeuledPropertyDetails(request):
    uname = request.session['semail']
    bdata = models.Broker.objects.get(broker_email=uname)
    sch_data=models.ScheduleBroker.objects.raw("SELECT * from add_property as p JOIN schedule_broker as s on p.property_id = s.fk_property_req_id join register as r on r.user_id=p.fk_reg_id WHERE s.fk_broker_id = %s",[bdata.broker_id])

    context = {
        'plist': sch_data
    }

    return render(request, 'broker/scheduledPlots.html', context)

def brokerPropertyBids(request,pid):
    pdata = models.AddProperty.objects.get(property_id=pid)
    # Fetch requests and join with register table to get the user's name
    requests_raw = models.PropertyRequest.objects.raw("""
        SELECT pr.*, r.full_name 
        FROM property_request as pr
        JOIN register as r ON r.user_id = pr.fk_user_id
        WHERE pr.fk_property_id = %s
    """, [pid])
    
    requests_list = list(requests_raw)

    # Join with property_request to get the status of each user's request for this property
    bids = models.Bid.objects.raw("""
        SELECT b.*, r.full_name, pr.property_req_status 
        FROM bid as b 
        JOIN register as r ON r.user_id = b.fk_user_id 
        LEFT JOIN property_request as pr ON pr.fk_user_id = b.fk_user_id AND pr.fk_property_id = b.fk_property_id
        WHERE b.fk_property_id = %s 
        ORDER BY b.bid_amount DESC
    """, [pid])
    
    # Check if any request is already accepted
    is_accepted = any(r.property_req_status == "accepted" for r in requests_list)
    
    # Process Deal Indicator for Broker UI
    bids_list = list(bids)
    predicted = float(pdata.price_predicted) if pdata.price_predicted else None
    
    for b in bids_list:
        if predicted and predicted > 0:
            diff = float(b.bid_amount) - predicted
            pct = (diff / predicted) * 100
            if pct >= 10:
                b.deal_status = {'text': f'+{abs(int(pct))}% High', 'color': 'success'}
            elif pct <= -10:
                b.deal_status = {'text': f'-{abs(int(pct))}% Low', 'color': 'danger'}
            else:
                b.deal_status = {'text': 'Fair Bid', 'color': 'primary'}
        else:
            b.deal_status = None

    context = {
        'property': pdata,
        'requests': requests_list,
        'bids': bids_list,
        'is_accepted': is_accepted
    }
    return render(request, 'broker/propertyBids.html', context)

def acceptBid(request, bid_id):
    try:
        bid = models.Bid.objects.get(bid_id=bid_id)
        property_id = bid.fk_property_id
        user_id = bid.fk_user_id

        # Update property status to "sold"
        prop = models.AddProperty.objects.get(property_id=property_id)
        prop.property_status = "sold"
        prop.save()

        # Update property request status for the winning user
        prop_req = models.PropertyRequest.objects.filter(
            fk_property_id=property_id,
            fk_user_id=user_id
        ).first()
        if prop_req:
            prop_req.property_req_status = "accepted"
            prop_req.save()

        # Calculate 3% commission of accepted bid amount
        commission_amt = float(bid.bid_amount) * 0.03

        # Save to broker_transaction
        transaction = models.BrokerTransaction(
            fk_property_id = property_id,
            fk_buyer_id = user_id,
            amount = bid.bid_amount,
            commission = commission_amt,
            status = "paid",
            created_at = datetime.now().date()
        )
        transaction.save()

        # Optionally reject other bids/requests for this property
        other_requests = models.PropertyRequest.objects.filter(
            fk_property_id=property_id
        ).exclude(fk_user_id=user_id)
        other_requests.update(property_req_status="rejected")

        return redirect('brokerPropertyBids', pid=property_id)
    except models.Bid.DoesNotExist:
        return redirect('dashboardBroker')

def rejectBid(request, bid_id):
    try:
        bid = models.Bid.objects.get(bid_id=bid_id)
        property_id = bid.fk_property_id
        user_id = bid.fk_user_id

        # Mark only this user's property request as "rejected"
        prop_req = models.PropertyRequest.objects.filter(
            fk_property_id=property_id,
            fk_user_id=user_id
        ).first()

        if prop_req:
            prop_req.property_req_status = "rejected"
            prop_req.save()

        return redirect('brokerPropertyBids', pid=property_id)
    except models.Bid.DoesNotExist:
        return redirect('dashboardBroker')
def property_details(request,pid):
    pdata = models.AddProperty.objects.get(property_id=pid)
    context = {
        'property': pdata
    }
    return render(request, 'broker/propertyDetails.html', context)

def view_chat(request,bid):
   
        uname = request.session.get('semail')
        broker = models.Broker.objects.get(broker_email=uname)
        
        # Get chat messages (both directions)
        bid_obj = models.Bid.objects.get(bid_id=bid)
        user_id = bid_obj.fk_user_id
        pid = bid_obj.fk_property_id
        messages = models.ChatBox.objects.filter(
            fk_bid_id=bid).order_by('chat_time')
        
        
        user = models.Register.objects.get(user_id=user_id)
        prop = models.AddProperty.objects.get(property_id=pid)
        
        context = {
            'messages': messages,
            'user': user,
            'property': prop,
            'broker': broker,
            'user_id': user_id,
            'pid': pid,
            'bid_id': bid
        }
        return render(request, 'broker/chat.html', context)
    
def send_message(request):

    uname = request.session.get('semail')
    broker = models.Broker.objects.get(broker_email=uname)
  
    message_text = request.POST.get('message', '').strip()
    bid_id = request.POST['bid_id']
    user_id = request.POST['user_id']
    pid = request.POST['pid']          
    chat = models.ChatBox(
                    message=message_text,
                    chat_time=datetime.now(),
                    fk_bid_id=bid_id,
                    fk_chat_sender_id=broker.broker_id,
                    fk_chat_receiver_id=user_id
                )   
    chat.save()
            
    return redirect('view_chat', bid=bid_id)

def viewCommissions(request):
    uname = request.session.get('semail')
    broker = models.Broker.objects.get(broker_email=uname)
    
    # Get all transactions for properties associated with this broker
    commissions = models.BrokerTransaction.objects.raw("""
        SELECT t.*, p.property_name, r.full_name as buyer_name
        FROM broker_transaction as t
        JOIN add_property as p ON t.fk_property_id = p.property_id
        JOIN register as r ON t.fk_buyer_id = r.user_id
        JOIN schedule_broker as s ON s.fk_property_req_id = p.property_id
        WHERE s.fk_broker_id = %s
    """, [broker.broker_id])
    
    # Calculate Total Commission
    total_commission = 0
    for c in commissions:
        total_commission += float(c.commission)
    
    context = {
        'commissions': commissions,
        'total_commission': total_commission
    }
    return render(request, 'broker/viewCommissions.html', context)

def uploadBrokerProfileImage(request):

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

        path = os.path.join(settings.MEDIA_ROOT,"broker_profile_images",filename)


        with open(path,'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        models.Broker.objects.filter(broker_email=email).update(
            profile_image=filename
        )

        return redirect('brokerProfile')

    return render(request,'broker/uploadBrokerProfileImage.html')


    