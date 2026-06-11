import os
from flask import Flask, render_template, request, jsonify
import language_tool_python

app = Flask(__name__)

java_home = r"C:\Program Files\Eclipse Adoptium\jdk-17.0.19.10-hotspot"
if os.path.exists(java_home):
    os.environ["JAVA_HOME"] = java_home
    os.environ["PATH"] = java_home + r"\bin;" + os.environ.get("PATH", "")

from difflib import SequenceMatcher
from itertools import combinations, permutations

tool = language_tool_python.LanguageTool('en-US')

def apply_replacements(text, matches):
    result = []
    last = 0
    for match in sorted(matches, key=lambda item: item.offset):
        if not match.replacements:
            continue
        start = match.offset
        end = start + match.error_length
        if start < last:
            continue
        result.append(text[last:start])
        result.append(match.replacements[0])
        last = end
    result.append(text[last:])
    return ''.join(result)


def score_candidate(tool, original, candidate):
    issues = len(tool.check(candidate))
    distance = 1 - SequenceMatcher(None, original, candidate).ratio()
    return (issues, distance)


def try_unscramble(tool, text, max_words=7):
    words = text.strip().split()
    if len(words) <= 1 or len(words) > max_words:
        return None

    original = " ".join(words)
    best_candidate = original
    best_score = score_candidate(tool, original, original)
    seen = set()

    for perm in permutations(words):
        if perm in seen:
            continue
        seen.add(perm)
        candidate = " ".join(perm).capitalize()
        score = score_candidate(tool, original, candidate)
        if score < best_score:
            best_candidate = candidate
            best_score = score
            if score[0] == 0:
                break

    return best_candidate if best_candidate != original else None


def best_rewrite(tool, text):
    matches = tool.check(text)
    candidates = {text}

    if matches:
        candidates.add(tool.correct(text))
        candidates.add(apply_replacements(text, matches))

        if len(matches) <= 5:
            for r in range(1, len(matches)):
                for subset in combinations(matches, r):
                    candidates.add(apply_replacements(text, subset))
        else:
            for i in range(len(matches)):
                subset = [m for j, m in enumerate(matches) if j != i]
                candidates.add(apply_replacements(text, subset))

    unscrambled = try_unscramble(tool, text)
    if unscrambled:
        candidates.add(unscrambled)

    return min(candidates, key=lambda cand: score_candidate(tool, text, cand))


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/editor')
def editor():
    return render_template('editor.html')

@app.route('/check', methods=['POST'])
def check():
    text = request.json['text']
    corrected = best_rewrite(tool, text)

    return jsonify({
        "result": corrected
    })

if __name__ == "__main__":
    app.run(debug=True)