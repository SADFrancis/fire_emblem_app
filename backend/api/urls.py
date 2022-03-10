from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.getRoutes, name="routes" ),
    path('realms/',views.realms, name= "Dict of realms"),
    path('realms/<str:key>/', views.realmList, name="Resplendents of Realm Key Specified"),
    path('characters/', views.CharacterList.as_view(), name="Entire character Roster" ),
    path('characters/<str:Name>/', views.characterDetail, name="character" ),
    path('titles/',views.game_titles, name= "Dict of Game titles"),
    path('titles/<str:key>/', views.titleList, name="Resplendents of Game Title Key Specified"),
    path('year/', views.CharacterList.as_view(), name="List of characters, to setup for other endpoints" ),
    path('year/<str:year>', views.yearList, name="Character by year" ),
    path('year/<str:year>/<str:month>', views.monthOfYearList, name="Character by month of said year" ),
    path('characters/latest', views.LatestDetail, name = "Returns the most recently added Resplendent"),
    path('characters/updatelatestarchived', views.UpdateLatestArchived, name = "Update the game_origin of the most recently archived Resplendent"),
    path('login/',LoginView.as_view(), name="try")
 ]
