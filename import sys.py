import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

API_KEY = "1829c074fe507ad5f134b9cce645179d"  

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("-", self)
        self.emoji_label = QLabel("-", self)
        self.description_label = QLabel("-", self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.description_label.setText("Please enter a city name.")
            return

        url = (
            f"http://api.openweathermap.org/data/2.5/weather?q={city}"
            f"&appid={API_KEY}&units=imperial"
        )

        try:
            response = requests.get(url)
            data = response.json()

            if data.get("cod") != 200:
                self.description_label.setText("City not found.")
                self.temperature_label.setText("-")
                self.emoji_label.setText("❓")
                return

            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            weather_main = data["weather"][0]["main"]

            emoji = self.get_weather_emoji(weather_main)

            self.temperature_label.setText(f"{temp}°F")
            self.description_label.setText(description.capitalize())
            self.emoji_label.setText(emoji)

        except Exception as e:
            self.description_label.setText("Error retrieving data.")
            print("Error:", e)

    def get_weather_emoji(self, weather_main):
        """Map weather condition to emoji."""
        mapping = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️",
            "Fog": "🌫️",
            "Haze": "🌫️",
            "Smoke": "🌫️",
            "Dust": "🌪️"
        }
        return mapping.get(weather_main, "❓")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
