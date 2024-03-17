
from django.urls import path
from bikeapp import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',views.homeFunction),
    path('login',views.userlogin),
    path('register',views.register),
    path('logout',views.userlogout),
    path('details/<pid>',views.bikedetails),
    path('addtocart/<bikeid>',views.addtocart),
    path('mycart',views.showMyCart),
    path('searchby/<val>',views.searchBikeByType),
    path('searchBike/<val>',views.searchBike),
    path('removecart/<cartid>',views.removeCart),
    path('confirmorder',views.confirmorder),
    path('pricerange',views.rangeofprice),
    path('sort/<dir>',views.sortBikesByPrice),
    path('makepayment',views.makepayment),
    path('placeorder',views.placeorder)
]

urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)