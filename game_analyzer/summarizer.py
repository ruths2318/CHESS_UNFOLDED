# from game import Move 
# from game import ChessGame
from .pgn_parser import PGNParser
from .visualizer import plot_time_deltas,plot_wdl_over_moves
from .analyzer import Analyzer
from groq import Groq
from django.conf import settings

def read_pgn_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_objects(pgn_text):

    parser=PGNParser()
    #pgn_text = read_pgn_file('data/sample/data.pgn')
    game=parser.parse_pgn(pgn_text)
    white,black=game.get_time_deltas()
    plot_time_deltas(game)
    analyzer=Analyzer(r".\engine\stockfish\stockfish-windows-x86-64-avx2.exe")
    analyzer.analyze_game(game)
    blunders=analyzer.find_blunders(game)
    best_moves=analyzer.find_best_moves(game)
    wdl_stats=analyzer.get_wdl_stats(game)
    #print(wdl_stats)
    san_moves = [move.san for move in game.moves]
    plot_wdl_over_moves(wdl_stats,san_moves)
    mistakes=analyzer.find_mistakes(game)
    highlights=analyzer.find_highlights(game)
    objects={}
    objects['blunders']=blunders
    objects['best_moves']=best_moves
    objects['mistakes']=mistakes
    objects['highlights']=highlights
    objects['player_1']=game.white
    objects['player_2']=game.black
    objects['date']=game.date
    objects['result']=game.result
    objects['link']=game.link
    return objects

def generate_llm_summary(objects):

    client = Groq(api_key=settings.API_KEY)

    summary_prompt = f"""
    
    - Date: {objects['date']}
    - White: {objects['player_1']}
    - Black: {objects['player_2']}
    - Result: {objects['result']}  .

    Key Game Insights:
    - Blunders: {objects['blunders']}
    - Best Moves: {objects['best_moves']}
    - Mistakes: {objects['mistakes']}
    - Highlights: {objects['highlights']}

    Summarize the chess game in an engaging, article-style summary. Return your summary as an HTML <div> with headings, styled paragraphs, and bullet points where ever appropriate.
    """

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are a chess journalist assistant. Your task is to convert structured game analysis into a publishable, engaging summary in HTML format."
            },
            {
                "role": "user",
                "content": summary_prompt
            }
        ]
    )

    return completion.choices[0].message.content



def get_summary(pgn_text):
    objects=get_objects(pgn_text)
    summary=generate_llm_summary(objects)
    return summary,objects



