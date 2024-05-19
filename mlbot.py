import Constants
import sys
import openai
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox
)

openai.api_key = Constants.API_KEY

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap('robot.jpg').scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(self.logo_pixmap)
        self.input_label = QLabel('Ask a question:')
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('Type here...')
        self.answer_field = QTextEdit()
        self.answer_field.setReadOnly(True)
        self.submit_button = QPushButton('Submit')
        self.submit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                border: None;
                padding: 15px 32px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #3e8e41;
            }
            """
        )

        # Popular questions
        self.popular_questions_group = QGroupBox('Popular Questions')
        self.popular_questions_layout = QVBoxLayout()
        self.popular_questions = [
            "What is Machine Learning?", 
            "How do I become a Machine Learning Engineer?", 
            "What are some popular Machine Learning algorithms?"
        ]
        self.question_buttons = []

        for question in self.popular_questions:
            button = QPushButton(question)
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #FFFFFF;
                    border: 2px solid #00AEFF;
                    padding: 10px 20px;
                    font-size: 18px;
                    font-weight: bold;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #E0F7FF;
                }
                """
            )
            button.clicked.connect(lambda _, q=question: self.input_field.setText(q))
            self.popular_questions_layout.addWidget(button)
            self.question_buttons.append(button)

        self.popular_questions_group.setLayout(self.popular_questions_layout)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

        # Add input field
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_field)
        layout.addLayout(input_layout)

        layout.addWidget(self.submit_button)
        layout.addWidget(self.answer_field)
        layout.addWidget(self.popular_questions_group)

        # Set the layout
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('Machine Learning Career Help Bot')
        self.setGeometry(200, 200, 600, 600)

        # Connect the submit button to the function which queries OpenAI API
        self.submit_button.clicked.connect(self.get_answer)
    
    def get_answer(self):
        question = self.input_field.text()
        try:
            completion = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": "You are a Machine Learning Engineering Expert. Answer the following question in a concise way or with bullet points."},
                    {"role": "user", "content": question}
                ],
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7
            )

            answer = completion.choices[0].message['content']
            self.answer_field.setText(answer)
        except Exception as e:
            self.answer_field.setText(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
