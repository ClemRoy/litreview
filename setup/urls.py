"""setup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path

import authentication.views
import review.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name="authentication/login.html",
        redirect_authenticated_user=True
    ), name='login'),
    path("logout/", authentication.views.logout_user, name="logout"),
    path("home/", review.views.home, name="home"),
    path("yourpost/", review.views.your_post, name="your_post"),
    path("follows/", review.views.follows, name="follows"),
    path("deletefollower/<int:key_id>/",
         review.views.delete_follower, name="delete_follower"),
    path("signup/", authentication.views.signup_page, name="signup"),
    path("ticket/", review.views.ticket, name="ticket"),
    path("ticket/<int:id>/delete_ticket/",
         review.views.delete_ticket, name="delete_ticket"),
    path("ticket/<int:id>/ticket_update/",
         review.views.ticket_update, name="ticket_update"),
    path("ticket/<int:id>/answer/",
         review.views.answer_ticket, name="answer_ticket"),
    path("ticket/<int:id>/update_answer/",
         review.views.review_update, name="review_update"),
    path("ticket/<int:id>/delete_answer/",
         review.views.delete_review, name="delete_review"),
    path("fullreview/", review.views.ticket_and_review_upload,
         name="fullreview")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
