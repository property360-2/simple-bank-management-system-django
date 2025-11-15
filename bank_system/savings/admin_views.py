from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import SavingsProduct
from .admin_forms import SavingsProductForm
from users.decorators import manager_required


@manager_required
def savings_products_list(request):
    """List all savings products"""
    products = SavingsProduct.objects.all()

    context = {'products': products}
    return render(request, 'admin/savings_products_list.html', context)


@manager_required
def savings_product_create(request):
    """Create a new savings product"""
    if request.method == 'POST':
        form = SavingsProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Savings product created successfully!')
            return redirect('admin_panel:savings_products_list')
    else:
        form = SavingsProductForm()

    context = {'form': form, 'title': 'Create Savings Product'}
    return render(request, 'admin/savings_product_form.html', context)


@manager_required
def savings_product_edit(request, pk):
    """Edit a savings product"""
    product = get_object_or_404(SavingsProduct, pk=pk)

    if request.method == 'POST':
        form = SavingsProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Savings product updated successfully!')
            return redirect('admin_panel:savings_products_list')
    else:
        form = SavingsProductForm(instance=product)

    context = {'form': form, 'product': product, 'title': f'Edit {product.name}'}
    return render(request, 'admin/savings_product_form.html', context)


@manager_required
def savings_product_delete(request, pk):
    """Delete a savings product"""
    product = get_object_or_404(SavingsProduct, pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Savings product deleted successfully!')
        return redirect('admin_panel:savings_products_list')

    context = {'product': product}
    return render(request, 'admin/confirm_delete.html', context)
