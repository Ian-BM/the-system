from django.urls import path

from . import views

app_name = "system"

urlpatterns = [
    path("setup/", views.SetupView.as_view(), name="setup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("body/", views.BodyView.as_view(), name="body"),
    path("mind/", views.MindView.as_view(), name="mind"),
    path("money/", views.MoneyView.as_view(), name="money"),
    path("log/", views.LogView.as_view(), name="log"),
    path("api/quest/toggle/", views.ToggleQuestView.as_view(), name="api_toggle_quest"),
    path("api/weight/", views.SaveWeightView.as_view(), name="api_save_weight"),
    path("api/trading/", views.SaveTradingView.as_view(), name="api_save_trading"),
    path("api/journal/", views.SaveJournalView.as_view(), name="api_save_journal"),
    path("api/scold/dismiss/", views.ScoldDismissView.as_view(), name="api_scold_dismiss"),
    path("sw.js", views.ServiceWorkerView.as_view(), name="service_worker"),
    path("offline/", views.OfflineView.as_view(), name="offline"),
]
