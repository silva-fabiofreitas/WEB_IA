
class IA {
    constructor() {
        this.api = '/text-to-sql/';
    }

    async process(instructions) {
        const response = await fetch(`${this.api}?question=${instructions}`);
        const data = await response.json();
        return JSON.parse(data);
    }
    async initChart(instructions) {
        const myChart = echarts.init(document.getElementById('chart'));
        myChart.showLoading();
        const data = await this.process(instructions);
        myChart.setOption(data);
        myChart.hideLoading();
    }
}

    document.getElementById('saveFile').addEventListener('click', function () {
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];

        if (!file) {
            alert('Selecione um arquivo antes de enviar.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

            fetch('/text-to-sql/', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('response').textContent = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                console.error('Erro:', error);
                document.getElementById('response').textContent = 'Erro ao enviar o arquivo.';
            });
    });

    // Função para ler o arquivo CSV, XLS ou XLSX
    document.getElementById('fileInput').addEventListener('change', function (event) {
        const file = event.target.files[0];
        console.log(file);
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const data = e.target.result;
                let rows = [];

                // Verificar o tipo de arquivo
                if (file.name.endsWith('.csv')) {
                    // Processar CSV
                    rows = data.split('\n').map(row => row.split(','));
                } else if (file.name.endsWith('.xls') || file.name.endsWith('.xlsx')) {
                    // Processar XLS/XLSX com SheetJS
                    const workbook = XLSX.read(data, { type: 'binary' });
                    const sheetName = workbook.SheetNames[0]; // Pega a primeira planilha
                    const sheet = workbook.Sheets[sheetName];
                    rows = XLSX.utils.sheet_to_json(sheet, { header: 1 }); // Converte para JSON
                }

                // Renderizar a tabela
                renderTable(rows);
            };

            if (file.name.endsWith('.csv')) {
                reader.readAsText(file);
            } else {
                reader.readAsBinaryString(file); // Para XLS/XLSX
            }
        }
    });

    // Função para renderizar a tabela de pré-visualização
    function renderTable(rows) {
        const tableHeader = document.getElementById('tableHeader');
        const tableBody = document.getElementById('tableBody');
        tableHeader.innerHTML = '';
        tableBody.innerHTML = '';

        if (rows.length > 0) {
            // Cabeçalho
            rows[0].forEach(header => {
                tableHeader.innerHTML += `<th>${header}</th>`;
            });

            // Dados
            rows.slice(1).forEach(row => {
                const tr = document.createElement('tr');
                row.forEach(cell => {
                    tr.innerHTML += `<td>${cell}</td>`;
                });
                tableBody.appendChild(tr);
            });
        }
    }

    // Função para processar as instruções com a IA
    document.getElementById('processButton').addEventListener('click', function () {
        const instructions = document.getElementById('instructions');
        if (!instructions.checkValidity()) {
            instructions.reportValidity()
            throw 'Insira as instruções'
        }

        const ia = new IA();
        ia.initChart(instructions.value);
    })