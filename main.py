import sys
import os

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGroupBox, QListWidget, 
                             QScrollArea, QHBoxLayout, QTabWidget, QLineEdit, QPushButton,
                             QLabel)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from src.recommend_by_keyword import recommend_by_keyword

WORDCLOUD_DIR = os.path.join(os.getcwd(), 'data', 'wordcloud_images')

category_list = [
    'Art',
    'Child',
    'Computer-Internet',
    'Economics-Management',
    'Elementary-Learning',
    'Health-Beauty',
    'History-Culture',
    'Hobby-Leisure',
    'Home-Life',
    'Humanity',
    'Infant',
    'Nature-Science',
    'Novel',
    'Poem-Essay',
    'SelfDevelopment',
    'SocialScience',
    'Teen',
    'Total',
    'Travel'
]


def create_books_tabs(recommendations):
    tabs = QTabWidget()

    # Extract all keywords
    all_keywords = set(k for cat in recommendations.values() for k in cat)

    # Sort (if needed) and then reverse the order of keywords
    sorted_keywords = sorted(all_keywords)  # You can remove this line if sorting is not required
    sorted_keywords.reverse()  # Reverse the order

    for keyword in sorted_keywords:
        # Create a scroll area for each tab
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        books_added = False

        for category_key, keywords_books in recommendations.items():
            if keyword in keywords_books:
                books = keywords_books[keyword][:5]  # Limit to top 5 books
                if books:
                    books_added = True

                    # Process the category name
                    category_name = category_key.replace('_data_for_recommendation', '').replace('_', ' ').capitalize()
                    group_box = QGroupBox(f"{category_name} Books")
                    books_layout = QVBoxLayout()

                    for book in books:
                        book_label = QLabel(book)
                        books_layout.addWidget(book_label)

                    group_box.setLayout(books_layout)
                    scroll_layout.addWidget(group_box)

        if not books_added:
            no_books_label = QLabel(f"No books available for keyword '{keyword}'")
            scroll_layout.addWidget(no_books_label)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        tabs.addTab(scroll_area, keyword.capitalize())

    return tabs


def create_category_group_box(category_name, books):
    group_box = QGroupBox(category_name)
    vbox = QVBoxLayout()

    book_list_widget = QListWidget()
    book_list_widget.addItems(books)
    vbox.addWidget(book_list_widget)

    group_box.setLayout(vbox)
    return group_box


def on_keyword_process():
    entered_keyword = keyword_input.text()
    res = recommend_by_keyword(ent  ered_keyword)

    # Clear existing content in the layout
    for i in reversed(range(keyword_layout.count())): 
        widget = keyword_layout.itemAt(i).widget()
        if widget is not None:
            widget.deleteLater()

    if not res:
        keyword_result_label.setText("No recommendations available for this keyword.")
        return

    # Create the tabs with keywords
    tabs = create_books_tabs(res)
    
    # Add the tabs to the keyword layout
    keyword_layout.addWidget(tabs)


def on_category_selected():
    selected_category = category_list_widget.currentItem().text()
    year_list.clear()
    years = [str(year) for year in range(2013, 2024)]
    year_list.addItems(years)


def on_year_selected():
    selected_category = category_list_widget.currentItem().text()
    selected_year = year_list.currentItem().text()

    # 카테고리와 년도에 따른 이미지 파일 경로 생성
    image_file_path = os.path.join(WORDCLOUD_DIR, selected_category, f"{selected_category}_{selected_year}_wordcloud.png")

    # 이미지 파일이 존재하는지 확인
    if os.path.exists(image_file_path):
        pixmap = QPixmap(image_file_path)
        image_label.setPixmap(pixmap.scaled(image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    else:
        image_label.setText("Image not available.")


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('Ajoulib')

tab_widget = QTabWidget()

# Keyword Input Tab
keyword_tab = QWidget()
keyword_layout = QVBoxLayout(keyword_tab)

# Horizontal layout for input field and button
input_layout = QHBoxLayout()

# User input for keyword
keyword_input = QLineEdit()
input_layout.addWidget(keyword_input)

# Button for processing keyword
process_keyword_button = QPushButton('Process Keyword')
process_keyword_button.clicked.connect(on_keyword_process)
input_layout.addWidget(process_keyword_button)

keyword_layout.addLayout(input_layout)

# Label to display result
keyword_result_label = QLabel()
keyword_layout.addWidget(keyword_result_label)

keyword_tab.setLayout(keyword_layout)

# Trend Analysis Tab
results_tab = QWidget()
trend_layout = QVBoxLayout(results_tab)

# Horizontal layout for category and year lists
lists_layout = QHBoxLayout()

# Category List
category_list_widget = QListWidget()
category_list_widget.addItems(category_list)  # 선언된 카테고리 리스트를 추가
category_list_widget.itemClicked.connect(on_category_selected)
lists_layout.addWidget(category_list_widget)

# Year List
year_list = QListWidget()
year_list.itemClicked.connect(on_year_selected)
lists_layout.addWidget(year_list)

trend_layout.addLayout(lists_layout, 1)  # Adding lists layout with a smaller stretch factor

# Image Display Label with larger stretch factor
image_label = QLabel()
image_label.setScaledContents(True)
trend_layout.addWidget(image_label, 4)

results_tab.setLayout(trend_layout)

# Adding Tabs
tab_widget.addTab(keyword_tab, "Keyword Input")
tab_widget.addTab(results_tab, "Trend Analysis")

# Main Layout Setup
layout = QHBoxLayout(window)
layout.addWidget(tab_widget)

window.setLayout(layout)
window.setFixedSize(800, 600)

window.show()
sys.exit(app.exec_())