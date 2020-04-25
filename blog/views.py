from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View

from .chatbot.functions import *
import pickle
from .ner.lib import *

from .models import Tutorial



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
                  context = {"tutorials":Tutorial.objects.all})

class HomeView(ListView):
    model = Tutorial
    # paginate_by = 9
    template_name = "posts/index.html"

class TutorialDetailView(DetailView):
    model = Tutorial
    template_name = "posts/detail.html"