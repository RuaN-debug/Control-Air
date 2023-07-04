# Control Air

A simple API to control air conditioners and to show the room temperature and humidity in real time.

## Getting Started

In order to run this, you need to create a virtual environment and install the requirements:
```sh
pip install -r requirements.txt
```

Now you need to copy the .env file and set the environment variables:
```sh
cp .env.example .env
```

Now you just need to run the server with:
```sh
uvicorn server:app --reload --port 8069
```