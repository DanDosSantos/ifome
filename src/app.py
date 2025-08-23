# ATENÇAO: ISSO É UM MODELO TESTE PARA VCS VERIFICAREM SE ESTA RODANDO NO NAVEGADOR DE VCS.

from flask import Flask

app = Flask(__name__)

@app.route('/')
def pagina_inicial():
    return '<h1>iFome funcionando! 🚀</h1><p>O container agora vai ficar rodando.</p>'

# Este bloco só será executado quando você rodar o script diretamente
if __name__ == '__main__':
    # app.run() inicia o servidor web e o mantém rodando para sempre
    #
    # host='0.0.0.0' é CRUCIAL para o Docker.
    # Significa que o servidor é visível fora do container.
    app.run(host='0.0.0.0', port=5000, debug=True)