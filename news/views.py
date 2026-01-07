from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Post, Category

def index(request):
    featured_posts = Post.objects.filter(
        status='published'
    ).order_by('-published_date')[:6]   # 🔥 OXIRGI 4 TA

    context = {
        'featured_posts': featured_posts
    }
    return render(request, 'index.html', context)



class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 8
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='published')
        
        # Kategoriya bo'yicha filtr
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        
        # Qidiruv bo'yicha filtr
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(excerpt__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['recent_posts'] = Post.objects.filter(status='published')[:5]
        context['featured_posts'] = Post.objects.filter(status='published', is_main=True)[:3]
        return context

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Ko'rishlar sonini oshirish
    post.increase_views()
    
    # Kommentariyalar
    
    # Yangi kommentariya qo'shish=
    
    # O'xshash postlar
    similar_posts = Post.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'similar_posts': similar_posts,
        'categories': Category.objects.all(),
        'recent_posts': Post.objects.filter(status='published').exclude(id=post.id)[:5],
    }
    
    return render(request, 'post_detail.html', context)

def get_featured_posts(request):
    """Asosiy sahifa uchun featured postlarni olish"""
    featured_posts = Post.objects.filter(status='published', is_main=True)[:8]
    return featured_posts