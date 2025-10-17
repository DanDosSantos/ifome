from flask import Blueprint, request, jsonify, render_template,flash,redirect,url_for,session
from app import db
from src.models.produtos_model import Produto
from src.models.cardapio_model import Cardapio

produto_bp = Blueprint('produto', __name__, template_folder='../templates')

# Tela de cadastro de produto com cardápio pré-selecionado
@produto_bp.route('/cadastro-produto/<int:cardapio_id>', methods=['GET'])
def cadastro_produto_com_cardapio(cardapio_id):
    cardapio = Cardapio.query.get_or_404(cardapio_id)
    return render_template(
        'cadastro-produto.html', 
        cardapio_id=cardapio.id, 
        cardapio_nome=cardapio.nome_cardapio
    )

# API que salva produto no banco
@produto_bp.route('/produto/api/cadastrar', methods=['POST'])
def cadastrar_produto():
    try:
        data = request.get_json()

        nome_item = data.get('nome_item')
        descricao = data.get('descricao', '')
        preco = data.get('preco')
        disponivel = data.get('disponivel', True)
        cardapio_id = data.get('cardapio_id')
        restaurante_id = session.get('restaurante_id')

        if not nome_item or not preco or not cardapio_id or not restaurante_id:
            return jsonify({'status': 'erro', 'mensagem': 'Campos obrigatórios faltando'}), 400

        cardapio = Cardapio.query.get(cardapio_id)
        if not cardapio:
            return jsonify({'status': 'erro', 'mensagem': 'Cardápio não encontrado'}), 404

        novo_produto = Produto(
            nome_item=nome_item,
            descricao=descricao,
            preco=preco,
            disponivel=disponivel,
            cardapio_id=cardapio.id,
            restaurante_id=restaurante_id
        )

        db.session.add(novo_produto)
        db.session.commit()

        return jsonify({
            'status': 'sucesso',
            'mensagem': 'Produto cadastrado com sucesso!',
            'redirect': url_for('cardapio.pagcardapio')
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500

# Editar produto
@produto_bp.route('/produto/<int:produto_id>/editar', methods=['GET', 'POST'])
def editar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)

    if request.method == 'POST':
        produto.nome_item = request.form['nome_item']
        produto.descricao = request.form.get('descricao', '')
        produto.preco = request.form['preco']
        produto.disponivel = 'disponivel' in request.form

        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('cardapio.pagcardapio'))

    return render_template('editar-produto.html', produto=produto)


# Excluir produto
@produto_bp.route('/produto/<int:produto_id>/excluir', methods=['POST'])
def excluir_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('cardapio.pagcardapio'))
