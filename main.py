# main.py
import sys
import os

# Add the lib directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

from cli import cli

if __name__ == '__main__':
    cli()
