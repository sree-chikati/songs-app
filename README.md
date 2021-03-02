# Songs App🎶
App where you can create playlists and songs!

## Setup

**To run the code**, navigate to the project folder and run the following to install the required packages:

```
pip3 install -r requirements.txt
```

Then, copy the `.env.example` file to `.env`:

```
cp .env.example .env
```

Then you can run the following to run the Flask server:

```
python3 app.py
```

## Running the Tests

**To run all of the tests**, you can run the following from the root project directory:

```
python3 -m unittest discover
```

(Make sure you have unittest installed.)

**To run all tests from a single file**, run the following:

```
python3 -m unittest books_app.main.tests
```

**To run one specific test**, you can run the following:

```
python3 -m unittest books_app.main.tests.MainTests.test_homepage_logged_in
```
