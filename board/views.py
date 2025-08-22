# pylint: disable=no-member
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from admin_board.models import Member
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required(login_url='login')
def dashboard(request, unique_id):
    if not hasattr(request.user, 'member_profile') or str(request.user.member_profile.unique_id) != str(unique_id):
        return HttpResponseRedirect(reverse('login'))

    member = request.user.member_profile
    return render(request, 'dashboard.html', {'member': member, 'user': member})