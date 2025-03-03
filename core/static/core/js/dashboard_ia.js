
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

    // Função para ler o arquivo CSV ou XLS
    document.getElementById('fileInput').addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const data = e.target.result;
                // Simulação de leitura de CSV (para XLS/XLSX, use uma biblioteca como SheetJS)
                const rows = data.split('\n').map(row => row.split(','));
                renderTable(rows);
            };
            reader.readAsText(file);
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