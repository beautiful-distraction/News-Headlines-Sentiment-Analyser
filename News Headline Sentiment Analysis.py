import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QComboBox, QTextEdit, \
    QListWidget, QWidget, QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from textblob import TextBlob

API_KEY = "79e3fb6eac1a4039b1925998df704227"
NEWS_API_URL = f"https://newsapi.org/v2/top-headlines"

class NewsApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("News Headlines")
        self.setGeometry(100, 100, 800, 600)

        self.categories = ["general", "business", "entertainment", "health", "science", "sports", "technology"]

        self.category_label = QLabel("Select a category:")
        self.category_menu = QComboBox()
        self.category_menu.addItems(self.categories)

        self.show_news_button = QPushButton("Show News")
        self.news_listbox = QListWidget()
        self.news_text = QTextEdit()
        self.sentiment_label = QLabel("Sentiment: ")

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        font = QFont()
        font.setBold(True)
        label = QLabel("News Headlines Sentiment Analyzer")
        font.setPointSize(20)
        label.setFont(font)

        layout.addWidget(label, alignment=Qt.AlignCenter)

        layout.addWidget(self.category_label)
        layout.addWidget(self.category_menu)
        layout.addWidget(self.show_news_button)
        layout.addWidget(self.news_listbox)
        layout.addWidget(self.news_text)
        layout.addWidget(self.sentiment_label)

        self.show_news_button.clicked.connect(self.display_news)
        self.news_listbox.itemSelectionChanged.connect(self.show_selected_news)

        central_widget.setLayout(layout)

    def fetch_news(self, category):
        params = {
            "apiKey": API_KEY,
            "category": category,
            "country": "in",
        }
        response = requests.get(NEWS_API_URL, params=params)
        data = response.json()

        return data.get("articles", [])

    def display_news(self):
        self.news_listbox.clear()
        category = self.category_menu.currentText()
        articles = self.fetch_news(category)
        for article in articles:
            title = article.get("title", "No title")
            list_item = QListWidgetItem(title)
            font = QFont()
            font.setPointSize(15)
            list_item.setFont(font)
            self.news_listbox.addItem(list_item)

    def show_selected_news(self):
        selected_item = self.news_listbox.currentItem()
        if selected_item:
            index = self.news_listbox.currentRow()
            articles = self.fetch_news(self.category_menu.currentText())
            article = articles[index]
            description = article.get("description", "No description")

            font = QFont()
            font.setPointSize(20)
            self.news_text.setFont(font)

            self.news_text.setPlainText(description)

            sentiment = self.analyze_sentiment(description)

            self.sentiment_label.setText(f"Sentiment: {sentiment}")

    def analyze_sentiment(self, text):
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity

        if polarity > 0:
            sentiment = "This is Positive News"
        elif polarity < 0:
            sentiment = "This is Negative News"
        else:
            sentiment = "This is Neutral News"

        font = QFont()
        font.setPointSize(15)
        self.sentiment_label.setFont(font)

        return sentiment

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NewsApp()
    window.show()
    sys.exit(app.exec_())
