from django.shortcuts import render,redirect
from house import models
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Sum
from collections import defaultdict
import json
from django.contrib.auth.hashers import make_password
from django.db.models import Count, Avg, Sum
from collections import defaultdict
import json
from django.contrib.auth.hashers import make_password

import os
from datetime import datetime
from django.conf import settings

# Create your views here.

def adminDashboard(request):
    return render(request, 'admin/index.html')

def adminLayout(request):
    return render(request, 'admin/adminLayout.html')

def dashboardAdmin(request):
    if 'semail' not in request.session:
        return redirect('login')
    
    total_users = models.Register.objects.count()
    total_properties = models.AddProperty.objects.count()
    total_brokers = models.Broker.objects.count()
    total_requests = models.PropertyRequest.objects.count()
    
    # --- CHART 1: Properties per District (Pie/Doughnut) ---
    district_counts = models.AddProperty.objects.values('property_district').annotate(count=Count('property_id'))
    chart_districts = [d['property_district'] for d in district_counts]
    chart_district_counts = [d['count'] for d in district_counts]

    # --- CHART 2: AI Price Variance per District (Bar) ---
    price_variance = models.AddProperty.objects.exclude(price_predicted__isnull=True).values('property_district').annotate(
        avg_listed=Avg('price_listed'),
        avg_ai=Avg('price_predicted')
    )
    variance_districts = []
    variance_listed = []
    variance_ai = []
    for pv in price_variance:
        variance_districts.append(pv['property_district'])
        variance_listed.append(float(pv['avg_listed']) if pv['avg_listed'] else 0)
        variance_ai.append(float(pv['avg_ai']) if pv['avg_ai'] else 0)
        
    # --- CHART 3: Commission Revenue Over Time (Line) ---
    transactions = models.BrokerTransaction.objects.all()
    revenue_by_month = defaultdict(float)
    for t in transactions:
        if t.created_at:
            try:
                # Handle both datetime fields and raw string dates
                dt_str = t.created_at.strftime('%Y-%m') if hasattr(t.created_at, 'strftime') else str(t.created_at)[:7]
                revenue_by_month[dt_str] += float(t.commission)
            except Exception:
                pass
    
    sorted_months = sorted(revenue_by_month.keys())
    revenue_values = [revenue_by_month[m] for m in sorted_months]
    
    context = {
        'total_users': total_users,
        'total_properties': total_properties,
        'total_brokers': total_brokers,
        'total_requests': total_requests,
        'chart_districts': json.dumps(chart_districts),
        'chart_district_counts': json.dumps(chart_district_counts),
        'variance_districts': json.dumps(variance_districts),
        'variance_listed': json.dumps(variance_listed),
        'variance_ai': json.dumps(variance_ai),
        'revenue_months': json.dumps(sorted_months),
        'revenue_values': json.dumps(revenue_values),
    }
    return render(request, 'admin/dashBoard.html', context)

def changePassword(request):
    return render(request, 'admin/changePassword.html')

def updatePassword(request):
    npass = request.POST['new_password']
    cpass = request.POST['confirm_password']
    uname = request.session['semail']
    udata = models.Login.objects.get(user_name=uname)
    if npass ==cpass:
        udata.password = make_password(npass)
        udata.save()
        return redirect('login')
    return redirect("changePassword")

def broker(request):
    district = models.District.objects.all()
    bdata = models.Broker.objects.all()
    
    # Calculate total commission for each broker
    for b in bdata:
        # We need to join broker_transaction with schedule_broker to find commissions for this specific broker
        # In our system, schedule_broker.fk_property_req_id stores the property_id
        comm_data = models.BrokerTransaction.objects.raw("""
            SELECT t.broker_transaction_id, SUM(t.commission) as total_comm
            FROM broker_transaction as t
            JOIN schedule_broker as s ON s.fk_property_req_id = t.fk_property_id
            WHERE s.fk_broker_id = %s
        """, [b.broker_id])
        
        b.total_commission = 0
        for row in comm_data:
            if row.total_comm:
                b.total_commission = row.total_comm

    context = {
        'blist' : bdata,
        'districts': district
    }
    return render(request, 'admin/broker.html',context)



def saveBroker(request):
    name = request.POST['name']
    email = request.POST['email']
    gender = request.POST['gender']
    phone = request.POST['phone']
    district = request.POST['district']
    password = request.POST['password']
    
    existing_broker = models.Login.objects.filter(user_name=email).first()
    if existing_broker:
        messages.error(request, 'A broker with this email already exists.')
        return redirect('broker')

    # Handle profile image upload
    profile_image_filename = None
    if 'profile_image' in request.FILES:
        file = request.FILES['profile_image']
        ext = file.name.split('.')[-1].lower()
        allowed_types = ['jpg', 'jpeg', 'png', 'webp']
        if ext in allowed_types:
            profile_image_filename = datetime.now().strftime("%Y%m%d%H%M%S") + "." + ext
            path = os.path.join(settings.MEDIA_ROOT, "broker_profile_images", profile_image_filename)
            with open(path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
        else:
            messages.error(request, 'Upload JPG, JPEG, PNG or WEBP only for profile image.')
            return redirect('broker')

    Bdata = models.Broker(
        broker_name=name,
        broker_email=email,
        broker_gender=gender,
        broker_phone=phone,
        broker_district=district,
        profile_image=profile_image_filename
    )
    
    hashed_password = make_password(password)
    Udata = models.Login(user_name=email, password=hashed_password, user_type="broker", status="active")
    Bdata.save()
    Udata.save()
    messages.success(request, 'Broker added successfully.')
    return redirect('broker')

def editBroker(request,bid):
    district=models.District.objects.all()
    bdata = models.Broker.objects.get(broker_id=bid)
    context = {
        'blist' : bdata,
        'districts': district
    }
    return render(request, 'admin/editBroker.html',context)

def updateBroker(request):
    bid = request.POST['bid']
    name = request.POST['name']
    email = request.POST['email']
    gender = request.POST['gender']
    phone = request.POST['phone']
    district = request.POST['district']
    bdata=models.Broker.objects.get(broker_id=bid)
    bdata.broker_name = name
    bdata.broker_email = email
    bdata.broker_gender = gender
    bdata.broker_phone = phone
    bdata.broker_district = district

    if 'profile_image' in request.FILES:
        file = request.FILES['profile_image']
        ext = file.name.split('.')[-1].lower()
        allowed_types = ['jpg', 'jpeg', 'png', 'webp']
        if ext in allowed_types:
            profile_image_filename = datetime.now().strftime("%Y%m%d%H%M%S") + "." + ext
            path = os.path.join(settings.MEDIA_ROOT, "broker_profile_images", profile_image_filename)
            with open(path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
            bdata.profile_image = profile_image_filename
        else:
            messages.error(request, 'Upload JPG, JPEG, PNG or WEBP only for profile image.')
            return redirect('broker')

    bdata.save()
    messages.success(request, 'Broker updated successfully.')
    return redirect('broker')

def deleteBroker(request,bid):
    bdata = models.Broker.objects.get(broker_id=bid)
    uname = bdata.broker_email
    ldata = models.Login.objects.get(user_name=uname)
    bdata.delete()
    ldata.delete()
    return redirect('broker')

def registered_users(request):
    udata = models.Register.objects.all()
    context = {
        'ulist' : udata
    }
    return render(request, 'admin/registered_users.html',context)

def viewUserProperties(request):
    pdata = models.AddProperty.objects.all()
    context = {
        'properties' : pdata
    }
    return render(request, 'admin/property/viewProperty.html',context)

def viewUserPropertyDetails(request, pid):
    pdata = models.AddProperty.objects.get(property_id=pid)
    context = {
        'p' : pdata
    }
    return render(request, 'admin/property/viewUserPropertyDetails.html',context)

def viewPropertyLocation(request, pid):
    pdata = models.AddProperty.objects.get(property_id=pid)
    context = {
        'p' : pdata
    }
    return render(request, 'admin/property/viewPropertyLocation.html',context)

def assignBroker(request, pid):
    pdis = models.AddProperty.objects.get(property_id=pid)
    district = pdis.property_district
    bdata = models.Broker.objects.filter(broker_district=district)
    pdata = models.AddProperty.objects.get(property_id=pid)
    assigned = models.ScheduleBroker.objects.filter(
        fk_property_req_id=pid
    ).first()

    assigned_broker = models.Broker.objects.filter(
        broker_id=assigned.fk_broker_id
    ).first() if assigned else None

    context = {
        'bdata' : bdata,
        'property' : pdata,
        'district': district,
        'assigned': assigned,
        'assigned_broker': assigned_broker
    }
    return render(request, 'admin/property/assignBroker.html',context)

def assignBrokerTOProperty(request):
    pid = request.POST['pid']
    bid = request.POST['bid']
    if models.ScheduleBroker.objects.filter(fk_property_req_id=pid).exists():
        return redirect('assignBroker', pid=pid)
    sdata = models.ScheduleBroker(fk_property_req_id=pid, fk_broker_id=bid)
    sdata.save()
    return redirect('assignBroker', pid=pid)

def replaceBrokerForProperty(request):
    pid = request.POST['pid']
    new_bid = request.POST['bid']
    sdata = models.ScheduleBroker.objects.get(fk_property_req_id=pid)
    sdata.fk_broker_id = new_bid
    sdata.save()
    return redirect('assignBroker', pid=pid)

def deAssignBroker(request):
    pid = request.POST['pid']
    sdata = models.ScheduleBroker.objects.get(fk_property_req_id=pid)
    sdata.delete()
    return redirect('assignBroker', pid=pid)
    
def viewBrokerCommissions(request):
    commissions = models.BrokerTransaction.objects.raw("""
        SELECT t.*, p.property_name, r.full_name as buyer_name, b.broker_name
        FROM broker_transaction as t
        JOIN add_property as p ON t.fk_property_id = p.property_id
        JOIN register as r ON t.fk_buyer_id = r.user_id
        JOIN schedule_broker as s ON s.fk_property_req_id = p.property_id
        JOIN broker as b ON s.fk_broker_id = b.broker_id
    """)
    
    # Calculate total sum
    total_commission = 0
    for c in commissions:
        total_commission += float(c.commission)
    
    context = {
        'commissions': commissions,
        'total_commission': total_commission
    }
    return render(request, 'admin/viewBrokerCommissions.html', context)



def viewPropertyRequest(request):
    pro_list = list(models.PropertyRequest.objects.raw("""
        SELECT pr.*, ap.*, r.full_name, r.email, r.phone_number, b.broker_name, bd.bid_amount
        FROM property_request pr
        INNER JOIN add_property ap ON pr.fk_property_id = ap.property_id
        INNER JOIN register r ON pr.fk_user_id = r.user_id
        LEFT JOIN schedule_broker sb ON pr.fk_property_id = sb.fk_property_req_id
        LEFT JOIN broker b ON sb.fk_broker_id = b.broker_id
        LEFT JOIN bid bd ON pr.fk_property_id = bd.fk_property_id AND pr.fk_user_id = bd.fk_user_id
    """))
    paginator = Paginator(pro_list, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'view_request': page_obj
    }
    return render(request, 'admin/viewPropertyRequest.html', context)
def request_details(request,pid):
    pdata = models.AddProperty.objects.get(property_id=pid)
    context = {
        'p' : pdata
    }
    return render(request, 'admin/requested_property_details.html',context)

def view_contact_messages(request):
    messages_list = models.Contact.objects.all().order_by('-id')  # newest first
    return render(request, 'admin/contact_messages.html', {'messages': messages_list})
