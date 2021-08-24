from django import forms



#"form":Search() must be in every render request or searchbar wont show.
# Create a searchbar on side to perform searches
class Search_Form(forms.Form):
    query = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder': 'Search Me', 
            'style': 'width:100%'}))


# Form used to create a new entry
class NewPage(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
            'placeholder': 'Enter title', 'id': 'new-entry-title'}))
    data = forms.CharField(label="", widget=forms.Textarea(attrs={
        'id': 'new-entry', "placeholder": "Fill This Out Using MARKDOWN! Check Out https://www.markdownguide.org/ for help",'style':'width:100%'}))


# Form used to edit an existing entry
class EditPage(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        'id': 'edit-entry-title'}))
    data = forms.CharField(label="", widget=forms.Textarea(attrs={
        'id': 'edit-entry'}))


class DeletePage(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        'id': 'delete-entry-title'}))
    data = forms.CharField(label="", widget=forms.Textarea(attrs={
        'id': 'delete-entry'}))
