import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qabul.settings')
django.setup()

from news.models import Post

# Set official institution logo / image for all news posts
for post in Post.objects.all():
    post.image = "Logo.png"
    post.save()
    print(f"Post #{post.id} ({post.title[:40]}...) image set to Logo.png")

print("All 8 official 2026 news posts updated to use official Logo.png!")
