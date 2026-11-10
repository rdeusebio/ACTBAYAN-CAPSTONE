import os
import re
from flask import Flask, jsonify, request

app = Flask(__name__)

PROFANITY_FILE = 'profanitylist.txt'

# 1. Leetspeak normalization map
LEET_MAP = {
    '1': 'i',
    '!': 'i',
    '3': 'e',
    '4': 'a',
    '@': 'a',
    '5': 's',
    '$': 's',
    '0': 'o',
    '7': 't',
    '9': 'g',
    '8': 'b',
}

# 2. Interchangeable character swaps (e.g., i = e, c = k, etc.)
# This unifies variations so swapped vowels/consonants map to the same base letter.
CHAR_EQUIVALENTS = {
    'e': 'i',  # Treats 'e' and 'i' as identical (i = e, e = i)
    'c': 'k',  # Treats 'c' and 'k' as identical
    'ph': 'f',  # Optional phonetic mapping
}


def load_profanities(filepath):
  """Loads profanities from a text file, ignoring comments and empty lines."""
  profanities = set()
  if not os.path.exists(filepath):
    print(f'Warning: {filepath} not found. Creating a default file.')
    with open(filepath, 'w', encoding='utf-8') as f:
      f.write('yawa\nputangina\ngago\nukininam\n')

  with open(filepath, 'r', encoding='utf-8') as f:
    for line in f:
      line = line.strip()
      if line and not line.startswith('#'):
        profanities.add(line.lower())
  return profanities


CUSTOM_PROFANITIES = load_profanities(PROFANITY_FILE)


def normalize_text(text):
  """Cleans text, applies leetspeak, unifies interchangeable characters,

  and strips spaces/symbols.
  """
  text = text.lower()

  # Apply leetspeak translations
  for char, replacement in LEET_MAP.items():
    text = text.replace(char, replacement)

  # Apply interchangeable character swaps (like i = e)
  for char, replacement in CHAR_EQUIVALENTS.items():
    text = text.replace(char, replacement)

  # Remove all spaces, punctuation, and non-alphabetical characters
  return re.sub(r'[^a-z]', '', text)



def check_profanity(text):
  # Normalize the incoming text
  normalized_text = normalize_text(text)

  # Create a reversed version of the normalized text to catch backwards typing
  reversed_text = normalized_text[::-1]

  for bad_word in CUSTOM_PROFANITIES:
    # Also normalize the bad word using the exact same rules
    normalized_bad_word = normalize_text(bad_word)

    if not normalized_bad_word:
      continue

    # Check if the bad word is present forwards OR backwards
    if (
        normalized_bad_word in normalized_text
        or normalized_bad_word in reversed_text
    ):
      return True, bad_word

  return False, None


@app.route('/api/check-profanity', methods=['POST'])
def api_check_profanity():
  data = request.get_json()
  if not data or 'text' not in data:
    return (
        jsonify({
            'error': (
                'Invalid request. Please provide "text" in the JSON body.'
            )
        }),
        400,
    )

  original_text = data['text']
  is_profane, matched_trigger = check_profanity(original_text)

  return jsonify({
      'original_text': original_text,
      'is_profane': is_profane,
      'matched_trigger': matched_trigger if is_profane else None,
  })
  
