import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qabul.settings')
django.setup()

from django.core.serializers import deserialize
from django.db import transaction

backup_path = 'backup.json'

if not os.path.exists(backup_path):
    print("backup.json file not found!")
    exit(1)

print("Restoring data safely from backup.json...")

with open(backup_path, 'r', encoding='utf-8') as f:
    objects = json.load(f)

# Models to skip during restore to avoid ID conflicts with server state
SKIP_MODELS = ['contenttypes.contenttype', 'auth.permission', 'sessions.session', 'admin.logentry']

restored_count = 0
skipped_count = 0

for item in objects:
    model_name = item.get('model')
    if model_name in SKIP_MODELS:
        skipped_count += 1
        continue
    
    try:
        # Convert item to json string for deserializer
        item_json = json.dumps([item])
        for obj in deserialize('json', item_json, ignorenonexistent=True):
            with transaction.atomic():
                obj.save()
            restored_count += 1
    except Exception as e:
        print(f"Skipped item {model_name} pk={item.get('pk')}: {e}")
        skipped_count += 1

print(f"\nSUCCESS! Restored {restored_count} records. Skipped {skipped_count} conflicting records.")
