import loader
from uvicorn import run

if __name__ == '__main__':
    run(
        loader.app,
        host='0.0.0.0',
        port=801,
    )