FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl ca-certificates \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean

RUN CHROME_VER=$(google-chrome --version | grep -oP '\d+' | head -1) \
    && DRIVER_VER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VER}") \
    && wget -q "https://chromedriver.storage.googleapis.com/${DRIVER_VER}/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip \
    && chmod +x /usr/local/bin/chromedriver

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "-m", "pytest", "tests.py", "-v", "--tb=short", "--junit-xml=results.xml"]
