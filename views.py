
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import logout
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .models import User,AboutParagraph, Feedback,Transaction,Statement,Referral,Message,Notification,Address,FAQ,FactAtAGlance,Objective,SocialNetwork
from .forms import FeedbackForm, RegisterForm, UserForm

from  django.contrib.auth.hashers import make_password

home_variables = {}
home_variables['address'] = Address.objects.all()[:1]
home_variables['facts'] = FactAtAGlance.objects.order_by('fact_order')[:10]
home_variables['objective'] = Objective.objects.all()[:1]
home_variables['faqs'] = FAQ.objects.all()
home_variables['social'] = SocialNetwork.objects.all()[:7]
home_variables['about'] = AboutParagraph.objects.order_by('paragraph_order')[:3] 

def aboutus(request):
    template = loader.get_template('royalking/aboutus.html')
    return HttpResponse(template.render())

def contactus(request):
    template = loader.get_template('royalking/contactus.html')
    return HttpResponse(template.render())

def send_message(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            product = request.POST['product']
            subject = request.POST["subject"]
            message = request.POST["message"]
            user = request.user
            sendmessage = Message(sender=user,product=product,subject=subject,message=message)
            sendmessage.save()
            if (sendmessage.id):
                total_earnings = len(Referral.objects.filter(referred_by=request.user.username,fee_paid=True)) * 150
                return render(request, 'royalking/send_message.html',{'total': total_earnings,'success':True})
            if (sendmessage.id):
                total_earnings = len(Referral.objects.filter(referred_by=request.user.username,fee_paid=True)) * 150
                return render(request, 'royalking/send_message.html',{'total': total_earnings,'success':False})
        total_earnings = len(Referral.objects.filter(referred_by=request.user.username,fee_paid=True)) * 150
        return render(request, 'royalking/send_message.html',{'total': total_earnings})
    else:
        return redirect('/')

def notifications(request):
    if request.user.is_authenticated:
        notfs = Notification.objects.order_by('-timesent').filter(to=request.user)
        total_earnings = len(Referral.objects.filter(referred_by=request.user.username,fee_paid=True)) * 150
        return render(request, 'royalking/notifications.html',{'total': total_earnings,'notifications': notfs})
    else:
        return redirect('/')

def surveys(request):
    if request.user.is_authenticated:
        total_earnings = len(Referral.objects.filter(referred_by=request.user.username,fee_paid=True)) * 150
        return render(request, 'royalking/surveys.html',{'total': total_earnings})
    else:
        return redirect('/')

def profile(request):
    if request.user.is_authenticated:
        total_earnings = len(Referral.objects.filter(referred_by=request.user.username,fee_paid=True)) * 150
        return render(request, 'royalking/profile.html',{'total': total_earnings})
    else:
        return redirect('/')

def withdraw_earnings(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            amount = request.POST['amount']
            user = request.user
            transaction_code = 'QA23N231T'
            withdraw = Transaction(user=user,amount=amount,transaction_code=transaction_code,transaction_type='Withdrawal',status='pending',phone=user.tel)
            withdraw.save()
            if (withdraw.id):
                total_earnings = len(Referral.objects.filter(referred_by=request.user.username,fee_paid=True)) * 150
                return render(request, 'royalking/index.html',{'total': total_earnings,'success':True,'success_msg':'Withdrawal Request sent.'})
            else:
                total_earnings = len(Referral.objects.filter(referred_by=request.user.username,fee_paid=True)) * 150
                return render(request, 'royalking/index.html',{'total': total_earnings,'success':False,'success_msg':'Your request could not be Sent. Try again later .'})
        total_earnings = len(Referral.objects.filter(referred_by=request.user.username,fee_paid=True)) * 150
        if total_earnings>100:
            withdrawable = True
        else:
            withdrawable = False
        return render(request, 'royalking/withdraw_earnings.html',{'total': total_earnings,'withdrawable': withdrawable})
    else:
        return render(request, 'royalking/home.html')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'royalking/change_password.html', {
        'form': form
    })

def password_reset(request):
    if request.method == 'POST':
        user = User.objects.filter(tel=request.POST['phone'])
        if(user):
            return redirect('/login_user')
        else:
            return render(request,'royalking/reset_password.html',{ 'error':'Phone number not registered'})
    return render(request, 'royalking/reset_password.html')

def feedback(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        tel = request.POST['tel']
        can_be_contacted = request.POST['approve']
        if(can_be_contacted == 'on'):
            can_be_contacted = True
        else:
            can_be_contacted = False
        message = request.POST['message']
        feedback = Feedback(firstname=firstname,lastname=lastname,tel=tel,email=email,can_be_contacted=can_be_contacted,message=message)
        feedback.save()
        if(feedback.id):
            success = True
            success_message = "Thank you for your feedback."
            return render(request, 'royalking/home.html', {'home': home_variables,'success': success,'success_message':success_message})
        else:
            success = False
            error_message = "Your feedback could not be sent. Try again later"
            return render(request, 'royalking/home.html', {'success': success,'error_message':error_message})
    return redirect('/#contactus')

def register(request):
    if request.user.is_authenticated:
        return render(request, 'royalking/index.html')
    else:
        form = RegisterForm(request.POST or None, request.FILES or None,request.GET or None)
        if form.is_valid():
            register = form.save(commit=False)
            register.first_name = request.POST['first_name']
            register.last_name = request.POST['last_name']
            register.package = request.POST['package']
            register.email = request.POST['email']
            register.tel = request.POST['tel']
            register.username = request.POST['username'] 
            register.password = make_password(request.POST['password'], salt=None, hasher='default') 
            register.is_active = True   
            register.save()
            if request.GET:
                reffered_by = request.GET['ref']
                if reffered_by:
                    try:
                        referral_code = User.objects.get(referral_code=reffered_by)
                        if not referral_code.is_staff:
                            current_user = User.objects.get(username = request.POST['username'])
                            referral = Referral( user=current_user,referred_by=referral_code)
                            referral.save()
                    except( ObjectDoesNotExist,ValidationError ):
                        pass
                    else:
                        pass
            return render(request, 'royalking/confirm_payment.html', {'register': register})
        context = {
            "form": form,
        }
        return render(request, 'royalking/signup.html', context)

def make_payment(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            return render(request, 'royalking/login.html')
        return render(request, 'royalking/confirm_payment.html')
    else:
        return redirect('/home')
    


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username", False)
        password = request.POST.get("password", False)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/home')
            else:
                return render(request, 'royalking/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'royalking/login.html', {'error_message': 'Invalid login'})
    return render(request, 'royalking/login.html')

def home(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        total_earnings = len(Referral.objects.filter(referred_by=request.user.username,fee_paid=True)) * 150
        count = len(Referral.objects.filter(referred_by=request.user.username,fee_paid=False))
        if len(Referral.objects.filter(referred_by=request.user.username)) > 0:
            completed = (len(Referral.objects.filter(referred_by=request.user.username,fee_paid=False))/len(Referral.objects.filter(referred_by=request.user.username)))*100
        else:
            completed = 0
        return render(request, 'royalking/index.html',{'total':total_earnings,'count': count, 'completed': int(completed)})

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'royalking/home.html',{'home': home_variables})
    else:
        return redirect('/home')

def deposit(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        total_earnings = len(Referral.objects.filter(referred_by=request.user.username,fee_paid=True)) * 150
        return render(request, 'royalking/deposit.html',{'total':total_earnings })

def transactions(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        transactions = Transaction.objects.filter(user = request.user)
        query = request.GET.get("product_type")
        if query:
            transactions = Transaction.objects.filter(transaction_type = query).distinct()
            return render(request, 'royalking/transactions.html',{'transactions': transactions})
        else:
            return render(request, 'royalking/transactions.html',{'transactions': transactions})
def statements(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        stats = Statement.objects.filter(account = request.user)
        query = request.GET.get("product_type")
        if query:
            stats = Statement.objects.filter(statement_type = query).distinct()
            return render(request, 'royalking/statement.html',{'statements': stats})
        else:
            return render(request, 'royalking/statement.html',{'statements': stats})

def buy_airtime(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'royalking/buy_airtime.html')

def referral_earnings(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        try:
            referrals = Referral.objects.filter(referred_by=request.user.username)
            total_earnings = len(Referral.objects.filter(referred_by=request.user.username,fee_paid=True)) * 150
            return render(request, 'royalking/refferals.html',{'referrals': referrals, 'total': total_earnings,'count': len(referrals)})
        except( ObjectDoesNotExist,ValidationError ):
            pass
    return render(request, 'royalking/refferals.html')
    
def logout_user(request):
    logout(request)
    return redirect('/')

def terms_and_conditions(request):
    return render(request,'royalking/terms_and_conditions.html')

def privacy_policy(request):
    return render(request,'royalking/privacy_policy.html')

def terms(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'royalking/terms.html')

def privacy(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'royalking/privacy.html')

