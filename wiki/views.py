from django.shortcuts import redirect, render
from encyclopedia import util

def main(request):
    return render(request, 'encyclopedia/index.html',{
        "entries": util.list_entries()
    })