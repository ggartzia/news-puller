import hashlib
import html
import re
import time

def clean_html(text):
    html_decoded_string = html.unescape(text)
    return re.sub(r'<(.|\n)*?>', '', html_decoded_string)


def create_unique_id(url):
    return hashlib.sha256(str(url).encode('utf-8')).hexdigest()


def parse_date(date):
	time.strftime("%Y-%m-%d %H:%M:%S", date)