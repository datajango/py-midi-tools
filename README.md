# Midi Tools created by Anthony Leotta 2021

## Description

This repo was created in order to implment a Midi Library written in Python 3 that follows a Test Driven Development approach.

Goals of this Project:

1. Create a realibe Midi Library
    1. Support Python 3.x and above
    1. Read any Midi 1.0, 1.1 file
    1. API to create Midi files
    1. Fully unit tested
1. Create Tools
    1. Validate a Midi File is correct
    1. Repair damaged Midi files
    1. Split a Midi that is one track with multiple channels into a multiple tracks per channel.
    1. Split a track into multiple channels


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

[View Coverage Report](./htmlcov/index.html)

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