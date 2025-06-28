from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, ProfileEditForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Compte créé avec succès ! Vous pouvez maintenant vous connecter.')
        return response

@login_required
def profile_view(request):
    """Page de profil utilisateur"""
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })

@login_required
def edit_profile_view(request):
    """Modification du profil utilisateur"""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès !')
            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

def logout_view(request):
    """Vue de déconnexion personnalisée"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('products:index')
