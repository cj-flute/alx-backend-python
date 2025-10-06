from django.shortcuts import render

# messaging/views.py
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def delete_user(request):
    user = request.user
    username = user.username

    # Delete the user (triggers post_delete signal)
    user.delete()

    messages.success(
        request, f"Account '{username}' has been deleted successfully.")
    return redirect('home')  # replace 'home' with your homepage route name
