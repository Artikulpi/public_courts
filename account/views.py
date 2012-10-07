from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, AdminPasswordChangeForm
from account.decorators import admin_required, referer_matches_re
from account.forms import NewUserForm, ProfileForm, RegistrationForm
from account.models import UserProfile
from datetime import timedelta
from django.utils import timezone
import hashlib

@admin_required
def new(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("./")
    else:
        form = NewUserForm()

    return render_to_response("account/new.html",
                            {"form": form,},
                            context_instance=RequestContext(request))

@admin_required
def view_account(request, user_id):
    try:
        view_user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        raise Http404
    
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=view_user)
        if form.is_valid():
            form.save()
    else:
        form = UserChangeForm(instance=view_user)
    
    return render_to_response("account/view.html",
                                {"view_user": view_user, "form": form,},
                                context_instance=RequestContext(request)
                            )

@admin_required
def delete_account(request, user_id):
    if request.method == "POST":
        try:
            delete_user = User.objects.get(pk=request.POST.get('user-id'))
            delete_user.is_active = False
            delete_user.save()
        except ObjectDoesNotExist:
            raise Http404

    return HttpResponseRedirect('/account/admin/')

def change_password(request, user_id):
    try:
        passwd_user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        raise Http404
    
    if request.method == "POST":
        form = AdminPasswordChangeForm(passwd_user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/account/admin/')
    
    else:
        form = AdminPasswordChangeForm(passwd_user)
    
    return render_to_response("account/passwd.html",
                                {"form": form, "passwd_user": passwd_user},
                                context_instance=RequestContext(request))

@admin_required
def admin(request):
    select = request.GET.get('q', 'all')
    users = {
        "all" : lambda : User.objects.all().order_by('-id'),
        "active" : lambda : User.objects.filter(is_active=True).order_by('-id'),
        "inactive" : lambda : User.objects.filter(is_active=False).order_by('-id'),
        "admin" : lambda : User.objects.filter(is_superuser=True).order_by('-id'),
        "staff" : lambda : User.objects.filter(is_staff=True,
                                            is_superuser=False).order_by('-id'),
        "user" : lambda : User.objects.filter(is_active=True,
                            is_superuser=False, is_staff=False).order_by('-id')
    }.get(select, lambda : User.objects.all().order_by('-id'))()
    
    return render_to_response('account/admin.html',
                            {"users": users},
                            context_instance=RequestContext(request))

@login_required
def profile(request):
    user_profile = request.user.get_profile()
    return render_to_response('account/profile/view.html',
                            {"profile": user_profile, },
                            context_instance=RequestContext(request))

@login_required
def profile_edit(request):
    current_user = request.user
    user_object = User.objects.get(pk=current_user.id)
    current_profile = current_user.get_profile()
    profile_object = UserProfile.objects.get(pk=current_profile.id)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, logged_user=user_object, user_profile=profile_object)
            
        if form.is_valid():
            form.save_user()
            form.save_profile()
            return HttpResponseRedirect('/account/profile/')
            
    else:
        profile = {
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "email": current_user.email,
            "address": current_profile.address,
            "phone": current_profile.phone,
        }
        form = ProfileForm(initial=profile)
        
    return render_to_response('account/profile/edit.html',
                            {"form": form, },
                            context_instance=RequestContext(request))

    
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user_profile = UserProfile.objects.get(pk=new_user.id)
            user_profile.address = form.cleaned_data["address"]
            user_profile.city = form.cleaned_data["city"]
            user_profile.phone = form.cleaned_data["phone"]
            user_profile.token = hashlib.sha224('%s%s' % (new_user.username,
                                    timezone.now())).hexdigest()
            user_profile.expire = timezone.now() + timedelta(days=7)
            user_profile.save()
            #TODO: send confirmation email
            
            return HttpResponseRedirect(
                        "/account/register/success/?u=%s&m=%s" % (
                        new_user.username, new_user.email))
    else:
        form = RegistrationForm()

    return render_to_response("account/register.html",
                            {"form": form, },
                            context_instance=RequestContext(request))

@referer_matches_re('/account/register/')
def register_success(request):
    new_user = request.GET.get('u', '')
    user_mail = request.GET.get('m', '')
    
    return render_to_response("account/success.html",
                            {"new_user": new_user, "user_mail": user_mail, },
                            context_instance=RequestContext(request))

def confirm(request, username, token):
    try:
        user_confirm = User.objects.get(username=username)
        if user_confirm.is_active:
            return HttpResponseRedirect('/')
            
        profile_user = user_confirm.get_profile()
        expire = profile_user.expire
        
        if profile_user.token == token and profile_user.expire > timezone.now():
            user_confirm.is_active = True
            user_confirm.save()
            confirm_error = False
            user_confirmed = user_confirm.username
        else:
            confirm_error = True
            user_confirmed = None
            
    except ObjectDoesNotExist:
        confirm_error = True
        user_confirmed = None
        
    return render_to_response("account/confirm.html",
                            {"confirm_error": confirm_error,
                            "user_confirmed": user_confirmed, },
                            context_instance=RequestContext(request))
