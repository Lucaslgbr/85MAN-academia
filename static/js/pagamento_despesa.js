async function payExpense(id, valor_pendente, contas) {
    categorias = CONTEXT.CATEGORIAS_SAIDA_FINANCEIRA;
    contas = CONTEXT.CONTAS;
    const contaOptions = contas.map(conta => `<option value="${conta.id}">${conta.nome}</option>`).join('');
    const categoriasOptions = categorias.map(categoria => `<option value="${categoria.id}">${categoria.descricao}</option>`).join('');

    const { value: inputValue } = await swal({
        title: 'Informe o valor a ser pago',
        html:
            '<input id="valor-input" class="swal2-input" type="number" placeholder="Digite o valor">' +
            '<br>' +
            '<input id="checkbox-input" class="swal2-checkbox" type="checkbox">' +
            '<label for="checkbox-input"> Gerar registro de saída financeira?</label>' +
            '<br>' +
            '<label for="conta-select">Conta</label>' +
            `<select id="conta-select" class="custom-select" disabled>${contaOptions}</select>`+
            '<label for="categoria-select">Categoria de saída financeira</label>' +
            `<select id="categoria-select" class="custom-select" disabled>${categoriasOptions}</select>`,

            
        showCancelButton: true,
        confirmButtonText: 'Pagar',
        cancelButtonText: 'Cancelar',
        preConfirm: () => {
            const valor = document.getElementById('valor-input').value;
            const checkbox = document.getElementById('checkbox-input').checked;
            const conta = document.getElementById('conta-select').value;
            const categoria = document.getElementById('categoria-select').value;
            return { valor, checkbox, conta, categoria };
        },
        inputValidator: (result) => {
            const { valor, checkbox } = result;
            if (!valor) {
                return 'Você precisa informar um valor';
            }
            if (parseFloat(valor) <= 0) {
                return 'O valor deve ser maior que zero';
            }
            if (parseFloat(valor) > valor_pendente) {
                return 'O valor não pode ser maior que o valor restante da despesa';
            }
            if (checkbox && !result.conta) {
                return 'Selecione a conta bancária de onde sairá o dinheiro';
            }
            if (checkbox && !result.categoria) {
                return 'Selecione a categoria de saída financeira';
            }
        },
        width: '40rem',
        onOpen: () => {
            document.getElementById('checkbox-input').addEventListener('change', (e) => {
                const contaSelect = document.getElementById('conta-select');
                const categoriaSelect = document.getElementById('categoria-select');
                contaSelect.disabled = !e.target.checked;
                categoriaSelect.disabled = !e.target.checked;
            });
        },
    });
    if (inputValue) {
        const { valor, checkbox, conta, categoria } = inputValue;
        debugger
        $.ajax({
            url: CONTEXT.ROUTES.DESPESA,
            method: 'POST',
            data: {
                despesa: id,
                valor: valor,
                conta: conta, 
                categoria_saida_financeira: categoria,
                csrfmiddlewaretoken: CONTEXT.CSRF_TOKEN,
            },
            success: function (data) {
                window.location.reload();
            },
        });
    }
}
