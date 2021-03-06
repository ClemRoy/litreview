from itertools import chain
from re import T
from django.db.models import CharField, Value
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from . import forms
from review.models import Ticket
from review.forms import ReviewForm, TicketForm, addFollowForm
from django.contrib.auth.models import User
from authentication import models as auth_models
from review import models as review_models
# Create your views here.


@login_required
def home(request):
    followers = request.user.followers.all()
    user_tickets_raw = review_models.Ticket.objects.filter(user=request.user)
    user_tickets = user_tickets_raw.annotate(content_type=Value('ticket', CharField()))
    user_reviews_raw = review_models.Review.objects.filter(user=request.user)
    user_reviews = user_reviews_raw.annotate(content_type=Value('review', CharField()))
    feed = chain(user_tickets,user_reviews)
    for ticket in user_tickets:
        answers_raw = review_models.Review.objects.filter(ticket=ticket)
        answers = answers_raw.annotate(content_type=Value('review', CharField()))
        feed = chain(feed,answers)
    for follower in followers:
        followers_tickets_raw = review_models.Ticket.objects.filter(user=follower)
        followers_tickets = followers_tickets_raw.annotate(content_type=Value('ticket', CharField()))
        for ticket in followers_tickets:
            followers_answered_raw = review_models.Review.objects.filter(ticket=ticket)
            followers_answered = followers_answered_raw.annotate(content_type=Value('review', CharField()))
            feed = chain(feed,followers_answered)
        followers_reviews_raw = review_models.Review.objects.filter(user=follower)
        followers_reviews = followers_reviews_raw.annotate(content_type=Value('review', CharField()))
        feed= chain(feed,followers_reviews,followers_tickets)
    feed_ready = sorted(feed,key=lambda post: post.time_created,reverse=True)
    return render(request, "review/home.html", context={"feed_ready": feed_ready})


@login_required
def your_post(request):
    tickets_raw = review_models.Ticket.objects.filter(user=request.user)
    tickets = tickets_raw.annotate(content_type=Value('ticket', CharField()))
    reviews_raw = review_models.Review.objects.filter(user=request.user)
    reviews = reviews_raw.annotate(content_type=Value('review', CharField()))
    posts = sorted(chain(tickets, reviews),
                   key=lambda post: post.time_created, reverse=True)

    return render(request, "review/yourpost.html", context={"posts": posts})


@login_required
def follows(request):
    user_follows = request.user.followers.all()
    following_users = review_models.UserFollows.objects.filter(
        followed_user=request.user)
    form = forms.addFollowForm()
    message = ""
    if request.method == "POST":
        form = forms.addFollowForm(request.POST)
        if form.is_valid():
            user_to_add = form.cleaned_data["followed_user_name"]
            if auth_models.CustomUser.objects.filter(username=user_to_add).exists():
                current_user = request.user
                if current_user.username != user_to_add:
                    user_to_follow = auth_models.CustomUser.objects.get(
                        username=user_to_add)
                    try:
                        follow = review_models.UserFollows()
                        follow.user = request.user
                        follow.followed_user = user_to_follow
                        follow.save()
                        message = f"Vous suivez d??sormais {user_to_follow}"
                    except IntegrityError:
                        message = f"vous suivez d??j?? {user_to_add}"
                else:
                    message = "Vous ne pouvez pas vous suivre vous m??me"
            else:
                message = "L'utilisateur n'existe pas"

    return render(request, "review/follows.html", context={"form": form, "message": message, "user_follows": user_follows, "following_users": following_users})


@login_required
def ticket(request):
    form = forms.TicketForm()
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("home")
    return render(request, "review/ticket.html", context={"form": form})


@login_required
def ticket_and_review_upload(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if any([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.review_count = 1
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("home")
    context = {"ticket_form": ticket_form,
               "review_form": review_form,
               }
    return render(request, "review/fullreview.html", context=context)


@login_required
def ticket_update(request, id):
    ticket = review_models.Ticket.objects.get(id=id)
    if ticket.user == request.user:
        if request.method == 'POST':
            form = TicketForm(request.POST, request.FILES, instance=ticket)
            if form.is_valid():
                form.save()
                return redirect("home")
        else:
            form = TicketForm(instance=ticket)
        return render(request, "review/ticket_update.html", {"form": form})
    else:
        message = "Vous ne pouvez pas modifier un ticket cr??e par un autre utilisateur"
        return render(request, "review/ticket_update.html", {"message": message})

@login_required
def review_update(request, id):
    review = review_models.Review.objects.get(id=id)
    if review.user == request.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("home")
        else:
            form = ReviewForm(instance=review)
        return render(request, "review/review_update.html", {"form": form})
    else:
        message = "Vous ne pouvez pas modifier une critique cr??e par un autre utilisateur"
        return render(request, "review/review_update.html", {"message": message})


@login_required
def delete_ticket(request, id):
    ticket_to_delete = review_models.Ticket.objects.get(id=id)
    if ticket_to_delete.user == request.user:
        if request.method == "POST":
            ticket_to_delete.delete()
            return redirect("home")
        return render(request, "review/delete_ticket.html", {"ticket": ticket_to_delete})
    else:
        message = "Vous ne pouvez pas supprimer un ticket cr??e par un autre utilisateur"
        return render(request, "review/ticket_update.html", {"message": message})

@login_required
def delete_review(request, id):
    review_to_delete = review_models.Review.objects.get(id=id)
    if review_to_delete.user == request.user:
        if request.method == "POST":
            review_to_delete.delete()
            return redirect("home")
        return render(request, "review/review_delete.html", {"review": review_to_delete})
    else:
        message = "Vous ne pouvez pas supprimer un ticket cr??e par un autre utilisateur"
        return render(request, "review/review_delete.html", {"message": message})


@login_required
def delete_follower(request, key_id):
    user_to_unfollow = auth_models.CustomUser.objects.get(id=key_id)
    follow_relation = review_models.UserFollows.objects.filter(
        user=request.user, followed_user=user_to_unfollow)
    if request.method == "POST":
        follow_relation.delete()
        return redirect("follows")
    return render(request, "review/delete_follower.html", {"followed_user": user_to_unfollow})


@login_required
def answer_ticket(request, id):
    form = forms.ReviewForm()
    ticket = review_models.Ticket.objects.get(id=id)
    if ticket.review_count != 0:
        message = "Ce ticket a d??j?? une critique,vous ne pouvez en cr??er une nouvelle"
        return render(request, "review/create_review.html", {"message": message})
    else:
        if request.method == "POST":
            form = forms.ReviewForm(request.POST)
            if form.is_valid():
                ticket.review_count = 1
                review = form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                ticket.save()
                review.save()
                return redirect("home")
    return render(request, "review/create_review.html", {"form": form, "ticket": ticket})
