from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from .models import Post, Comment
from django.contrib.auth.forms import AuthenticationForm  # will be used for login authenticate
from .forms import CommentForm
from django.contrib import messages
from .forms import RegisterForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def home(request):
    featured_posts = Post.objects.filter(featured=True)[:8]
    recent_posts = Post.objects.order_by('-created_at')
    popular_posts = Post.objects.order_by('-views')[:5]

    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        #'popular_posts': popular_posts,
    }

    return render(request, 'blog/home.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = CommentForm()

    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

            # Return JSON for AJAX
            return JsonResponse({
                'status': 'success',
                'username': request.user.username,
                'content': comment.content,
            })
        else:
            return JsonResponse({'status': 'error'}, status=400)

    # GET request → normal rendering
    comments = post.comment_set.all().order_by('created_at')  # newest last
    return render(request, 'blog/postdetails.html', {
        'post': post,
        'comments': comments,
        'form': form
    })
    
def about(request):
    popular_posts = Post.objects.order_by('-views')[:5]
    return render(request, 'blog/about.html', {'popular_posts': popular_posts})

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    return JsonResponse({'total_likes': post.likes.count()})

def search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )

    return render(request, 'blog/search_results.html', {
        'query': query,
        'results': results
    })
    
    
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


