# game_summarizer/tests/test_views.py

import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from game_summarizer.models import Game

@pytest.mark.django_db
def test_index_view(client):
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert "text/html" in response["Content-Type"]

@pytest.mark.django_db
def test_summarize_post_text(client, mocker):
    mock_summary = ("Mock summary", {
        "date": "2024-01-01",
        "player_1": "WhitePlayer",
        "player_2": "BlackPlayer",
        "result": "1-0"
    })
    mocker.patch("game_summarizer.views.summarizer.get_summary", return_value=mock_summary)

    response = client.post(reverse("summarize"), {"pgn_text": "1. e4 e5 2. Nf3 Nc6"})
    assert response.status_code == 200
    assert "summary" in response.json()

@pytest.mark.django_db
def test_summarize_post_file(client, mocker):
    mock_summary = ("Mock summary from file", {
        "date": "2024-01-01",
        "player_1": "WhitePlayer",
        "player_2": "BlackPlayer",
        "result": "1-0"
    })
    mocker.patch("game_summarizer.views.summarizer.get_summary", return_value=mock_summary)

    file_data = SimpleUploadedFile("game.pgn", b"1. e4 e5 2. Nf3 Nc6")
    response = client.post(reverse("summarize"), {"pgn_file": file_data})
    assert response.status_code == 200
    assert response.json()["summary"] == "Mock summary from file"

@pytest.mark.django_db
def test_analyze_existing_game(client, mocker):
    mock_summary = ("Existing game summary", {
        "date": "2024-01-01",
        "player_1": "White",
        "player_2": "Black",
        "result": "1-0"
    })
    mocker.patch("game_summarizer.views.summarizer.get_summary", return_value=mock_summary)

    game = Game.objects.create(
        pgn_text="1. e4 e5",
        date="2024-01-01",
        player_1="White",
        player_2="Black",
        result="1-0"
    )

    response = client.get(reverse("analyze_existing_game", args=[game.id]))
    assert response.status_code == 200
    assert "summary" in response.json()
