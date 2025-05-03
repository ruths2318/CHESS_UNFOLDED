# Author: Ruthura ,Sravanthi
# Date: 05-02-2025
# Description : This code summarizes the chess game by finding mistakes,game highlights,blunders,turning points,best moves,etc
# and generates text summary from llm.


from .pgn_parser import PGNParser
from .visualizer import plot_time_deltas,plot_wdl_over_moves
from .analyzer import Analyzer
from groq import Groq
from django.conf import settings

def read_pgn_file(file_path):
    """
    Reads a PGN file and returns its content as a string.

    Args:
        file_path (str): Path to the PGN file.

    Returns:
        str: Contents of the PGN file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def get_objects(pgn_text):
    """
    Parses and analyzes the PGN text to extract key insights like blunders,
    mistakes, best moves, WDL stats, and highlights.

    Args:
        pgn_text (str): PGN formatted game string.

    Returns:
        dict: Dictionary containing extracted game information and analysis.
    """

    # Parse the PGN text
    parser=PGNParser()
    game=parser.parse_pgn(pgn_text)

    # Generate time usage plot
    plot_time_deltas(game)

    #  Initialize Stockfish analyzer
    analyzer=Analyzer(r".\engine\stockfish\stockfish-windows-x86-64-avx2.exe")
    analyzer.analyze_game(game)

    # Run all analysis methods
    blunders=analyzer.find_blunders(game)
    best_moves=analyzer.find_best_moves(game)
    wdl_stats=analyzer.get_wdl_stats(game)
    san_moves = [move.san for move in game.moves]
    plot_wdl_over_moves(wdl_stats,san_moves)
    mistakes=analyzer.find_mistakes(game)
    highlights=analyzer.find_highlights(game)

    # add all extracted data into a dictionary
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
    """
    Uses a large language model to generate an HTML summary of the chess game.

    Args:
        objects (dict): The dictionary of game insights.

    Returns:
        str: HTML content summarizing the chess game.
    """

    client = Groq(api_key=settings.API_KEY)

    # Build the LLM prompt from extracted objects
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

    # Generate summary using LLaMA-3 model via Groq API
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
    """
    Generates a summary and collects structured analysis for a given PGN game.

    Args:
        pgn_text (str): PGN formatted game string.

    Returns:
        tuple: (summary in HTML, game analysis dictionary)
    """

    objects=get_objects(pgn_text)
    summary=generate_llm_summary(objects)
    return summary,objects



