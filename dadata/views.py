from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .forms import AddressForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class AddressCreate(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        form = AddressForm()
        return render(request, 'dadata/suggest.html', context={'form': form})

    def post(self, request):
        bound_form = AddressForm(request.POST)
        
        if bound_form.is_valid():
            bound_form.instance.author = self.request.user
            new_address = bound_form.save()
            return redirect(new_address)
        return render(request, 'dadata/suggest.html', context={'form': bound_form})

    def test_func(self):
        if self.request.user.groups.filter(name='agent').count() == 0:
            return False
        return True