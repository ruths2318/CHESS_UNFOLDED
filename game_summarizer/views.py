from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.http import JsonResponse
from .models import Game

from game_analyzer import summarizer


def index(request):
    games = Game.objects.all().order_by('-date')  # Show recent first
    return render(request, 'index.html', {"games": games})
    #return render(request, 'index.html')

def summarize(request):
    if request.method == 'POST':
        pgn_text = ''
        if 'pgn_text' in request.POST and request.POST['pgn_text'].strip():
            pgn_text = request.POST['pgn_text']
        elif 'pgn_file' in request.FILES:
            pgn_file = request.FILES['pgn_file']
            pgn_text = pgn_file.read().decode('utf-8')

        if not pgn_text:
            return JsonResponse({'error': 'No PGN data provided.'}, status=400)

        
        response_text,objects =summarizer.get_summary(pgn_text)
        
        Game.objects.create(
            pgn_text=pgn_text,
            date=objects['date'],
            player_1=objects['player_1'],
            player_2=objects['player_2'],
            result=objects['result']
        )

        games = Game.objects.all()
        #print(games)

        # return the plots
        # summary    
        # game link
        return JsonResponse({'summary': response_text,
                             "image_url":'time_plot.png'})
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def analyze_existing_game(request, game_id):
    if request.method == 'GET':
        game = get_object_or_404(Game, id=game_id)
        
        response_text, objects = summarizer.get_summary(game.pgn_text)

        return JsonResponse({
            'summary': response_text,
            'image_url': 'time_plot.png'
        })