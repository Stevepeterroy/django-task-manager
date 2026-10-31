from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Todo
from .forms import TodoForm

@login_required
def todo_list(request):
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todos/todo_list.html', {'todos': todos})

@login_required
def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo updated successfully!')
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/todo_detail.html', {'form': form, 'todo': todo})

@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Todo created successfully!')
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todos/todo_form.html', {'form': form})

@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Todo deleted successfully!')
        return redirect('todo_list')
    return render(request, 'todos/todo_confirm_delete.html', {'todo': todo})

@login_required
@require_POST
def todo_toggle_complete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('todo_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
