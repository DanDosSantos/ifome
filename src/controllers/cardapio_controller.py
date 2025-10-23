from flask import Blueprint, request, jsonify, render_template, redirect, url_for,session
from app import db
from src.models.cardapio_model import Cardapio
from src.models.produtos_model import Produto

cardapio_bp = Blueprint('cardapio', __name__, template_folder='../templates')

@cardapio_bp.route('/cardapio', methods=['GET'])
def pagcardapio():
    try:
        # Exemplo: supondo que o ID do restaurante está guardado na sessão
        from flask import session

        restaurante_id = session.get('restaurante_id')
        if not restaurante_id:
            return redirect(url_for('restaurante.portal_parceiro'))

        # Busca todos os cardápios do restaurante
        cardapios = Cardapio.query.filter_by(restaurante_id=restaurante_id).all()
        for c in cardapios:
            c.itens_cardapio = Produto.query.filter_by(cardapio_id=c.id).all()

        # Renderiza o template e passa os cardápios
        return render_template('cardapio.html', cardapios=cardapios)

    except Exception as e:
        print("❌ Erro ao carregar cardápios:", e)
        return jsonify({'erro': str(e)}), 500

@cardapio_bp.route('/cadastro-cardapio', methods=['GET']) 
def cadastro_cardapio(): 
    return render_template('cadastro-cardapio.html')
    
@cardapio_bp.route('/cardapio/api/cadastrar', methods=['POST'])
def cadastrar_cardapio():
    try:
        data = request.get_json()

        nome_cardapio = data.get('nome_cardapio')
        # Pega o restaurante logado da sessão
        restaurante_id = session.get('restaurante_id')
        ativo = data.get('ativo', True)

        if not nome_cardapio or not restaurante_id:
            return jsonify({'erro': 'Campos obrigatórios faltando'}), 400

        novo_cardapio = Cardapio(
            nome_cardapio=nome_cardapio,
            restaurante_id=restaurante_id,
            ativo=ativo
        )

        db.session.add(novo_cardapio)
        db.session.commit()

        print(f"✅ Cardápio '{novo_cardapio.nome_cardapio}' cadastrado com sucesso!")

        # 🔹 Redireciona para a página de cardápios
        return redirect(url_for('cardapio.pagcardapio'))

    except Exception as e:
        db.session.rollback()
        print("❌ Erro ao cadastrar cardápio:", e)
        return jsonify({'erro': str(e)}), 500

# Página de edição do cardápio
@cardapio_bp.route('/cardapio/editar/<int:cardapio_id>', methods=['GET', 'POST'])
def editar_cardapio(cardapio_id):
    cardapio = Cardapio.query.get_or_404(cardapio_id)

    if request.method == 'POST':
        nome_cardapio = request.form.get('nome_cardapio')
        ativo = True if request.form.get('ativo') == 'on' else False

        cardapio.nome_cardapio = nome_cardapio
        cardapio.ativo = ativo

        try:
            db.session.commit()
            return redirect(url_for('cardapio.pagcardapio'))
        except Exception as e:
            db.session.rollback()
            return f"Erro ao atualizar cardápio: {e}", 500

    return render_template('editar-cardapio.html', cardapio=cardapio)

# Rota de exclusão do cardápio
@cardapio_bp.route('/cardapio/excluir/<int:cardapio_id>', methods=['POST'])
def excluir_cardapio(cardapio_id):
    cardapio = Cardapio.query.get_or_404(cardapio_id)

    try:
        db.session.delete(cardapio)
        db.session.commit()
        return redirect(url_for('cardapio.pagcardapio'))
    except Exception as e:
        db.session.rollback()
        return f"Erro ao excluir cardápio: {e}", 500
