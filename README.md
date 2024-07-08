Sure! Here's a README for your Python-based voice assistant program:

---

# Echo - AI Voice Assistant

Echo is an AI voice assistant that can perform various tasks such as searching Wikipedia, fetching weather information, checking battery status, browsing the internet, and more. It uses several external libraries to achieve its functionality, including `speech_recognition`, `pyttsx3`, `requests`, `wikipedia`, and more.

## Features

- **Greet the user**: Greets the user based on the time of day.
- **Search Wikipedia**: Searches Wikipedia and reads out a summary.
- **Fetch Weather Information**: Provides current weather information based on the user's location.
- **Check Battery Status**: Informs the user about the current battery percentage and whether the power cable is plugged in.
- **Browse the Internet**: Opens various websites such as Google, YouTube, and Gmail.
- **Check Internet Connection**: Checks if the user is connected to the internet.
- **List Available WiFi Networks**: Lists the available WiFi networks.
- **Perform Calculations**: Evaluates basic mathematical expressions.
- **Get User Location**: Provides the user's current city and country.

## Requirements

- Python 3.x
- The following Python libraries:
  - `speech_recognition`
  - `pyttsx3`
  - `datetime`
  - `wikipedia`
  - `requests`
  - `json`
  - `webbrowser`
  - `os`
  - `subprocess`
  - `psutil`
  - `urllib`
  - `platform`
  - `python-dotenv`

## Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/DaviesOwonibi/ECHO
   cd ECHO
   ```

2. **Install the required libraries**:

   ```sh
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in the root directory and add your API keys:

   ```
   WEATHER_API_KEY=your_openweathermap_api_key
   ```

## Usage

Run the script:

```sh
python echo.py
```

### Commands

- **Wikipedia Search**: Say "Wikipedia" followed by the search term.
- **Search the Internet**: Say "Search" followed by the search query.
- **Check Battery Status**: Say "Battery".
- **Greet**: Say "Hello" or "Hi".
- **Shutdown**: Say "Shutdown" or "Bye".
- **Get Weather Information**: Say "Weather".
- **Open YouTube**: Say "YouTube".
- **Open Gmail**: Say "Gmail".
- **Open Google**: Say "Google".
- **Check Time**: Say "What time is it".
- **Check Internet Connection**: Say "Internet".
- **List Available WiFi Networks**: Say "List WiFi".
- **Get Location**: Say "Location".
- **Perform Calculations**: Say "What is" followed by the calculation.

## Customization

You can customize the voice of the assistant by modifying the `setProperty` method in the script:

```python
# Set the desired voice here (by index or ID)
engine.setProperty('voice', voices[0].id)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

---