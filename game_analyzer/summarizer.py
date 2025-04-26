# from game import Move 
# from game import ChessGame
from .pgn_parser import PGNParser
from .visualizer import plot_time_deltas
from .analyzer import Analyzer
from groq import Groq
from django.conf import settings

# def read_pgn_file(file_path):
#     with open(file_path, 'r', encoding='utf-8') as f:
#         return f.read()


def get_objects(pgn_text):

    parser=PGNParser()
    #pgn_text = read_pgn_file('./data/sample/data.pgn')
    game=parser.parse_pgn(pgn_text)
    #print(game.moves)
    white,black=game.get_time_deltas()
    print(sum(white)+sum(black))
    plot_time_deltas(game)
    analyzer=Analyzer(r".\engine\stockfish\stockfish-windows-x86-64-avx2.exe")
    analyzer.analyze_game(game)
    blunders=analyzer.find_blunders(game)
    #print("blunders",blunders)
    best_moves=analyzer.find_best_move(game)
    #print("best_moves",best_moves)
    wdl_stats=analyzer.get_wdl_stats(game)
    #print("wdl_stats",wdl_stats)
    mistakes=analyzer.find_mistakes(game)
    #print("mistakes",mistakes)
    highlights=analyzer.find_highlights(game)
    print("highlights",highlights)
    objects={}
    objects['blunders']=blunders
    objects['best_moves']=best_moves
    objects['mistakes']=mistakes
    objects['highlights']=highlights
    objects['player_1']=game.white
    objects['player_2']=game.black
    objects['date']=game.date
    objects['result']=objects['player_1'] if game.result == '1-0' else objects['player_2']
    return objects

def generate_llm_summary(objects):

    client = Groq(api_key=settings.API_KEY)

    # Build a structured, readable prompt from the dictionary
    summary_prompt = f"""
    Summarize the following chess game in an engaging, article-style summary:
    
    - Date: {objects['date']}
    - White: {objects['player_1']}
    - Black: {objects['player_2']}
    - Result: {objects['result']} won

    Key Game Insights:
    - Blunders: {objects['blunders']}
    - Best Moves: {objects['best_moves']}
    - Mistakes: {objects['mistakes']}
    - Highlights: {objects['highlights']}

    You are a chess journalist summarizing the game. Return your summary as an HTML <div> with headings, styled paragraphs, and bullet points where appropriate.
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

#main()

