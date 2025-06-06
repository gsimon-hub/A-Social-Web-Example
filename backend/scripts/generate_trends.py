# -*- coding: utf-8 -*-

import os
import django
import sys
from datetime import timedelta
from django.utils import timezone
from collections import Counter

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from post.models import Post, Trend

# following snippets from github Copilot
def extract_hashtags(text):
    """Extract hashtags from a given text."""
    return [word[1:] for word in text.split() if word.startswith('#')]

Trend.objects.all().delete()

last_minute = timezone.now() - timedelta(hours= 24)
oneday_posts = Post.objects.filter(created__gte = last_minute)

hashtags = Counter()
for post in oneday_posts:
    hashtags.update(extract_hashtags(post.body))

for tag, count in hashtags.most_common(10):
    Trend.objects.create(hashTag = tag, occurences = count)

    
""" 
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(
        user_id=user.id,
        verb= verb,
        created__gte=last_minute
    ) 
"""
