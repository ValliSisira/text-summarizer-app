
from transformers import pipeline

# Create the pipeline with T5-large
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    tokenizer="facebook/bart-large-cnn",
    framework="pt"
)

def generate_abstractive_summary(text):
    # Token limit safety: truncate to ~600 words max
    words = text.split()
    if len(words) > 600:
        text = ' '.join(words[:600])
    
    # Add prompt for T5
    input_text = "summarize: " + text

    # Generate summary
    summary = summarizer(
        input_text,
        max_length=250,
        min_length=80,
        do_sample=False,
        early_stopping=True,
        no_repeat_ngram_size=2
    )

    return summary[0]['summary_text']
