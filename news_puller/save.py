from elasticsearch import Elasticsearch


def iterate_docs(host, port, index, _source=True, body=None):
    client = Elasticsearch(
        [
            {
                'host': host,
                'port': port
            }
        ],
        retry_on_timeout=True
    )

    data = client.search(
        index=index,
        scroll='2m',
        _source=_source,
        body=body
    )

    sid = data['_scroll_id']
    scroll_size = len(data['hits']['hits'])
    for hit in data['hits']['hits']:
        yield hit

    while scroll_size > 0:
        data = client.scroll(scroll_id=sid, scroll='2m')
        for hit in data['hits']['hits']:
            yield hit
        sid = data['_scroll_id']
        scroll_size = len(data['hits']['hits'])


def get_doc(host, port, index, doc_id, _source=True):
    client = Elasticsearch(
        [
            {
                'host': host,
                'port': port
            }
        ]
    )

    return client.get_source(
        index=index,
        id=doc_id,
        _source=_source
    )


def get_docs(host, port, index, ids, _source=True):
    client = Elasticsearch(
        [
            {
                'host': host,
                'port': port
            }
        ]
    )

    response = client.mget(
        index=index,
        body={'ids': ids},
        _source=_source
    )

    docs = response['docs']

    return [doc['_source'] for doc in docs]
