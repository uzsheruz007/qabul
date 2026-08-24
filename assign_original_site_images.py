import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qabul.settings')
django.setup()

from news.models import Post

original_images = {
    1: "blog/images/blog-1.png",
    2: "blog/images/blog-2.png",
    3: "blog/images/blog-4.png",
    4: "blog/images/carousel-2.png",
    5: "blog/images/contact-img.png",
    6: "blog/images/instagram-footer-1.jpg",
    7: "blog/images/instagram-footer-2.jpg",
    8: "blog/images/blog-2_1doTLCU.png"
}

for post_id, img_path in original_images.items():
    post = Post.objects.filter(id=post_id).first()
    if post:
        post.image = img_path
        post.save()
        print(f"Post #{post.id} updated to original site image: {img_path}")

print("All 8 posts updated to original site images!")
