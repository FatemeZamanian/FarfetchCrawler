import argparse
from crawler import Crawler


def main(url, output):
    crl = Crawler()
    crl(url, output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url", type=str, default="https://www.farfetch.com/uk/shopping/men/burberry-check-print-stretch-cotton-shirt-item-19844301.aspx", help="link of cloths page.")
    parser.add_argument("--output", type=str, default="output",
                        help="output directory path")
    args = parser.parse_args()
    main(args.url, args.output)
