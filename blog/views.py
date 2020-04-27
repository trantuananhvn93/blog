from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View

from .chatbot.functions import *
import pickle
from .ner.lib import *

from .models import Post

from django.urls import reverse
from django.views.generic import DateDetailView

from .forms import CommentForm

def chatbot(request):
    return render(request, 'chatbot/index.html')

def chatbotReply(request):
    if request.method == 'POST':
        save_dir = "../data/chatbot/"
        searcher = pickle.load( open( os.path.join(save_dir, "searcher.pck"), "rb" ) )
        # searcher = GreedySearchDecoder(encoder, decoder)
        voc = pickle.load( open( os.path.join(save_dir, "voc.pck"), "rb" ) )

        text  = request.POST.get('chattext')
        # Normalize sentence
        input_sentence = normalizeString(text)
        # Evaluate sentence
        state, output_words = evaluate(searcher, voc, input_sentence)
        # Format and print response sentence
        if state:
            output_words[:] = [x for x in output_words if not (x == 'EOS' or x == 'PAD')]
            response = ' '.join(output_words)
        else: 
            response = "'" + output_words + "'" + " is not found in our dictionary. Please try again!"
        context = {'query': text, 'response': response}
        return render(request, 'chatbot/index.html', context)

def ner(request):
    return render(request, 'ner/index.html')

def nerReply(request):
    if request.method == 'POST':
        text  = request.POST.get('nertext')
        doc = nlp(str(text))
        response = displacy.render(doc, jupyter=False, style='ent')
        context = {'response': response}
        return render(request, 'ner/index.html', context)


def homepage(request):
    return render(request = request,
                  template_name='posts/index.html',
                  context = {"tutorials":Post.objects.all})

class HomeView(ListView):
    model = Post
    # paginate_by = 9
    template_name = "posts/index.html"

# class PostDetailView(DetailView):
#     model = Post
#     template_name = "posts/detail.html"



def post_detail(request, post_id):
    template_name = 'posts/detail.html'
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            # reset comment form
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})