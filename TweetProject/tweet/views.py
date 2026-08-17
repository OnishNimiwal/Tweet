from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm,UserRegistrationForm,SearchTweetForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# page for the home page of the whole project
def home(request):
    return render(request, 'home.html')

# page that will render on the home page of the tweet app
def index(request):
    return render(request,'index.html')


# page that will list all the created tweets
def tweet_list(request):
    tweets=Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html',{'tweets':tweets})


# page will handle the filled and unfilled form
@login_required# protecting the function with the login decorator
def tweet_create(request):
    if request.method=="POST":# if form is filled and clicked submit
        form=TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet=form.save(commit=False)# means we are not currently saving the form in the db
            tweet.user=request.user# to add the user in the forms too which comes automatically with every req in django
            tweet.save()
            return redirect('tweet_list')
    else:# if we have to give the form
        form=TweetForm()
    return render(request,'tweet_form.html',{'form':form})

# page to edit the tweet
@login_required
def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=="POST":# when user give us the edited tweet
        form=TweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form=TweetForm(instance=tweet)# when we serve the user form to edit
    return render(request,'tweet_form.html',{'form':form})
    
# page to delete tweet
@login_required
def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=="POST":# means user send request to delete
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',{'tweet':tweet})# when request is not of delete this we show


def register(request):
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])#for cleaning the data properly see the doc.
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form=UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form})
# Create your views here.

@login_required
def tweet_search(request):
    form = SearchTweetForm(request.GET or None)
    tweets = Tweet.objects.all()

    if form.is_valid():
        text = form.cleaned_data['text']# cleaned_data is used in django to align the data w.r.t to the model and the form feilds.

        if text:
            tweets = Tweet.objects.filter(
                text__icontains=text
            )
    return render(request, 'tweet_search.html', {'form': form,'tweets': tweets})
