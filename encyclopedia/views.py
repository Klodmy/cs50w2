from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from . import util
import re
from django import forms

# request a list of entries
li = util.list_entries()

class NewEntry(forms.Form):
    e_title = forms.CharField(label='', min_length='1', max_length='100', widget=forms.TextInput(attrs={'placeholder': 'Title', 'id':'e_title'}))
    e_content = forms.CharField(label='', widget=forms.Textarea(attrs={"rows":"5", 'cols':'10', 'placeholder': 'Entry text', 'id':'e_content'}))


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
    if title in util.list_entries():
        return render(request, "encyclopedia/titles.html", {
            'title' : title,
            'entry' : entry
        })
    else:
        return HttpResponseRedirect(f'{title}')
    

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
        
        # if there is something similar in the list of entries returns it
        if possibles:
            return render(request, 'encyclopedia/search.html', {
                'entries' : possibles
            })
        
        return render(request, 'encyclopedia/search.html')
    

    

def new(request):
    # loads the page
    if request.method == 'GET':
        # create form
        form = NewEntry()

        # render the page
        return render(request, "encyclopedia/new.html",{
            'form' : form
        })
    # on form submission
    else:
        # take data from the form
        form = NewEntry(request.POST)
        # check if user provided valid data
        if form.is_valid():
            title = form.cleaned_data['e_title']
            content = form.cleaned_data['e_content']
            # try to create new fiel
            try:
                new = open(f'entries/{title}.md', 'x')
            except:
                return render(request, 'encyclopedia/error.html')
            new.write(content)
            util.list_entries()
            return HttpResponseRedirect(f'/wiki/{title}')
        return render(request, 'encyclopedia/error.html')
            
        
    

    
