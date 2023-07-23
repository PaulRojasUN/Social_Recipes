from .models import PostSeed;

def reset_posts_seeds():
    PostSeed.objects.all().update(seed=0);

