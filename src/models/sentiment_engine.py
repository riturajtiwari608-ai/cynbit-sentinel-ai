"""
Aspect-Based Sentiment Analysis (ABSA) Engine
Engineered for fine-grained sentiment extraction and aspect-level attribution.
"""

import re
from typing import Dict, List, Any
from src.config import ASPECT_TAXONOMY, HINGLISH_LEXICON


class AspectSentimentEngine:
    """
    Analyzes review text to extract overarching sentiment polarity,
    granularity across specific business aspects, and confidence metrics.
    """

    def __init__(self):
        self.aspects = ASPECT_TAXONOMY
        self.hinglish = HINGLISH_LEXICON
        self._init_lexicons()

    def _init_lexicons(self):
        # Positive sentiment seed words
        self.positive_seeds = {
            "good", "great", "excellent", "wonderful", "amazing", "spotless", "delicious",
            "exceptional", "top", "love", "loved", "friendly", "helpful", "clean", "prompt",
            "best", "perfect", "seamless", "solid", "pleased", "fantastic", "breathtaking",
            "charming", "patiently", "clear", "fresh", "discounts", "value", "faster"
        }

        # Negative sentiment seed words
        self.negative_seeds = {
            "bad", "worst", "terrible", "horrible", "awful", "arrogant", "rude", "missed",
            "poor", "slow", "delay", "pain", "broken", "dirty", "unacceptable", "failing",
            "outage", "refused", "fraud", "scam", "leak", "leaking", "stolen", "useless",
            "negligence", "dropped", "severe", "crowded", "forgot", "expensive"
        }

        # Negators and Intensifiers
        self.negators = {"not", "never", "no", "didn't", "didnt", "don't", "dont", "hardly", "barely", "neither", "nor", "without"}
        self.intensifiers = {
            "very": 1.4,
            "extremely": 1.8,
            "completely": 1.6,
            "severely": 2.0,
            "absolutely": 1.7,
            "highly": 1.4,
            "too": 1.3,
            "super": 1.4,
            "really": 1.3
        }

    def _clean_text(self, text: str) -> str:
        text = text.lower()
        # Keep punctuation marks that segment clauses
        text = re.sub(r'[^a-z0-9\s.,!?\'\-/]', '', text)
        return text

    def compute_sentence_sentiment(self, sentence: str) -> float:
        """
        Calculates polarity for a sentence considering negations and intensifiers.
        Returns float between -1.0 and 1.0.
        """
        sentence_lower = sentence.lower()

        # Check Hinglish phrases first
        hinglish_scores = []
        for phrase, score in self.hinglish.items():
            if phrase in sentence_lower:
                hinglish_scores.append(score)

        if hinglish_scores:
            # If negative Hinglish phrases exist, prioritize the negative grievance
            if any(s < 0 for s in hinglish_scores):
                return round(min(hinglish_scores), 3)
            return round(sum(hinglish_scores) / len(hinglish_scores), 3)

        words = re.findall(r"\b\w+(?:'\w+)?\b", sentence_lower)
        if not words:
            return 0.0

        score = 0.0
        word_count = 0
        window = 3

        for i, word in enumerate(words):
            val = 0.0
            if word in self.positive_seeds:
                val = 1.0
            elif word in self.negative_seeds:
                val = -1.0

            if val != 0.0:
                # Check for negations in preceding window
                start_idx = max(0, i - window)
                preceding = words[start_idx:i]

                has_negator = any(neg in preceding for neg in self.negators)
                multiplier = 1.0

                # Check for intensifiers
                for w in preceding:
                    if w in self.intensifiers:
                        multiplier *= self.intensifiers[w]

                if has_negator:
                    val = -val * 0.85

                val *= multiplier
                score += val
                word_count += 1

        if word_count == 0:
            return 0.0

        # Normalize score into [-1.0, 1.0]
        normalized = max(-1.0, min(1.0, score / max(1, word_count * 0.9)))
        return round(normalized, 3)

    def extract_aspect_sentiments(self, text: str) -> Dict[str, Dict[str, Any]]:
        """
        Maps sentences/clauses to business aspects and determines aspect-level sentiment.
        """
        clauses = re.split(r'[.,;!?\n]+', text)
        aspect_results: Dict[str, Dict[str, Any]] = {}

        for aspect_name, keywords in self.aspects.items():
            matching_scores = []
            matching_snippets = []

            for clause in clauses:
                clause_clean = clause.strip()
                if not clause_clean:
                    continue

                clause_lower = clause_clean.lower()
                if any(re.search(rf"\b{re.escape(kw)}\b", clause_lower) for kw in keywords):
                    s_score = self.compute_sentence_sentiment(clause_clean)
                    matching_scores.append(s_score)
                    matching_snippets.append(clause_clean)

            if matching_scores:
                avg_score = sum(matching_scores) / len(matching_scores)
                if avg_score > 0.15:
                    sentiment_label = "Positive"
                elif avg_score < -0.15:
                    sentiment_label = "Negative"
                else:
                    sentiment_label = "Neutral"

                aspect_results[aspect_name] = {
                    "sentiment": sentiment_label,
                    "score": round(avg_score, 3),
                    "confidence": round(min(0.98, 0.70 + (len(matching_scores) * 0.08)), 2),
                    "snippets": matching_snippets[:3]
                }

        return aspect_results

    def analyze(self, text: str, rating: int = None) -> Dict[str, Any]:
        """
        Performs holistic ABSA analysis on a single review text.
        """
        cleaned = self._clean_text(text)
        overall_score = self.compute_sentence_sentiment(cleaned)
        aspect_sentiments = self.extract_aspect_sentiments(text)

        # Incorporate star rating if provided as Bayesian prior
        if rating is not None:
            # Map rating (1 to 5) to score (-1.0 to 1.0)
            rating_score = (rating - 3.0) / 2.0
            overall_score = round((overall_score * 0.7) + (rating_score * 0.3), 3)

        if overall_score > 0.15:
            sentiment_label = "Positive"
        elif overall_score < -0.15:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        # Calculate model confidence
        num_aspects_found = len(aspect_sentiments)
        confidence = round(min(0.99, 0.75 + (num_aspects_found * 0.05) + (abs(overall_score) * 0.15)), 2)

        return {
            "overall_sentiment": sentiment_label,
            "polarity_score": overall_score,
            "confidence": confidence,
            "aspect_breakdown": aspect_sentiments,
            "word_count": len(text.split()),
            "detected_aspects_count": num_aspects_found
        }
