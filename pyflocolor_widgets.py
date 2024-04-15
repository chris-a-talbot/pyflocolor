def back_button(QPushButton):
        back_button.clicked.connect(self.close)
        layout.addWidget(back_button, alignment=Qt.AlignTop | Qt.AlignRight)