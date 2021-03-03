# Midi Tools created by Anthony Leotta 2021

## Description

This repo was created in order to implment a Midi Library written in Python 3 that follows a Test Driven Development approach.

To run the read tester program:
```
conda activate pyaudio
python src\tools\read.py assets\a.mid
```

To run unit tests:

```
pytest
coverage run -m pytest
coverage html
```

## Conda

1. Create a new anaconda Environment

    ```
    conda create --name pyaudio python=3.8
    ```

1. Activate Anaconda Environment

    ```
    conda activate pyaudio
    ```

1. Add PIP Requirements

    ```
    pip install -r requirements.txt
    ```

## Testing

```
pyttest
```

```
coverage run -m pytest
```

```
coverage report -m
```

```
coverage html
```

Creates [Coverage](./htmlcov/index.html) Report