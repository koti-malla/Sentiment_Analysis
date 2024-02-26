from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from transformers import AutoTokenizer, BertForSequenceClassification, RobertaForSequenceClassification

app = Flask(__name__)
Bootstrap(app)  # Initialize Bootstrap

# Load BERT model and tokenizer
bert_model_path = "Sentiment_analysis_Bert/checkpoint-2232"
bert_model = BertForSequenceClassification.from_pretrained(bert_model_path)
bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Load RoBERTa model and tokenizer
roberta_model_path = "sentiment_model_roberta_model/checkpoint-1488"
roberta_model = RobertaForSequenceClassification.from_pretrained(roberta_model_path)
roberta_tokenizer = AutoTokenizer.from_pretrained("roberta-base")

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define the route for processing user input
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get user input from the form
        sentence = request.form['sentence']
        selected_model = request.form['model']  # Get the selected model from the form

        # Tokenize and predict using the selected model
        if selected_model == 'BERT':
            tokenizer = bert_tokenizer
            model = bert_model
        elif selected_model == 'RoBERTa':
            tokenizer = roberta_tokenizer
            model = roberta_model

        inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        prediction = outputs.logits.argmax(dim=1).item()

        # Map the predicted label to sentiment
        sentiments = ['Negative', 'Neutral', 'Positive']
        predicted_sentiment = sentiments[prediction]

        # Render the result template with the predicted sentiment
        return render_template('result.html', sentence=sentence, predicted_sentiment=predicted_sentiment)

if __name__ == '__main__':
    app.run(debug=True ,port = 7860)
