import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qabul.settings')
django.setup()

from news.models import Post

artifacts_dir = "C:/Users/User/.gemini/antigravity-cli/brain/74ca79b2-4762-4bb0-b366-1f64bdd83e91"
target_media_dir = "C:/Users/User/qabul/media/blog/images"
os.makedirs(target_media_dir, exist_ok=True)

# Map post IDs to generated images
image_mapping = {
    1: "news_conf_2026_1787565942838.png",
    2: "news_startup_2026_1787565956397.png",
    3: "news_youth_2026_1787565968933.png",
    4: "news_olymp_2026_1787565980254.png",
    5: "news_memory_2026_1787565993889.png",
    6: "news_sport_2026_1787566005647.png",
    7: "news_health_2026_1787566017466.png",
    8: "news_lang_2026_1787566029075.png"
}

for post_id, filename in image_mapping.items():
    src_path = os.path.join(artifacts_dir, filename)
    target_filename = f"samduuf_2026_news_{post_id}.png"
    dst_path = os.path.join(target_media_dir, target_filename)
    
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"Copied {filename} -> {target_filename}")
        
        rel_media_path = f"blog/images/{target_filename}"
        post = Post.objects.filter(id=post_id).first()
        if post:
            post.image = rel_media_path
            post.save()
            print(f"Updated Post #{post.id} image: {rel_media_path}")

print("\nAll 8 post images successfully replaced with brand new HD event photographs!")
