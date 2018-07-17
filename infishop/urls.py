from django.urls import path
from infishop import views
app_name = "infishop"
urlpatterns = [
    path('categoryList/', views.CategoryListView.as_view(), name="categoryList"),
    path('addCategory/', views.AddCategoryView.as_view(), name="addCategory"),
    path('updateCategory/<int:pk>/', views.UpdateCategoryView.as_view(), name="updateCategory"),
    path('deleteCategory/<int:pk>/', views.DeleteCategoryView.as_view(), name="deleteCategory"),
    path('categoryList/<int:pk>/productList/', views.ProductDetailView.as_view(), name="productList"),
    path('categoryList/<int:pk>/addProduct/',views.AddProductView.as_view(), name = "addProduct"),
    path('categoryList/<int:category_id>/updateProduct/<int:pk>/', views.UpdateProductView.as_view(), name="updateProduct"),
    path('categoryList/<int:pk1>/deleteProduct/<int:pk>/', views.DeleteProductView.as_view(), name="deleteProduct"),
    path('categoryList/<int:pk>/productListByPriceAsc/<str:name>/', views.ProductPriceAscDetailView.as_view(), name="productListByPriceAsc"),
    path('categoryList/<int:pk>/productListByPriceDesc/<str:name>/', views.ProductPriceDescDetailView.as_view(), name="productListByPriceDesc"),
    path('categoryList/productListFilter/',views.productFilterListView.as_view(),name="productListFilter"),
    path('categoryListFilter/',views.CategoryFilterListView.as_view(),name="categoryListFilter"),
    path('addToCart/<int:pk>/',views.AddToCartView.as_view(),name = "addToCart"),
    path('removeFromCart/<int:pk>/',views.RemoveFromCartView.as_view(),name = "removeFromCart"),
    path('viewCart/',views.ViewCart.as_view(),name = "viewCart"),
    path('addAddress/',views.AddAddressView.as_view(),name = "addAddress"),
    path('viewAddress/', views.ViewAddress.as_view(), name="viewAddress"),
    path('updateAddress/<int:pk>/', views.UpdateAddressView.as_view(), name="updateAddress"),
    path('removeAddress/<int:pk>/', views.RemoveAddressView.as_view(), name="removeAddress"),
    path('success/', views.SuccessView, name="success"),
    path('', views.HomeView, name="home"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.Logout_user, name="logout"),
]