import markdown2
import random
# import secrets

from .forms import Search_Form, NewPage, EditPage, DeletePage

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.files.storage import default_storage
from .import util

# from django.views.generic import (
    
#     ListView,
#     DeleteView
# )

import encyclopedia


# Default homepage, displays list of created entries/pages
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": Search_Form()
    })

# Return the wiki entry. Url: (wiki/title). Error if doesn't exist
def entry(request, title):
    entry = util.get_entry(title)
    # If url specified is not in entry/page list, return error page
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "form": Search_Form()
        })
    # Take user to the entry for the title. Url: (wiki/title)
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2.markdown(entry),
            "entry_raw": entry,
            "form": Search_Form()
        })

# defining a search function 
def search(request):
    if request.method == "POST":
        entries_found = []  #List of entries that match query
        entries_all = util.list_entries()  #All entries
        form = Search_Form(request.POST or None)  #Gets info from form
        # Check if form fields are valid
        if form.is_valid():
            # Get the query to search entries/pages
            query = form.cleaned_data["query"]
            # Check if any entries/pages match query
            # If exists, redirect to entry/page
            for entry in entries_all:
                if query.lower() == entry.lower():
                    title = entry
                    entry = util.get_entry(title)
                    return HttpResponseRedirect(reverse("entry", args=[title]))
                # Partial matches are displayed in a list
                if query.lower() in entry.lower():
                    entries_found.append(entry)
            # Return list of partial matches
            return render(request, "encyclopedia/search.html", {
                "results": entries_found,
                "query": query,
                "form": Search_Form()
            })
    # # Default values
    # return render(request, "encyclopedia/search.html", {
    #     "results": "",
    #     "query": "",
    #     "form": Search()
    # })

def deleteEntry(request, title):
    if request.method == "POST":
        deleteTitle = util.delete_entry(title) ## delete a selected title
        msg_success = "Success"
       #return to index page with a success message after deleting the page
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": Search_Form(),
        "msg_success": msg_success,
        "title": title
    }) 
 
# def deleteEntry(request, title):
#     if request.method == "POST":
#         # Extract information from form
#         edit_entry = EditPage(request.POST or None)
#         if edit_entry.is_valid():
#             # Extract 'data' from form
#             content = edit_entry.cleaned_data["data"]
#             # Extract 'title' from form
#             title_edit = edit_entry.cleaned_data["title"]
            
#             if title_edit != title:
#                 filename = f"entries/{title}.md"
#                 if default_storage.exists(filename):
#                     default_storage.delete(filename)
#             # Delete entry
#             util.delete_entry(title_edit, content)
            
               
#         return HttpResponse(util.delete_entry)


def create(request):
    if request.method == "POST":
        new_entry = NewPage(request.POST or None) #request info from form
        if new_entry.is_valid(): # Check if input fields are valid
            
            title = new_entry.cleaned_data["title"] # Extract title of newly added entry
            data = new_entry.cleaned_data["data"] # Check if title with the same name exists
            
            entries_all = util.list_entries()
            # If entry exists, return same page with error
            for entry in entries_all:
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/create.html", {
                        "form": Search_Form(),
                        "newPageForm": NewPage(),
                        "error": "That entry already exists!"
                    }
                    )
                 
            # "# " + title = add markdown to content of entry & "\n" + data = is a new line is appended to spearate title from content
            new_added_content = "# " + title + '\n' + data
            # Save the new entry with the title
            util.save_entry(title, new_added_content)
            savedEntry = util.get_entry(title)
            msg_success = "Hurray ! Page Successfully Added!"
            # Return the page for the newly created entry
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": markdown2.markdown(savedEntry),
                "form": Search_Form(),
                "msg_success" : msg_success
            })
    # # Default Create New Page view
    return render(request, "encyclopedia/create.html", {
        "form": Search_Form(),
        "newPageForm": NewPage()
    })

# Edit an existing entry
def edit_Entry(request, title):
    if request.method == "POST":
        # Get data for the entry to be edited
        savedEntry = util.get_entry(title)
        # Display content in textarea
        edit_form = EditPage(initial={'title': title, 'data': savedEntry})
                # Return the page with forms filled with entry information
        return render(request, "encyclopedia/edit.html", {
            "form": Search_Form(),
            "editPageForm": edit_form,
            "entry": savedEntry,
            "title": title
        })

    



# Submit edited wiki page
def submit_Edit_Entry(request, title):
    if request.method == "POST":
        # Extract information from form
        edit_entry = EditPage(request.POST or None)
        if edit_entry.is_valid():
            # Extract 'data' from form
            content = edit_entry.cleaned_data["data"]
            # Extract 'title' from form
            title_edit = edit_entry.cleaned_data["title"]
            # Delete old file after editing the title
            if title_edit != title:
                filename = f"entries/{title}.md"
                if default_storage.exists(filename):
                    default_storage.delete(filename)
            # Save new entry
            util.save_entry(title_edit, content)
            # Get the new entry 
            savedEntry = util.get_entry(title_edit)
            msg_success = "Hurray ! Page Successfully updated!"
        # Return the edited entry
        return render(request, "encyclopedia/entry.html", {
            "title": title_edit,
            "entry": markdown2.markdown(savedEntry),
            "form": Search_Form(),
            "msg_success": msg_success
        })

# Random wiki entry
def randomEntry(request):
    # Get list of all entries
    entries = util.list_entries()
    # Get the title of a randomly selected entry
    random_title = random.choice(entries)
    # Get the content of the selected entry
    entry = util.get_entry(random_title)
    # Return the redirect page for the entry
    return HttpResponseRedirect(reverse("entry", args=[random_title]))




