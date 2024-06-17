async function importarArquivoCSV() {
    const contas = CONTEXT.CONTAS;
    const categorias = CONTEXT.CATEGORIAS_ENTRADA_FINANCEIRA;
    const contaOptions = contas.map(conta => `<option value="${conta.id}">${conta.nome}</option>`).join('');
    const categoriaOptions = categorias.map(categoria => `<option value="${categoria.id}">${categoria.descricao}</option>`).join('');

    const { value: contaCategoriaValue } = await swal({
        title: 'Selecione a conta bancária e a categoria de entrada financeira',
        html: `
            <label for="conta-select">Conta</label>
            <select id="conta-select" class="custom-select">${contaOptions}</select>
            <br>
            <label for="categoria-select">Categoria de entrada financeira</label>
            <select id="categoria-select" class="custom-select">${categoriaOptions}</select>
            <input id="file-input" class="swal2-input" type="file" accept=".csv" style="display:none">
        `,
        showCancelButton: true,
        confirmButtonText: 'Próximo',
        cancelButtonText: 'Cancelar',
        preConfirm: () => {
            const conta = document.getElementById('conta-select').value;
            const categoria = document.getElementById('categoria-select').value;
            if (!conta) {
                return Swal.showValidationMessage('Você precisa selecionar uma conta');
            }
            if (!categoria) {
                return Swal.showValidationMessage('Você precisa selecionar uma categoria de entrada financeira');
            }
            return { conta, categoria };
        },
        width: '30rem',
        onOpen: () => {
            document.getElementById('conta-select').addEventListener('change', () => {
                document.getElementById('file-input').style.display = 'block';
            });
            document.getElementById('categoria-select').addEventListener('change', () => {
                document.getElementById('file-input').style.display = 'block';
            });
        },
    });

    if (contaCategoriaValue) {
        const { conta, categoria } = contaCategoriaValue;

        const { value: fileValue } = await swal({
            title: 'Selecione o arquivo CSV',
            html: `
                <input id="file-input" class="swal2-input" type="file" accept=".csv">
            `,
            showCancelButton: true,
            confirmButtonText: 'Importar',
            cancelButtonText: 'Cancelar',
            preConfirm: () => {
                const fileInput = document.getElementById('file-input');
                const file = fileInput.files[0];
                if (!file) {
                    return Swal.showValidationMessage('Você precisa selecionar um arquivo CSV');
                }
                return { file };
            },
            width: '30rem',
        });

        if (fileValue) {
            const { file } = fileValue;

            const formData = new FormData();
            formData.append('conta', conta);
            formData.append('categoria', categoria);
            formData.append('file', file);
            formData.append('csrfmiddlewaretoken', CONTEXT.CSRF_TOKEN);

            $.ajax({
                url: CONTEXT.ROUTES.IMPORT_ENTRADA,
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function (data) {
                    swal('Sucesso!', 'Arquivo importado com sucesso.', 'success').then(() => {
                        window.location.reload();
                    });
                },
                error: function (xhr, status, error) {
                    swal('Erro!', 'Ocorreu um erro ao importar o arquivo.', 'error');
                }
            });
        }
    }
}
