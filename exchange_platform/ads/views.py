from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm

@login_required  # Только авторизованные пользователи могут создавать объявления
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)  # Не сохраняем сразу в базу данных
            ad.user = request.user  # Привязываем объявление к текущему пользователю
            ad.save()  # Сохраняем объявление
            return redirect('ad_list')  # Перенаправляем на страницу со списком объявлений
    else:
        form = AdForm()
    return render(request, 'ads/create_ad.html', {'form': form})
@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_list')
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/edit_ad.html', {'form': form})

@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)
    ad.delete()
    return redirect('ad_list')

def ad_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    condition = request.GET.get('condition')

    ads = Ad.objects.all()
    if query:
        ads = ads.filter(title__icontains=query) | ads.filter(description__icontains=query)
    if category:
        ads = ads.filter(category=category)
    if condition:
        ads = ads.filter(condition=condition)

    paginator = Paginator(ads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ads/ad_list.html', {'page_obj': page_obj})

@login_required
def create_exchange_proposal(request, ad_id):
    receiver_ad = get_object_or_404(Ad, id=ad_id)
    sender_ads = Ad.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_sender = sender_ads.get(id=request.POST['ad_sender'])
            proposal.ad_receiver = receiver_ad
            proposal.save()
            return redirect('ad_list')
    else:
        form = ExchangeProposalForm(initial={'ad_receiver': receiver_ad})
    return render(request, 'ads/create_exchange_proposal.html', {'form': form, 'sender_ads': sender_ads})

@login_required
def update_exchange_proposal(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id, ad_receiver__user=request.user)
    if request.method == 'POST':
        proposal.status = request.POST.get('status')
        proposal.save()
        return redirect('exchange_proposals')
    return render(request, 'ads/update_exchange_proposal.html', {'proposal': proposal})

@login_required
def exchange_proposals(request):
    proposals = ExchangeProposal.objects.filter(ad_receiver__user=request.user)
    return render(request, 'ads/exchange_proposals.html', {'proposals': proposals})