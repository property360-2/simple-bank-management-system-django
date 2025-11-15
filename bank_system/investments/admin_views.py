from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import InvestmentProduct, InvestmentPlatform
from .admin_forms import InvestmentProductForm, InvestmentPlatformForm
from users.decorators import manager_required


@manager_required
def investment_products_list(request):
    """List all investment products"""
    products = InvestmentProduct.objects.all()
    platforms = InvestmentPlatform.objects.all()

    platform_filter = request.GET.get('platform')
    if platform_filter:
        products = products.filter(platform_id=platform_filter)

    context = {
        'products': products,
        'platforms': platforms,
        'current_platform': platform_filter,
    }
    return render(request, 'admin/investment_products_list.html', context)


@manager_required
def investment_product_create(request):
    """Create a new investment product"""
    if request.method == 'POST':
        form = InvestmentProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment product created successfully!')
            return redirect('admin:investment_products_list')
    else:
        form = InvestmentProductForm()

    context = {'form': form, 'title': 'Create Investment Product'}
    return render(request, 'admin/investment_product_form.html', context)


@manager_required
def investment_product_edit(request, pk):
    """Edit an investment product"""
    product = get_object_or_404(InvestmentProduct, pk=pk)

    if request.method == 'POST':
        form = InvestmentProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment product updated successfully!')
            return redirect('admin:investment_products_list')
    else:
        form = InvestmentProductForm(instance=product)

    context = {'form': form, 'product': product, 'title': f'Edit {product.name}'}
    return render(request, 'admin/investment_product_form.html', context)


@manager_required
def investment_product_delete(request, pk):
    """Delete an investment product"""
    product = get_object_or_404(InvestmentProduct, pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Investment product deleted successfully!')
        return redirect('admin:investment_products_list')

    context = {'product': product}
    return render(request, 'admin/confirm_delete.html', context)


@manager_required
def investment_platforms_list(request):
    """List all investment platforms"""
    platforms = InvestmentPlatform.objects.all()

    context = {'platforms': platforms}
    return render(request, 'admin/investment_platforms_list.html', context)


@manager_required
def investment_platform_create(request):
    """Create a new investment platform"""
    if request.method == 'POST':
        form = InvestmentPlatformForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment platform created successfully!')
            return redirect('admin:investment_platforms_list')
    else:
        form = InvestmentPlatformForm()

    context = {'form': form, 'title': 'Create Investment Platform'}
    return render(request, 'admin/investment_platform_form.html', context)


@manager_required
def investment_platform_edit(request, pk):
    """Edit an investment platform"""
    platform = get_object_or_404(InvestmentPlatform, pk=pk)

    if request.method == 'POST':
        form = InvestmentPlatformForm(request.POST, instance=platform)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment platform updated successfully!')
            return redirect('admin:investment_platforms_list')
    else:
        form = InvestmentPlatformForm(instance=platform)

    context = {'form': form, 'platform': platform, 'title': f'Edit {platform.name}'}
    return render(request, 'admin/investment_platform_form.html', context)


@manager_required
def investment_platform_delete(request, pk):
    """Delete an investment platform"""
    platform = get_object_or_404(InvestmentPlatform, pk=pk)

    if request.method == 'POST':
        platform.delete()
        messages.success(request, 'Investment platform deleted successfully!')
        return redirect('admin:investment_platforms_list')

    context = {'platform': platform}
    return render(request, 'admin/confirm_delete.html', context)
