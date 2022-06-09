import hashlib
import html
import re
import time

def clean_html(text):
    html_decoded_string = html.unescape(text)
    processed_text = re.sub(r'<(.|\n)*?>', '', html_decoded_string)
    processed_text = re.sub(r'(?:\@|http?\://|https?\://|www)\S+', '', text)
    processed_text = " ".join(processed_text.split())
    return processed_text


def create_unique_id(url):
    return hashlib.sha256(str(url).encode('utf-8')).hexdigest()


def parse_date(date):
	time.strftime("%Y-%m-%d %H:%M:%S", date)