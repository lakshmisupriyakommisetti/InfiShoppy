from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,FormView,DeleteView,UpdateView
from infishop.forms import *
from infishoppy import settings

class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'categoryList.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView,self).get_context_data(**kwargs)
        context.update({'user_permissions':self.request.user.get_all_permissions()})
        return context


class AddCategoryView(LoginRequiredMixin,PermissionRequiredMixin,FormView):
    login_url = '/login/'
    raise_exception = True
    template_name = 'addCategory.html'
    form_class= AddCategoryForm
    permission_required = "infishop.add_category"
    permission_denied_message = "user does not have permission to add a category"

    def post(self, request, *args, **kwargs):
        category_form = AddCategoryForm(request.POST)
        if category_form.is_valid():
            college = category_form.save(commit=True)
            return redirect('infishop:categoryList')


class UpdateCategoryView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/login/'
    raise_exception = True
    model = Category
    form_class = AddCategoryForm
    template_name = "addCategory.html"
    success_url = reverse_lazy('infishop:categoryList')
    permission_required = "infishop.change_category"
    permission_denied_message = "user does not have permission to change a category"

    def get_object(self, queryset=None):
        return get_object_or_404(Category, **self.kwargs)


class DeleteCategoryView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/login/'
    raise_exception = True
    model = Category
    success_url = reverse_lazy('infishop:categoryList')
    permission_required = "infishop.delete_category"
    permission_denied_message = "user does not have permission to delete a category"
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

class AddProductView(LoginRequiredMixin,PermissionRequiredMixin,FormView):
    login_url = '/login/'
    raise_exception = True
    template_name = 'addProduct.html'
    form_class = AddProductForm
    permission_required = "infishop.add_product"
    permission_denied_message = "user does not have permission to add a product"

    def post(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk=kwargs.get('pk'))
        product_form = AddProductForm(request.POST, request.FILES)
        print(product_form)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.category = category
            product.save()
            return redirect('infishop:productList',kwargs.get('pk'))
        return redirect('infishop:addProduct',kwargs.get('pk'))

class ProductDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'productList.html'
    def get_object(self, queryset=None):
        return get_object_or_404(Category,**self.kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView,self).get_context_data(**kwargs)
        category = context.get('category')
        print(category)
        products = list(category.product_set.values("id","name","description","price","stock","image",'category__id'))
        context.update({
            'products':products,
            'category_id':kwargs['object'].id,
            'MEDIA_URL':settings.MEDIA_URL,
            'search_term':"none",
            'user_permissions':self.request.user.get_all_permissions()})
        return context


class UpdateProductView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/login/'
    raise_exception = True
    model = Product
    permission_required = "infishop.change_product"
    permission_denied_message = "user does not have permission to change a product"
    form_class = AddProductForm
    template_name = "addProduct.html"
    # success_url = reverse_lazy('infishop:productList')

    def get_success_url(self):
        print(self.kwargs)
        return reverse_lazy('infishop:productList',
                            kwargs={'pk': self.kwargs.get('category_id', None)}, )
    def get_object(self, queryset=None):
        return get_object_or_404(Product, **self.kwargs)


class DeleteProductView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/login/'
    raise_exception = True
    model = Product
    permission_required = "infishop.delete_product"
    permission_denied_message = "user does not have permission to delete a product"
    def get_success_url(self):
        return reverse_lazy('infishop:productList',
                            kwargs={'pk': self.kwargs.get('pk1', None)}, )


    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)