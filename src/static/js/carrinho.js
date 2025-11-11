document.addEventListener('DOMContentLoaded', function () {
    const btn = document.getElementById('btn-sacola');
    const drawer = document.getElementById('cart-drawer');
    const closeBtn = document.getElementById('cart-close');

    function openCart() {
        drawer.classList.remove('translate-x-full');
    }

    function closeCart() {
        drawer.classList.add('translate-x-full');
    }

    // Toggle ao clicar no ícone do carrinho
    btn?.addEventListener('click', function (e) {
        e.preventDefault();
        if (drawer.classList.contains('translate-x-full')) openCart();
        else closeCart();
    });

    closeBtn?.addEventListener('click', closeCart);

    // Fecha com Escape
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeCart();
    });

    // Renderiza carrinho salvo
    let carrinho = [];
    const carrinhoSalvo = localStorage.getItem('carrinho');
    if (carrinhoSalvo) {
        carrinho = JSON.parse(carrinhoSalvo);
    }
    atualizarCarrinho();

    function atualizarCarrinho() {
        const itemsDiv = document.getElementById('cart-items');
        const totalSpan = document.getElementById('cart-total');
        if (!itemsDiv || !totalSpan) return;

        itemsDiv.innerHTML = '';
        let total = 0;

        if (carrinho.length === 0) {
            itemsDiv.innerHTML = '<p class="text-black font-medium text-lg text-center mt-10">Carrinho vazio</p>';
        } else {
            carrinho.forEach((item, idx) => {
                const subtotal = item.preco * item.quantidade;
                total += subtotal;
                const div = document.createElement('div');
                div.className = "flex items-center justify-between gap-2 mb-4";
                div.innerHTML = `
                    <div class="flex-1 min-w-0">
                        <div class="font-medium text-gray-900 truncate">${item.nome_item}</div>
                        <div class="flex items-center gap-2 mt-1">
                            <button class="minus bg-gray-200 px-2 rounded" data-idx="${idx}">-</button>
                            <span class="text-gray-900 font-bold">${item.quantidade}</span>
                            <button class="plus bg-gray-200 px-2 rounded" data-idx="${idx}">+</button>
                        </div>
                    </div>
                    <div class="flex flex-col items-end">
                        <div class="text-green-600 font-bold">R$ ${subtotal.toFixed(2)}</div>
                        <button class="ml-2 text-red-500 text-xl" title="Remover" onclick="removerDoCarrinho(${idx})">&times;</button>
                    </div>
                `;
                itemsDiv.appendChild(div);
            });

            // Adiciona eventos aos botões de quantidade
            itemsDiv.querySelectorAll('.plus').forEach(btn => {
                btn.onclick = function() {
                    const idx = parseInt(this.dataset.idx);
                    carrinho[idx].quantidade++;
                    localStorage.setItem('carrinho', JSON.stringify(carrinho));
                    atualizarCarrinho();
                };
            });
            itemsDiv.querySelectorAll('.minus').forEach(btn => {
                btn.onclick = function() {
                    const idx = parseInt(this.dataset.idx);
                    if (carrinho[idx].quantidade > 1) {
                        carrinho[idx].quantidade--;
                        localStorage.setItem('carrinho', JSON.stringify(carrinho));
                        atualizarCarrinho();
                    }
                };
            });
        }

        totalSpan.textContent = `R$ ${total.toFixed(2)}`;
    }

    // Função global para remover item
    window.removerDoCarrinho = function(idx) {
        carrinho.splice(idx, 1);
        localStorage.setItem('carrinho', JSON.stringify(carrinho));
        atualizarCarrinho();
    };

    // Função global para adicionar item (chame ela no modal do produto)
    window.adicionarAoCarrinho = function(produto, quantidade) {
        const existente = carrinho.find(item => item.nome_item === produto.nome_item);
        if (existente) {
        existente.quantidade += quantidade;
        } else {
        carrinho.push({
            nome_item: produto.nome_item,
            preco: parseFloat(produto.preco),
            quantidade: quantidade
        });
        }
        localStorage.setItem('carrinho', JSON.stringify(carrinho));
        atualizarCarrinho();
    };
});