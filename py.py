import re

def clean_text(text):
    return re.sub(r'[^a-zA-Z \n]', '', text).lower()

def split_syllables(word):
    vowels = "aeiou"
    syllables = []
    current = ""
    i = 0
    while i < len(word):
        ch = word[i]
        current += ch
        if ch in vowels:
            if i + 1 < len(word):
                next_ch = word[i + 1]
                if (ch == 'a' and next_ch in 'aiu') or \
                   (ch == 'e' and next_ch == 'e') or \
                   (ch == 'o' and next_ch == 'o'):
                    current += next_ch
                    i += 1
            j = i + 1
            consonants_ahead = ""
            while j < len(word) and word[j] not in vowels:
                consonants_ahead += word[j]
                j += 1
            if len(consonants_ahead) == 0:
                syllables.append(current)
                current = ""
            elif len(consonants_ahead) == 1:
                if j >= len(word):
                    current += consonants_ahead
                    syllables.append(current)
                    current = ""
                    i = j
                else:
                    syllables.append(current)
                    current = ""
            else:
                if j >= len(word):
                    current += consonants_ahead
                    syllables.append(current)
                    current = ""
                    i = j
                else:
                    current += consonants_ahead[0]
                    syllables.append(current)
                    current = ""
                    i += 1 
        i += 1
    if current:
        if syllables: syllables[-1] += current
        else: syllables.append(current)
    return syllables

def is_guru(syllable):
    long_vowels = ['aa', 'ee', 'oo', 'ai', 'au']
    for lv in long_vowels:
        if lv in syllable: return True
    # Ends in consonant (closed syllable)
    if syllable and syllable[-1] not in 'aeiou': return True
    return False

def get_pattern(syllables):
    return ["G" if is_guru(s) else "L" for s in syllables]

def identify_meter(pattern):
    p_str = "".join(pattern)
    length = len(p_str)

    # 1. Anushtubh: 8 syllables, focus on 5th(L) and 6th(G)
    if length == 8:
        if p_str[4] == "L" and p_str[5] == "G":
            return "Anushtubh"
    
    # 2. Indravajra: 11 syllables, starts with Ta-gana (G G L)
    if length == 11:
        if p_str.startswith("GGL"):
            return "Indravajra"
        
    # 3. Upendravajra: 11 syllables, starts with Ja-gana (L G L)
    if length == 11:
        if p_str.startswith("LGL"):
            return "Upendravajra"

    return "Unknown"

# MAIN
print("Enter verse (transliterated Sanskrit):")
lines = []
while True:
    line = input()
    if not line.strip(): break
    lines.append(line)

text = clean_text("\n".join(lines))
verse_lines = [l.strip() for l in text.split("\n") if l.strip()]

print("\n--- Meter Analysis ---")
for i, line in enumerate(verse_lines):
    words = line.split()
    flat_syllables = []
    for w in words:
        flat_syllables.extend(split_syllables(w))
    
    pattern = get_pattern(flat_syllables)
    meter = identify_meter(pattern)
    
    print(f"Line {i+1}: {'-'.join(flat_syllables)}")
    print(f"Pattern: {' '.join(pattern)}")
    print(f"Detected: {meter}")
    print("-" * 20)
