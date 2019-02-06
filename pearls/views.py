from django.views.generic import ListView

from pearls.models import Post


class PostList(ListView):
    model = Post
    paginate_by = 30
    queryset = Post.objects.all()
    template_name = 'pearl_list.html'
