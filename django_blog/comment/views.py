from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from common.signals import comment_save_signal

from .forms import CommentForm
from .models import Comment


class CommentShowMixin:
    def get_comments(self):
        target = self.object.slug
        comments = Comment.objects.filter(target=target).all()
        return comments

    def get_context_data(self, **kwargs):
        kwargs.update(
            {"comment_form": CommentForm, "comment_list": self.get_comments()}
        )
        return super().get_context_data(**kwargs)


class CommentView(TemplateView):
    template_name = "comment/result.html"

    def post(self, request, *args, **kwargs):
        target = self.request.POST.get("target")
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment_form.save(commit=False)
            comment_form.target = target
            comment_form.save()

            comment_save_signal.send(
                sender=self.__class__,
                nickname=request.POST.get("nickname"),
                content=request.POST.get("content"),
                email=settings.EMAIL_HOST_USER,
                link=f"https://blog.jasonqiao36.cc/{target}",
            )
            return redirect(reverse("post_detail", args=(target,)))
        else:
            context = {"form": comment_form, "target": target}
            return self.render_to_response(context)
