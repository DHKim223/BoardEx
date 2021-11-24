from django.urls import path
from board import views
from django.views.generic.base import TemplateView
urlpatterns = [
    path("boardlist",views.boardlist,name="boardlist"),
#    path("write",views.write,name="write"),
#    path("writepro",views.writepro,name="writepro"),
    path("writepro",views.writepro,name="writepro"),
    path( "detail",views.detail,name = "detail"),
    #path( "delete", views.delete, name="delete" ),
    path( "deletepro", views.deletepro, name="deletepro" ),
    #path( "modify",views.modify, name="modify"),
    path("modifyview",views.modifyview,name="modifyview"),
    path("modifypro",views.modifypro,name="modifypro"),
    
]