from django.db import connection, models
from django.core.cache import cache
from datetime import datetime

class Quote(models.Model):
    quote = models.CharField(max_length=100)
    author = models.CharField(max_length=50)

def get_quote(sort='latest'):
    if sort not in (('latest', 'oldest', 'random')):
        sort = 'latest'
        
    results = try_cache(sort=sort)
    if results:
        console_out('data returned from cache server')

    if not results:
        with connection.cursor() as cursor:
            results = Quote.objects.raw("SELECT * FROM quote_table ORDER BY {};".format(to_order_format(sort)))
        update_cache(sort, results)
        console_out('data returned from DB')
    return results

def insert_quote(quote:str, author:str):
    quote = quote + '.' if not quote.endswith('.') else quote
    quote = quote.replace("'", "''")
    quote = quote.replace('"', '""')
    author = author.upper()

    with connection.cursor() as cursor:
        query = "INSERT INTO quote_table (quote, author) VALUES ('{}','{}');".format(quote, author)
        cursor.execute(query)

    cache.clear()

def to_order_format(sort):
    switch_dict = {
        'latest': 'id DESC',
        'oldest': 'id ASC',
        'random': 'RAND()'
    }
    return switch_dict.get(sort, 'default')

def try_cache(sort):
    key = 'quotes_{}'.format(sort)
    return cache.get(key)

def update_cache(sort, content):
    cache.set('quotes_{}'.format(sort), content)

def console_out(msg:str):
    time = datetime.now().strftime("[%d/%b/%Y %H:%M:%S]")
    print(time+' '+msg)
