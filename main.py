import unittest

from app import create_app

# Create app
app = create_app()


@app.cli.command()
def test():
    test = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(test)
