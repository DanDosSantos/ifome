from flask import Blueprint, render_template, session, request, jsonify
from src.models.usuarios_model import Usuarios
from flask_mail import Message
from app import mail

pedido_bp = Blueprint('pedido', __name__, template_folder='../templates')

# @pedido_bp.route('/pedido/finalizar')
# def finalizar_pedido():
#     usuario = Usuarios.query.get(session.get('usuario_id'))
#     return render_template('finalizar-pedido.html', usuario=usuario)


@pedido_bp.route('/pedido/finalizar', methods=['GET', 'POST'])
def finalizar_pedido():
    usuario = Usuarios.query.get(session.get('usuario_id'))
    if request.method == 'POST':
        dados = request.get_json()
        # Aqui você pode salvar o pedido no banco se quiser

        # Gerar nota fiscal (exemplo simples)
        produtos_formatados = ""
        for item in dados['items']:
            produtos_formatados += f"- {item['nome_item']} (Qtd: {item['quantidade']}) - R$ {item['preco']:.2f}<br>"

        nota_fiscal = f"""
        Olá {usuario.nome},<br>
        Obrigado pela compra!<br>
        Produtos:<br>
        {produtos_formatados}
        Total: R$ {dados['total']}<br>
        Endereço: {dados['address']}<br>
        Observações: {dados['notes']}
        """

        msg = Message(
            subject='Nota Fiscal - iFome',
            recipients=[usuario.email],
            html=nota_fiscal
        )
        mail.send(msg)
        return jsonify({'success': True})
    return render_template('finalizar-pedido.html', usuario=usuario)