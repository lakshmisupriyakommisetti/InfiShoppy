from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView,DetailView,FormView,DeleteView,UpdateView
from infishop.forms import *
from infishop.models import Cart
from infishoppy import settings
class ProductPriceAscDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'productList.html'

    def get_object(self, queryset=None):
        print(self.kwargs)
        return get_object_or_404(Category, id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductPriceAscDetailView, self).get_context_data(**kwargs)
        category = context.get('category')
        print(category)
        search_query = self.kwargs['name']
        if (search_query != "none"):
            products = list(
                Product.objects.filter(name__icontains=search_query).values("id", "name", "description", "price",
                                                                                 "stock", "image",
                                                                                 'category__id').order_by(
                    'price'))
        else:
            products = list(
                category.product_set.values("id", "name", "description", "price", "stock", "image",
                                            'category__id').order_by('price'))
        context.update({
            'products': products,
            'category_id': kwargs['object'].id,
            'MEDIA_URL': settings.MEDIA_URL,
            'search_term': search_query,
            'user_permissions': self.request.user.get_all_permissions()})

        return context


class ProductPriceDescDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'productList.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Category, id = self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductPriceDescDetailView, self).get_context_data(**kwargs)
        category = context.get('category')
        # print(category)
        # print(self.kwargs)
        search_query = self.kwargs['name']
        if(search_query!="none"):
            products = list(Product.objects.filter(name__icontains = search_query).values("id", "name", "description", "price", "stock", "image",
                                                    'category__id').order_by('price').reverse())
        else:
            products = list(
                category.product_set.values("id", "name", "description", "price","stock", "image",'category__id').order_by('price').reverse())
        context.update({
            'products': products,
            'category_id': kwargs['object'].id,
            'MEDIA_URL': settings.MEDIA_URL,
            'search_term': search_query,
            'user_permissions': self.request.user.get_all_permissions()})
        return context

class productFilterListView(ListView):
    model = Product
    context_object_name = 'product'
    template_name = 'productList.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(productFilterListView, self).get_context_data(**kwargs)
        products = context.get('product')
        search_query = self.request.GET.get('search_box', None)
        if(search_query==""):
            context.update({
                'products': [],
                'category_id': 0,
                'MEDIA_URL': settings.MEDIA_URL,
                'search_term':"none",
                'user_permissions': self.request.user.get_all_permissions()})
        else:
            products = list(products.values("id", "name", "description", "price", "stock", "image",
                                                    'category__id').filter(name__icontains = search_query))
            if(products==[]):
                category_id = 0
            else:
                category_id = products[0]['category__id']
            context.update({
                'products': products,
                'category_id': category_id,
                'MEDIA_URL': settings.MEDIA_URL,
                'search_term': search_query,
                'user_permissions': self.request.user.get_all_permissions()})
        return context


class CategoryFilterListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'categoryList.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryFilterListView,self).get_context_data(**kwargs)
        categories = context.get('categories')
        context.update({
            'categories':categories.filter(name__icontains = self.request.GET.get('search_box', None)),
            'user_permissions':self.request.user.get_all_permissions()})
        return context


class AddToCartView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    raise_exception = True
    login_url = '/login/'
    model = Product
    context_object_name = 'products'
    template_name = "viewcart.html"
    permission_required = "infishop.add_cart"
    permission_denied_message = "user does not have permission to add item to this cart"

    def get_context_data(self, *, object_list=None, **kwargs):
        if(Cart.objects.filter(user=self.request.user,product = Product.objects.get(id=kwargs['object'].id)) != None):
            Cart.objects.filter(user=self.request.user, product=Product.objects.get(id=kwargs['object'].id)).delete()
        c = Cart(product=Product.objects.get(id=kwargs['object'].id), user=self.request.user,
                 quantity=self.request.GET.get('quan_box'))
        c.save()
        context = super(AddToCartView, self).get_context_data(**kwargs)
        products = Cart.objects.filter(user=self.request.user).values("id","product__id","product__name", "product__description",
                                                                 "product__price", "product__stock", "product__image","quantity")
        cost = 0
        for i in range(0, len(products)):
            cost += products[i]['product__price'] * products[i]['quantity'];
        context.update({'products':products,'cost':cost,'MEDIA_URL':settings.MEDIA_URL,'user_permissions':self.request.user.get_all_permissions()})
        return context


class ViewCart(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    model = User
    context_object_name = 'user'
    template_name = 'viewcart.html'
    def get_object(self, queryset=None):
        return get_object_or_404(User,pk=self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ViewCart,self).get_context_data(**kwargs)
        user = context.get('user')
        products = list(user.cart_set.values("id","product__id","product__name","product__description","product__price","product__stock","product__image","quantity"))
        cost = 0
        for i in range(0,len(products)):
            cost += products[i]['product__price'];
        context.update({
            'products':products,
            'cost':cost,
            'MEDIA_URL':settings.MEDIA_URL,
            'user_permissions':self.request.user.get_all_permissions()})
        return context


class RemoveFromCartView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    raise_exception = True
    login_url = '/login/'
    model = Cart
    permission_required = "infishop.delete_cart"
    permission_denied_message = "user does not have permission to delete this item"

    def get_success_url(self):
        return reverse_lazy('infishop:viewCart')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

class AddAddressView(LoginRequiredMixin,PermissionRequiredMixin,FormView):
    raise_exception = True
    login_url = '/login/'
    template_name = 'addAddress.html'
    form_class = AddShippingAddressForm
    permission_required = "infishop.add_shippingaddress"
    permission_denied_message = "user does not have permission to address address"

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.request.user.id)
        address_form = AddShippingAddressForm(request.POST)
        #print(product_form)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = user
            address.save()
            return redirect('infishop:viewAddress')
        return redirect('infishop:addAddress')

class ViewAddress(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    model = User
    context_object_name = 'user'
    template_name = 'viewAddress.html'
    def get_object(self, queryset=None):
        return get_object_or_404(User,pk=self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ViewAddress,self).get_context_data(**kwargs)
        user = context.get('user')
        addresses = list(user.shippingaddress_set.values("id","first_name","last_name","email","phoneno","address","postal_code","city"))
        context.update({
            'addresses':addresses,
            'user_permissions':self.request.user.get_all_permissions()})
        return context


def SuccessView(request):
    items = Cart.objects.filter(user=request.user);
    for item in items:
        product = Product.objects.get(id = item.product.id)
        product.stock = product.stock-item.quantity
        product.save()

    Cart.objects.filter(user=request.user).delete()
    return render(request, "success.html")



def HomeView(request):
    return render(request, "home.html")


class RemoveAddressView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    raise_exception = True
    login_url = '/login/'
    model = ShippingAddress
    permission_required = "infishop.delete_shippingaddress"
    permission_denied_message = "user does not have permission to delete address"

    def get_success_url(self):
        return reverse_lazy('infishop:viewAddress')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class UpdateAddressView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/login/'
    raise_exception = True
    model = ShippingAddress
    form_class = AddShippingAddressForm
    template_name = "addAddress.html"
    success_url = reverse_lazy('infishop:viewAddress')
    permission_required = "infishop.change_shippingaddress"
    permission_denied_message = "user does not have permission to change address"

    def get_object(self, queryset=None):
        return get_object_or_404(ShippingAddress, **self.kwargs)