import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qabul.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.serializers import deserialize
from django.db import transaction
from news.models import Post, Category

User = get_user_model()
main_user = User.objects.filter(is_superuser=True).first() or User.objects.first()

backup_path = 'backup.json'

if not os.path.exists(backup_path):
    print("backup.json not found!")
    exit(1)

print("Starting safe restoration...")

with open(backup_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. Restore Categories
categories_data = [x for x in data if x.get('model') == 'news.category']
for c_item in categories_data:
    fields = c_item.get('fields', {})
    cat, created = Category.objects.get_or_create(
        id=c_item.get('pk'),
        defaults={
            'name': fields.get('name'),
            'slug': fields.get('slug'),
            'description': fields.get('description', '')
        }
    )
    if not created:
        cat.name = fields.get('name')
        cat.slug = fields.get('slug')
        cat.save()

# 2. Restore Posts and assign main_user as author
posts_data = [x for x in data if x.get('model') == 'news.post']
for p_item in posts_data:
    fields = p_item.get('fields', {})
    cat_id = fields.get('category')
    category = Category.objects.filter(id=cat_id).first()
    
    post, created = Post.objects.get_or_create(
        id=p_item.get('pk'),
        defaults={
            'title': fields.get('title'),
            'slug': fields.get('slug'),
            'author': main_user,
            'category': category,
            'content': fields.get('content'),
            'excerpt': fields.get('excerpt', ''),
            'image': fields.get('image', ''),
            'status': fields.get('status', 'published'),
            'views': fields.get('views', 0),
            'is_main': fields.get('is_main', False),
            'published_date': fields.get('published_date')
        }
    )
    if not created or True:
        post.title = fields.get('title')
        post.content = fields.get('content')
        post.image = fields.get('image', '')
        post.author = main_user
        post.status = fields.get('status', 'published')
        post.save()

# 3. Restore other models safely
SKIP_MODELS = ['contenttypes.contenttype', 'auth.permission', 'sessions.session', 'admin.logentry', 'news.post', 'news.category']
restored_count = 0

for item in data:
    model_name = item.get('model')
    if model_name in SKIP_MODELS:
        continue
    try:
        item_json = json.dumps([item])
        for obj in deserialize('json', item_json, ignorenonexistent=True):
            with transaction.atomic():
                obj.save()
            restored_count += 1
    except Exception as e:
        pass

print(f"SUCCESS! News restored: {Post.objects.count()} posts with original site images. Other records restored: {restored_count}.")
