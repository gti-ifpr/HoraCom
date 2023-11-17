//as funções de Java Script são conforto para o usuario na hora da visualização do front//
function validarFormulario() {/**PARA CADASTRO */
var nome = document.getElementById("nome").value;
var cpf = document.getElementById("cpf").value;
var email = document.getElementById("email").value;
var senha = document.getElementById("senha").value;
var confirmaSenha = document.getElementById("confirma-senha").value;

if (nome === "" || cpf === "" || email === "" || senha === "" || confirmaSenha === "") {
  alert("Por favor, preencha todos os campos.");
  return false;
}

if (senha !== confirmaSenha) {
  alert("As senhas não coincidem. Por favor, verifique.");
  return false;
}

alert("Cadastro realizado com sucesso!\nNome: " + nome + "\nCPF: " + cpf + "\nEmail: " + email);
return true;
}
function validatedata() {
  // Obtenha os valores dos campos
  var emailCpf = document.getElementById('email-cpf').value;
  var senha = document.getElementById('senha').value;

  // Realize a validação (exemplo: garantir que os campos não estejam vazios)
  if (emailCpf === '' || senha === '') {
      // Exiba uma mensagem de erro (isso pode ser ajustado conforme necessário)
      alert('Por favor, preencha todos os campos.');
      
      // Impede o envio do formulário
      return false;
  }

  // Se a validação for bem-sucedida, permita o envio do formulário
  return true;
}


const GRUPOS = {//**PARA ANEXAR */
G1: 'g1',
G2: 'g2'
};

function showOptions() {//**PARA SELECIONAR GRUPO */
const grupoPrincipal = document.getElementById('grupoPrincipal').value;
const gruposOptions = document.querySelectorAll('.grupo-options');

gruposOptions.forEach(option => option.style.display = 'none');

const grupoOption = document.getElementById(`${grupoPrincipal}Options`);
if (grupoOption) {
  grupoOption.style.display = 'block';
  updateDescription(`${grupoPrincipal === GRUPOS.G1 ? 'Grupo 1' : 'Grupo 2'}: ...`);
  document.getElementById('horasDesejadas').disabled = grupoPrincipal === GRUPOS.G1;
  onSubGrupoChange(grupoPrincipal);
} else {
  updateDescription('');
  document.getElementById('horasDesejadas').disabled = true;
  
}
}

function onSubGrupoChange(grupo) {//**PARA SELECIONAR OPÇÃO */
  const subGrupo = grupo === GRUPOS.G1 ? document.getElementById('subGrupoG1') : document.getElementById('subGrupoG2');
  const maximoHorasSpan = document.getElementById('maximoHoras');
  const opcao = subGrupo.value;
  
  // Atualiza o span com o máximo de horas
  maximoHorasSpan.innerText = obterLimiteHoras(grupo, opcao) + ' horas';
}

function obterLimiteHoras(grupo, opcao) {//*Para aparecer as definições de limItes de horas  */
const limites = {
  g1: {
    opcao1: 60,
    opcao2: 60,
    opcao3: 80,
    opcao4: 20,
    opcao5: 20,
    opcao6: 80,
    opcao7: 40,
    opcao8: 60,
    opcao9: 60,
    opcao10: 80,
    opcao11: 80,
    opcao12: 80,
    opcao13: 80,
    opcao14: 80,
    opcao15: 60,
    opcao16: 60,
    opcao17: 60,
    opcao18: 60,
    opcao19: 60,
    
  },
  g2: {
    opcao1: 120,
    opcao2: 120,
    opcao3: 60,
    opcao4: 60,
    
  }
};

return limites[grupo] && limites[grupo][opcao] ? limites[grupo][opcao] : 0;
}

function verificarLimiteHoras() {//Para retornar o limite de horas por opção//
  const grupoPrincipal = document.getElementById('grupoPrincipal').value;
  const subGrupo = grupoPrincipal === GRUPOS.G1 ? document.getElementById('subGrupoG1') : document.getElementById('subGrupoG2');
  const horasDesejadas = parseInt(document.getElementById('horasDesejadas').value, 10);
  const limiteHoras = obterLimiteHoras(grupoPrincipal, subGrupo.value);

  if (horasDesejadas > limiteHoras) {
    alert(`Você excedeu o limite de horas para essa opção. Limite: ${limiteHoras} horas.`);
    return false;
  } else {
    const maximoHorasSpan = document.getElementById('maximoHoras');
    maximoHorasSpan.innerText = `Máximo de horas aceitas para essa opção: ${limiteHoras} horas`;

    // Adicione o arquivo ao formulário para envio
    const form = document.querySelector('form');
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.name = 'arquivo';
    fileInput.files = droppedFile ? [droppedFile] : null;
    form.appendChild(fileInput);

    return true;
  }
}

function calculateReducedHours() {//**CALCULA AS HORAS COM REDUTORES */
  const grupoPrincipal = document.getElementById('grupoPrincipal').value;
  const subGrupo = grupoPrincipal === GRUPOS.G1 ? document.getElementById('subGrupoG1') : document.getElementById('subGrupoG2');
  const horasDesejadas = parseInt(document.getElementById('horasDesejadas').value, 10);

  const redutores = {
    g1: {
      opcao1: 0.25,
      opcao5: 0.5,
      opcao9: 0.5,
      opcao16: 0.5
    },
    g2: {
      opcao1: 0.25,
      opcao2: 0.25
    }
  };

  const horasReduzidasElement = document.getElementById('horasReduzidas');

  if (redutores[grupoPrincipal] && redutores[grupoPrincipal][subGrupo.value]) {
    const redutor = redutores[grupoPrincipal][subGrupo.value];
    const horasReduzidas = horasDesejadas * redutor;
    horasReduzidasElement.innerText = `Esta opção tem redutor em seu cálculo,quantidade de horas aceitas: ${horasReduzidas} horas`;
    horasReduzidasElement.style.display = 'block';  // Exibe o elemento
  } else {
    horasReduzidasElement.style.display = 'none';  // Oculta o elemento se não houver redutor
  }
}
function handleDragOver(event) {//Para soltar arquivo//
  event.preventDefault();
  const dragInfo = document.getElementById('dragInfo');
  dragInfo.innerText = 'Solte o arquivo a ser carregado aqui...';
}

function handleDrop(event) {//faz  parte do soltar arquivo também//
  event.preventDefault();
  const dragInfo = document.getElementById('dragInfo');
  dragInfo.innerText = 'Arquivo solto!';

  const droppedFile = event.dataTransfer.files[0];
  console.log('Arquivo solto:', droppedFile);
  
  const fileList = document.getElementById('fileList');
  fileList.innerHTML = '';  // Limpa o conteúdo anterior

  // Adiciona o arquivo solto à lista
  const listItem = document.createElement('li');
  listItem.textContent = `Arquivo selecionado: ${droppedFile.name}`;
  fileList.appendChild(listItem);
}


function displaySelectedFileName() {//Mostra o arquivo selecionado logo abaixo do escolher//
  const input = document.getElementById('arquivo');
  const arquivoSelecionado = document.getElementById('arquivoSelecionado');

  arquivoSelecionado.innerHTML = `Arquivo selecionado: ${input.files[0].name}`;
}
function inserirCertificado() {//Insere certificados//
  // Obter os valores necessários do formulário
  const id_aluno = 1;  // Substitua pelo valor correto
  const grupo = document.getElementById("grupoPrincipal").value;
  const opcao = document.getElementById("subGrupo" + grupo.charAt(1)).value;  // Obtém o valor da opção do grupo selecionado
  const quantidade_horas = parseFloat(document.getElementById("horasDesejadas").value);

  // Chamar a função de inserção
  inserir_certificado(id_aluno, grupo, opcao, quantidade_horas);

  // Exibir a mensagem de sucesso
  const mensagemDiv = document.getElementById("mensagem");
  mensagemDiv.innerText = "Certificado inserido com sucesso!";
}


document.addEventListener("DOMContentLoaded", function () {
  // Verifica se o usuário está autenticado antes de fazer a solicitação
  if (usuarioAutenticado()) {
    obterRegistros();
  }
});

function usuarioAutenticado() {
  // Sua lógica de verificação de autenticação aqui
  // Retorne true se autenticado, false caso contrário
  return true; // ou implemente sua lógica real aqui
}

function obterRegistros() {
  fetch("/obter_registros_certificados")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Erro ao obter registros");
      }
      return response.json();
    })
    .then((data) => {
      // Lógica para manipular os dados obtidos e atualizar a interface
      exibirRegistrosNaTela(data.registros);
    })
    .catch((error) => {
      console.error(error);
    });
}

function exibirRegistrosNaTela(registros) {
  const registrosDiv = document.getElementById('registros');

  registros.forEach((registro, index) => {
    const item = document.createElement('div');
    item.classList.add('registro-item');
    item.innerHTML = `<strong>ID Aluno:</strong> ${registro.id_aluno}, <strong>Grupo:</strong> ${registro.grupo}, <strong>Opção:</strong> ${registro.opcao}, <strong>Horas:</strong> ${registro.quantidade_horas}`;
    registrosDiv.appendChild(item);
  });
}





