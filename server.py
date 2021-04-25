from sanic import Sanic
from sanic.response import text
from asyncio import sleep


app = Sanic(name='Sanic_serv')

@app.route('/')
async def test(request):
    await sleep(1)
    return text('Hello')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


