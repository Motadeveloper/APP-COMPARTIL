document.addEventListener("DOMContentLoaded", function() {
    let valorFreteSelecionado = 0;
    let tipoFreteSelecionado = '';
    let datasIndisponiveis = {};

    const startBookingButton = document.getElementById('startBooking');
    if (startBookingButton) {
        startBookingButton.addEventListener('click', function() {
            document.getElementById('detalhesEquipamentoContainer').style.display = 'none';
            document.getElementById('bookingFormContainer').style.display = 'block';
            //document.getElementById('step1').scrollIntoView({ behavior: 'smooth' });
        });
    }

    const dataContainer = document.getElementById('data-container');
    const quantidadeSelecionada = document.getElementById('quantidade-selecionada');
    const valorTotal = document.getElementById('valor-total');
    const freteSelecionado = document.getElementById('frete-selecionado');
    const tipoFrete = document.getElementById('tipo-frete');
    const detalhesEquipamentoContainer = document.getElementById('detalhesEquipamentoContainer');
    const equipamentoId = detalhesEquipamentoContainer.dataset.equipId;
    let valorDiaria;

    function fetchValorDiaria() {
        fetch(`/api/equipamento/${equipamentoId}/valor_diaria/`)
            .then(response => response.json())
            .then(data => {
                valorDiaria = parseFloat(data.preco_diaria);
                console.log('Valor da Diária:', valorDiaria);
            })
            .catch(error => {
                console.error('Erro ao buscar valor da diária:', error);
            });
    }

    fetchValorDiaria();

    const hoje = new Date();
    let dataInicio = null;
    let dataFim = null;

    function mostrarAlerta(mensagem) {
        const alertContainer = document.getElementById('alert-container');
        alertContainer.innerHTML = `
            <div class="alert-card">
                ${mensagem}
                <div class="alert-timer"></div>
            </div>
        `;

        setTimeout(() => {
            alertContainer.innerHTML = '';
            limparSelecao();
        }, 2000); // Remove o alerta após 2 segundos
    }

    function mostrarAlertaStep2(mensagem) {
        const alertContainerStep2 = document.getElementById('alert-container-step2');
        alertContainerStep2.innerHTML = `
            <div class="alert-card">
                ${mensagem}
                <div class="alert-timer"></div>
            </div>
        `;

        setTimeout(() => {
            alertContainerStep2.innerHTML = '';
        }, 2000); // Remove o alerta após 2 segundos
    }

    function mostrarAlertaCPF(mensagem) {
        const alertContainerCPF = document.getElementById('alert-container-cpf');
        alertContainerCPF.innerHTML = `
            <div class="alert-card">
                ${mensagem}
                <div class="alert-timer"></div>
            </div>
        `;

        setTimeout(() => {
            alertContainerCPF.innerHTML = '';
        }, 2000); // Remove o alerta após 2 segundos
    }

    function limparSelecao() {
        dataInicio = null;
        dataFim = null;
        atualizarSelecao();
    }

    function atualizarSelecao() {
        const bolinhas = document.querySelectorAll('.data-bolinha');
        let contagemSelecionada = 0;
        bolinhas.forEach(bolinha => {
            const data = new Date(bolinha.dataset.date);
            if (dataInicio && dataFim && data >= dataInicio && data <= dataFim) {
                if (datasIndisponiveis[bolinha.dataset.date]?.disponivel === false) {
                    bolinha.classList.add('indisponivel');
                    bolinha.classList.add('disabled');
                } else {
                    bolinha.classList.add('selected-range');
                    contagemSelecionada++;
                }
            } else if (dataInicio && data.getTime() === dataInicio.getTime()) {
                bolinha.classList.add('selected-start');
                contagemSelecionada++;
            } else {
                bolinha.classList.remove('selected-range');
                bolinha.classList.remove('selected-start');
            }
        });

        const quantidadeBolinhas = Math.max(0, contagemSelecionada - 1);
        quantidadeSelecionada.textContent = `Quantidade de diária(s): ${quantidadeBolinhas} dias`;

        let total = quantidadeBolinhas * valorDiaria;
        let desconto = 0;
        let mensagemDesconto = '';

        if (quantidadeBolinhas >= 7) {
            desconto = total * 0.58;
            mensagemDesconto = '<br>(Desconto de 58% aplicado)';
        } else if (quantidadeBolinhas >= 3) {
            desconto = total * 0.40;
            mensagemDesconto = '<br>(Desconto de 40% aplicado)';
        }

        total -= desconto;
        total += valorFreteSelecionado;
        valorTotal.innerHTML = `Valor Total: R$ ${total.toFixed(2)}${mensagemDesconto}`;

        if (freteSelecionado) {
            freteSelecionado.textContent = `Valor do Frete: R$ ${valorFreteSelecionado.toFixed(2)}`;
        }
        if (tipoFrete) {
            tipoFrete.textContent = `Tipo de Frete: ${tipoFreteSelecionado}`;
        }

        const hiddenValorTotal = document.getElementById("hidden_valor_total");
        if (hiddenValorTotal) {
            hiddenValorTotal.value = total.toFixed(2);
        }

        document.getElementById("hidden_data_inicio").value = dataInicio ? dataInicio.toISOString().split('T')[0] : '';
        document.getElementById("hidden_data_fim").value = dataFim ? dataFim.toISOString().split('T')[0] : '';

        console.log('Valor Total:', total);
        console.log('Data Início:', dataInicio);
        console.log('Data Fim:', dataFim);
    }

    function carregarDatasIndisponiveis() {
        fetch(`/api/equipamento/${equipamentoId}/disponibilidade/`)
            .then(response => response.json())
            .then(data => {
                datasIndisponiveis = data.disponibilidades;
                for (let i = 0; i < 30; i++) {
                    const dataAtual = new Date(hoje);
                    dataAtual.setDate(hoje.getDate() + i);
                    const dia = dataAtual.getDate();
                    const mes = dataAtual.toLocaleString('default', { month: 'short' });
                    const diaSemana = dataAtual.toLocaleString('default', { weekday: 'short' }).substring(0, 3);

                    const bolinha = document.createElement('div');
                    bolinha.className = 'data-bolinha';
                    bolinha.innerHTML = `<span>${dia}</span><small>${mes}</small><small class="day-name">${diaSemana}</small>`;
                    bolinha.dataset.date = dataAtual.toISOString().split('T')[0];

                    if (datasIndisponiveis[bolinha.dataset.date]?.disponivel === false) {
                        bolinha.classList.add('indisponivel');
                        bolinha.classList.add('disabled');
                    } else {
                        bolinha.addEventListener('click', function() {
                            const dataClicada = new Date(bolinha.dataset.date);
                            if (!dataInicio || (dataInicio && dataFim)) {
                                dataInicio = dataClicada;
                                dataFim = null;
                                bolinha.classList.add('selected-start');
                                carregarHorariosDisponiveis(dataClicada, datasIndisponiveis[bolinha.dataset.date]?.horario_final_locacao);
                            } else if (dataClicada >= dataInicio) {
                                if (!verificarDisponibilidadeIntervalo(dataInicio, dataClicada)) {
                                    mostrarAlerta("Intervalo de datas selecionado contém datas indisponíveis. Por favor, selecione outro intervalo.");
                                } else {
                                    dataFim = dataClicada;
                                    atualizarSelecao();
                                }
                            }
                        });
                    }
                    dataContainer.appendChild(bolinha);
                }
            })
            .catch(error => {
                console.error('Erro ao carregar datas indisponíveis:', error);
            });
    }

    function verificarDisponibilidadeIntervalo(dataInicio, dataFim) {
        let dataAtual = new Date(dataInicio);
        while (dataAtual <= dataFim) {
            const dataString = dataAtual.toISOString().split('T')[0];
            if (datasIndisponiveis[dataString]?.disponivel === false) {
                return false;
            }
            dataAtual.setDate(dataAtual.getDate() + 1);
        }
        return true;
    }

    function carregarHorariosDisponiveis(data, horarioFinalLocacao) {
        const horaContainer = document.getElementById('hora-container');
        const horaSelect = document.getElementById('hora_inicio');
        horaSelect.innerHTML = '';

        const horariosDisponiveis = [];
        const inicioHoras = horarioFinalLocacao ? parseInt(horarioFinalLocacao.split(':')[0], 10) + 1 : 8;

        for (let h = inicioHoras; h <= 17; h++) {
            const horario = `${h < 10 ? '0' : ''}${h}:00`;
            horariosDisponiveis.push(horario);
        }

        horariosDisponiveis.forEach(horario => {
            const option = document.createElement('option');
            option.value = horario;
            option.text = horario;
            horaSelect.appendChild(option);
        });

        horaContainer.style.display = 'block';
    }

    function verificarCamposDataHora() {
        const horaInicio = document.getElementById('hora_inicio').value;
        return dataInicio && horaInicio;
    }

    const nextToStep2Button = document.getElementById('nextToStep2');
    if (nextToStep2Button) {
        nextToStep2Button.addEventListener('click', function() {
            if (verificarCamposDataHora()) {
                document.getElementById('step1').style.display = 'none';
                document.getElementById('step2').style.display = 'block';
                document.getElementById('step2').style.overflow = 'hidden';
            } else {
                mostrarAlerta("Por favor, selecione a data de início e fim da locação, bem como o horário de início.");
            }
        });
    }

    const backToEquipamentoButton = document.getElementById('backToEquipamento');
    if (backToEquipamentoButton) {
        backToEquipamentoButton.addEventListener('click', function() {
            document.getElementById('bookingFormContainer').style.display = 'none';
            document.getElementById('detalhesEquipamentoContainer').style.display = 'block';
            document.getElementById('detalhesEquipamentoContainer').scrollIntoView({ behavior: 'smooth' });
        });
    }

    const backToStep1Button = document.getElementById('backToStep1');
    if (backToStep1Button) {
        backToStep1Button.addEventListener('click', function() {
            document.getElementById('step2').style.display = 'none';
            document.getElementById('step1').style.display = 'block';
            document.getElementById('step1').scrollIntoView({ behavior: 'smooth' });
        });
    }

    const nextToStep3Button = document.getElementById('nextToStep3');
    if (nextToStep3Button) {
        nextToStep3Button.addEventListener('click', function() {
            const cep = document.getElementById('cep').value;
            const freteOpcao = document.querySelector('input[name="frete_opcao"]:checked');
            const numero = document.getElementById('numero').value;
            const complemento = document.getElementById('complemento').value;

            if (!cep || !freteOpcao || !numero || !complemento) {
                mostrarAlertaStep2("Por favor, preencha todos os campos obrigatórios antes de continuar.");
            } else {
                document.getElementById('step2').style.display = 'none';
                document.getElementById('step3').style.display = 'block';
                document.getElementById('step3').scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    const backToStep3Button = document.getElementById('backToStep3');
    if (backToStep3Button) {
        backToStep3Button.addEventListener('click', function() {
            document.getElementById('step4').style.display = 'none';
            document.getElementById('step3').style.display = 'block';
            document.getElementById('step3').scrollIntoView({ behavior: 'smooth' });
        });
    }

    const backToStep3FromStep5Button = document.getElementById('backToStep3FromStep5');
    if (backToStep3FromStep5Button) {
        backToStep3FromStep5Button.addEventListener('click', function() {
            document.getElementById('step5').style.display = 'none';
            document.getElementById('step3').style.display = 'block';
            document.getElementById('step3').scrollIntoView({ behavior: 'smooth' });
        });
    }

    function formatarDataBrasileira(data) {
        const [ano, mes, dia] = data.split('-');
        return `${dia}/${mes}/${ano}`;
    }

    function protegerEmail(email) {
        const [usuario, dominio] = email.split('@');
        return `${usuario[0]}*****@${dominio}`;
    }

    function protegerTelefone(telefone) {
        return `(**) *****-${telefone.slice(-4)}`;
    }

    const verifyCPFButton = document.getElementById('verifyCPF');
    if (verifyCPFButton) {
        verifyCPFButton.addEventListener('click', function() {
            const cpf = document.getElementById('cpf').value;
            fetch(`/api/verificar_cpf/?cpf=${cpf}`)
                .then(response => response.json())
                .then(data => {
                    if (data.valid) {
                        fetch(`/clientes/verificar/?cpf=${cpf}`)
                            .then(response => response.json())
                            .then(data => {
                                if (data.error) {
                                    document.getElementById("step3").style.display = 'none';
                                    document.getElementById("step5").style.display = 'block';
                                    document.getElementById('step5').scrollIntoView({ behavior: 'smooth' });
                                } else {
                                    document.getElementById('confirm_nome_completo').innerText = data.nome_completo;
                                    document.getElementById('confirm_data_nascimento').innerText = formatarDataBrasileira(data.data_nascimento);
                                    document.getElementById('confirm_email').innerText = protegerEmail(data.email);
                                    document.getElementById('confirm_telefone').innerText = protegerTelefone(data.telefone);
                                    document.getElementById('hidden_cliente_id').value = data.cliente_id;
                                    document.getElementById("step3").style.display = 'none';
                                    document.getElementById("step4").style.display = 'block';
                                    document.getElementById('step4').scrollIntoView({ behavior: 'smooth' });
                                }
                            })
                            .catch(error => {
                                console.error('Erro ao verificar o CPF:', error);
                            });
                    } else {
                        mostrarAlertaCPF('CPF inválido. Por favor, verifique e tente novamente.');
                    }
                })
                .catch(error => {
                    console.error('Erro ao verificar o CPF:', error);
                });
        });
    }

    const calcularFreteButton = document.querySelector(".calcular-frete");
    if (calcularFreteButton) {
        calcularFreteButton.addEventListener('click', function() {
            const equipId = this.getAttribute('data-equip-id');
            const cep = document.getElementById("cep").value;
            const loadingSpinner = document.getElementById("loading");
            loadingSpinner.style.display = 'block';
            fetch(`/frete/calcular-entrega/?cep=${cep}`)
                .then(response => response.json())
                .then(data => {
                    loadingSpinner.style.display = 'none';
                    if (data.error) {
                        mostrarAlertaStep2(data.error);
                        return;
                    }
                    const valorFrete = data.valor_frete.toFixed(2);
                    const metadeFrete = (valorFrete / 2).toFixed(2);
                    document.getElementById("frete_total_valor").innerText = valorFrete;
                    document.getElementById("entrega_valor").innerText = metadeFrete;
                    document.getElementById("coleta_valor").innerText = metadeFrete;
                    document.getElementById("hidden_frete_total").value = valorFrete;
                    document.getElementById("hidden_frete_entrega").value = metadeFrete;
                    document.getElementById("hidden_frete_coleta").value = metadeFrete;

                    document.getElementById("logradouro").innerText = data.logradouro;
                    document.getElementById("hidden_logradouro").value = data.logradouro;

                    document.getElementById("frete-info").style.display = 'block';

                    valorFreteSelecionado = parseFloat(valorFrete);
                    atualizarSelecao();
                })
                .catch(error => {
                    loadingSpinner.style.display = 'none';
                    console.error('Erro ao calcular o frete:', error);
                });
        });
    }

    const freteOpcoes = document.querySelectorAll('input[name="frete_opcao"]');
    freteOpcoes.forEach(radio => {
        radio.addEventListener('change', function() {
            valorFreteSelecionado = parseFloat(this.nextElementSibling.querySelector('span').innerText);
            tipoFreteSelecionado = this.nextElementSibling.previousElementSibling.textContent;
            document.getElementById('hidden_opcao_frete').value = this.value;
            atualizarSelecao();
        });
    });

    const numeroInput = document.getElementById('numero');
    if (numeroInput) {
        numeroInput.addEventListener('input', function() {
            document.getElementById('hidden_numero').value = this.value;
        });
    }

    const complementoInput = document.getElementById('complemento');
    if (complementoInput) {
        complementoInput.addEventListener('input', function() {
            document.getElementById('hidden_complemento').value = this.value;
        });
    }

    function previewImage(input, previewContainer) {
        const file = input.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = previewContainer.querySelector('img');
                img.src = e.target.result;
                previewContainer.style.display = 'flex';
            }
            reader.readAsDataURL(file);
        } else {
            previewContainer.style.display = 'none';
        }
    }

    document.getElementById('documento_oficial').addEventListener('change', function() {
        previewImage(this, document.getElementById('documento_oficial_preview'));
    });

    document.getElementById('comprovante_residencia').addEventListener('change', function() {
        previewImage(this, document.getElementById('comprovante_residencia_preview'));
    });


    carregarDatasIndisponiveis();
});

const backToStep2Button = document.getElementById('backToStep2');
if (backToStep2Button) {
    backToStep2Button.addEventListener('click', function() {
        document.getElementById('step3').style.display = 'none';
        document.getElementById('step2').style.display = 'block';
        document.getElementById('step2').scrollIntoView({ behavior: 'smooth' });
    });
}
