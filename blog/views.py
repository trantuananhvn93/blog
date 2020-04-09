from django.shortcuts import render
from django.http import HttpResponse

from .chatbot.functions import *
import pickle

save_dir = "../data/chatbot/"
searcher = pickle.load( open( os.path.join(save_dir, "searcher.pck"), "rb" ) )
# searcher = GreedySearchDecoder(encoder, decoder)
voc = pickle.load( open( os.path.join(save_dir, "voc.pck"), "rb" ) )

def chatbot(request):
    return render(request, 'chatbot.html')

def chatbotReply(request):
    if request.method == 'POST':
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
        return render(request, 'chatbot.html', context)