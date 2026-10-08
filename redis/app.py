from flask import Flask, request
import redis
import time


app = Flask(__name__)
db = redis.Redis(host='redis', port=6379, db=0)

@app.route('/')
def hello():
    start = time.time()
    count = db.incr('hits')
    elapsed = time.time() - start
    return f'Hello World! I have been seen {count} times.\nTempo de resposta: {elapsed:.6f} segundos'

@app.route('/sem-redis')
def hellow():
    start = time.time()
    response = 'Hello World! I have been seen times.'
    elapsed = time.time() - start
    return f'{response}\nTempo de resposta: {elapsed:.6f} segundos'


@app.route('/set/<chave>/<valor>')
def set_valor(chave, valor):
    db.set(chave, valor)
    return f'Valor {valor} foi armazenado com a chave {chave}'

@app.route('/get/<chave>')
def get_valor(chave):
    valor = db.get(chave)
    if valor:
        return f'Valor recuperado: {valor.decode("utf-8")}'
    else:
        return 'Chave não encontrada'

@app.route('/push/<lista>/<valor>')
def push_lista(lista, valor):
    db.lpush(lista, valor)
    return f'Valor {valor} adicionado à lista {lista}'

@app.route('/pop/<lista>')
def pop_lista(lista):
    valor = db.lpop(lista)
    if valor:
        return f'Valor retirado da lista {lista}: {valor.decode("utf-8")}'
    else:
        return f'Lista {lista} está vazia ou não existe'

@app.route('/listar/<lista>')
def listar_valores(lista):
    valores = db.lrange(lista, 0, -1)
    return f'Valores na lista {lista}: {[valor.decode("utf-8") for valor in valores]}'


def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

@app.route('/fib/<int:n>')
def fib_sem_cache(n):
    start = time.time()
    resultado = fib(n)
    elapsed = time.time() - start
    return f'[SEM CACHE] Fibonacci({n}) = {resultado} (tempo: {elapsed:.4f} segundos)'

@app.route('/fib-cache/<int:n>')
def fib_com_cache(n):
    start = time.time()

    cache_key = f"fib:{n}"
    if db.exists(cache_key):
        resultado = int(db.get(cache_key))
        source = "Redis (cache)"
    else:
        resultado = fib(n)
        db.setex(cache_key, 60, resultado)
        source = "calculado e salvo no Redis"

    elapsed = time.time() - start
    return f'[COM CACHE] Fibonacci({n}) = {resultado} ({source}) (tempo: {elapsed:.4f} segundos)'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
