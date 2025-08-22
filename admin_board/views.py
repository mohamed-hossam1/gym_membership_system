# pylint: disable=no-member
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Member
from django.contrib.auth.models import User
from .forms import MemberForm
import uuid
import secrets

import qrcode
from io import BytesIO
from django.core.files import File

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


def is_superuser_check(user):
    return user.is_authenticated and user.is_superuser

@login_required(login_url='login')
@user_passes_test(is_superuser_check, login_url='login')
def admin_dashboard(request):
    users = Member.objects.all().order_by('name')
    print(users[1].image.url)
    print(users[0].image.url)
    return render(request, 'admin-dashboard.html',{'users':users})


@login_required(login_url='login')
@user_passes_test(is_superuser_check, login_url='login')
def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)

            base_username = member.name.lower().replace(" ", "")[:10]
            unique_id_part = str(uuid.uuid4())[:8]
            generated_username = f"{base_username}_{unique_id_part}"

            while User.objects.filter(username=generated_username).exists():
                unique_id_part = str(uuid.uuid4())[:8]
                generated_username = f"{base_username}_{unique_id_part}"

            member.user_name = generated_username
            member.unique_id = unique_id_part

            auth_user = User.objects.create_user(
                username=generated_username,
                password=generated_username
            )
            member.user = auth_user

            member.save()

            qr_content = request.build_absolute_uri(reverse('edit-member', args=[member.unique_id]))
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_content)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            member.qr_code.save(f'qr_{member.user_name}.png', File(buffer), save=False)

            member.save()

            return HttpResponseRedirect(reverse('admin-dashboard'))
    else:
        form = MemberForm()
    return render(request, 'add-member.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(is_superuser_check, login_url='login')
def scan_qr(request):
    error_message = None

    if request.method == 'POST':
        qr_data = request.POST.get('qr_code_data')

        if qr_data:
            member_unique_id = None
            if 'edit-member/' in qr_data:
                try:
                    parts = qr_data.split('edit-member/')
                    if len(parts) > 1:
                        member_unique_id = parts[1].strip('/').split('/')[0]
                except Exception:
                    error_message = "Invalid QR Code Data format. Please ensure it's a valid URL."
            else:
                member_unique_id = qr_data

            if member_unique_id is not None:
                try:
                    member = Member.objects.get(unique_id=member_unique_id)
                    return HttpResponseRedirect(reverse('edit-member', args=[member.unique_id]))
                except Member.DoesNotExist:
                    error_message = f"Member with ID '{member_unique_id}' not found."
                except Exception as e:
                    error_message = f"An unexpected error occurred: {e}"
        else:
            error_message = "QR Code Data cannot be empty."

    return render(request, 'scan-qr.html', {'error_message': error_message})


@login_required(login_url='login')
@user_passes_test(is_superuser_check, login_url='login')
def edit_member(request, unique_id):
    user = get_object_or_404(Member, unique_id=unique_id)
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin-dashboard'))
    else:
        form = MemberForm(instance=user)
    return render(request, 'edit-member.html',{'form': form, 'user': user})


def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None and user.is_superuser:
            login(request, user)
            return HttpResponseRedirect(reverse('admin-dashboard'))

        try:
            member_profile = Member.objects.get(user_name=username)
            member_django_user = authenticate(request, username=username, password=password)

            if member_django_user is not None and member_django_user == member_profile.user:
                login(request, member_django_user)
                request.session['member_unique_id'] = member_profile.unique_id
                return HttpResponseRedirect(reverse('dashboard', args=[member_profile.unique_id]))
            else:
                error_message = "Username or password is wrong"
        except Member.DoesNotExist:
            error_message = "Username or password is wrong"
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"

    return render(request, 'login.html', {'error_message': error_message})


def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return HttpResponseRedirect(reverse('admin-dashboard'))
    elif request.user.is_authenticated and hasattr(request.user, 'member_profile'):
        return HttpResponseRedirect(reverse('dashboard', args=[request.user.member_profile.unique_id]))
    return HttpResponseRedirect(reverse('login'))