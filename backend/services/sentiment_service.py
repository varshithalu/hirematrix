from transformers import pipeline

# Load once at startup
sentiment_pipeline = pipeline(
    "sentiment-analysis",  # type: ignore[arg-type]
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_sentiment(text: str):
    result = sentiment_pipeline(text)[0]

    return {
        "label": result["label"],
        "confidence": float(result["score"])
    }