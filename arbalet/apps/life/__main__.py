import argparse
from .life import Life

parser = argparse.ArgumentParser(description='Game of life - randomely generated')

Life(parser, 50).start()