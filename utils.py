from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def evaluate_answer(answer, keywords, ideal_answer=None):
    feedback = []

    if len(answer.strip()) == 0:
        return 0, ["Answer cannot be empty."]

    answer = answer.lower()
    answer_words = answer.split()
    keywords = [k.lower() for k in keywords]

    word_count = len(answer_words)

    # 🔥 FLEXIBLE KEYWORD MATCH
    matched = 0
    for keyword in keywords:
        if keyword in answer:
            matched += 1
        else:
            # partial match
            if any(word in keyword for word in answer_words):
                matched += 0.5

    keyword_score = (matched / len(keywords)) * 5 if keywords else 0

    # 🔥 TF-IDF SIMILARITY
    similarity = 0
    similarity_score = 0

    if ideal_answer:
        vectorizer = TfidfVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform([ideal_answer.lower(), answer])
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
        similarity_score = similarity * 3

    # 🔥 CONCEPT BOOST (NEW)
    concept_words = [
    "model", "data", "training", "testing",
    "generalization", "overfit", "memorize", "noise"
]
    concept_hits = sum(1 for word in concept_words if word in answer)
    concept_score = min(concept_hits * 0.4, 2)

    # 🔥 LENGTH BONUS
    length_bonus = 0
    if word_count > 30:
        length_bonus = 1
    elif word_count > 20:
        length_bonus = 0.5

    # FINAL SCORE
    final_score = keyword_score + similarity_score + concept_score + length_bonus
    final_score = min(final_score, 10)

    # FEEDBACK
    if word_count < 20:
        feedback.append("Answer is too short. Add more explanation.")

    if matched < len(keywords) / 2:
        feedback.append("Try to include more key concepts.")

    if similarity < 0.3:
        feedback.append("Your answer lacks clarity. Improve explanation.")
    elif similarity < 0.6:
        feedback.append("Good answer but can be improved.")
    else:
        feedback.append("Excellent answer with strong understanding.")

    return round(final_score, 2), feedback