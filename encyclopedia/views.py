from django.shortcuts import render, HttpResponse, redirect
from . import util
import re

# request a list of entries
li = util.list_entries()


# main page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# entries
def titles(request, title):

    # getting entry data by title
    entry = util.get_entry(title)

    # check if given title is in that list and if yes render appropriate html
    if title in li:
        return render(request, "encyclopedia/titles.html", {
            'title' : title,
            'entry' : entry
        })
    else:
        return HttpResponse("A chy tudy ty zayshov, pivnyk?")

def search(request):
    if request.method == 'POST':
        # get users iput
        query = request.POST.get('q')

        # find out if it 100% matches and if does redirect to appropriate page
        for e in util.list_entries():
            if e.lower() == query.lower():
                return redirect(f'/wiki/{e}')  
                           
        # create list for matching entries
        possibles = []
        # use regular expressions to match prompt with enries
        for e in util.list_entries():
            if re.search(query.lower(), e.lower()):
                possibles.append(e)
        
        if possibles:
            return render(request, 'encyclopedia/search.html', {
                'entries' : possibles
            })
        
        return render(request, 'encyclopedia/search.html')