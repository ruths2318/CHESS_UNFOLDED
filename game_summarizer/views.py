from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.conf import settings
from groq import Groq


def index(request):
    return render(request, 'index.html')

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

    
        response_text = generate_llm_summary(pgn_text)

        return JsonResponse({'summary': response_text})
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def generate_llm_summary(pgn):
    client = Groq(api_key=settings.API_KEY)
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "you are chess summarizer, you take a pgn and summarizes it in such a way that chess journalist can copy paste your output in a article.and return the summary in html div"
            },
            {
                "role": "user",
                "content": "Summarize this pgn: " + pgn + "and return a html div"
            }
        ]
    )
    return completion.choices[0].message.content