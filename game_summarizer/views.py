# Author: Ruthura ,Sravanthi
# Date: 05-02-2025
# Description : This code stores all the views for this app.

from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.http import JsonResponse
from .models import Game

from game_analyzer import summarizer


def index(request):
    """
    Renders the index page with a dropdown list of all past games stored in the database.

    Parameters:
        request (HttpRequest): The incoming request object.

    Returns:
        HttpResponse: Renders the 'index.html' template with the game list.
    """

    # Retrieve all games sorted by most recent
    games = Game.objects.all().order_by('-date') 
    return render(request, 'index.html', {"games": games})

def summarize(request):
    """
    Summarizes a newly uploaded chess game from PGN input or file.

    Parameters:
        request (HttpRequest): The POST request with PGN input.

    Returns:
        JsonResponse: Contains summary, image URLs, and video link.
    """
        
    if request.method == 'POST':
        pgn_text = ''

        # Try to read PGN from textarea
        if 'pgn_text' in request.POST and request.POST['pgn_text'].strip():
            pgn_text = request.POST['pgn_text']

        # try reading from uploaded file
        elif 'pgn_file' in request.FILES:
            pgn_file = request.FILES['pgn_file']
            pgn_text = pgn_file.read().decode('utf-8')

        if not pgn_text:
            return JsonResponse({'error': 'No PGN data provided.'}, status=400)

        # Analyze game
        response_text,objects =summarizer.get_summary(pgn_text)
        
        # Store metadata in database
        Game.objects.create(
            pgn_text=pgn_text,
            date=objects['date'],
            player_1=objects['player_1'],
            player_2=objects['player_2'],
            result=objects['result']
        )

        # Return response including summary + plot URLs
        return JsonResponse({'summary': response_text,
                             "image_url":'/static/plots/time_plot.png',
                             "wdl_url":'/static/plots/wdl_plot.png',
                             "video_url": objects['link']})
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def analyze_existing_game(request, game_id):
    """
    Re-analyzes a stored chess game from the database.

    Parameters:
        request (HttpRequest): The incoming GET request.
        game_id (int): ID of the game to analyze.

    Returns:
        JsonResponse: Summary, image URLs, and video link.
    """

    if request.method == 'GET':
        game = get_object_or_404(Game, id=game_id)
        
        response_text, objects = summarizer.get_summary(game.pgn_text)

        return JsonResponse({
            'summary': response_text,
            'image_url': '/static/plots/time_plot.png',
            "wdl_url":'/static/plots/wdl_plot.png',
            "video_url": objects['link']
        })