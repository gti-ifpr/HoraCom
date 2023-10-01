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

function atualizarHoras() {
const horasDesejadas = document.getElementById('horasDesejadas').value;
const maximoHorasSpan = document.getElementById('maximoHoras');
maximoHorasSpan.innerText = horasDesejadas ? `Horas desejadas: ${horasDesejadas}` : '';
}

function verificarLimiteHoras() {
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

function calculateReducedHours() {
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

function goBack() {
// Implemente a lógica para voltar
}
let droppedFile = null;

function handleDrop(event) {
  event.preventDefault();
  const dragInfo = document.getElementById('dragInfo');
  dragInfo.innerText = 'Arquivo solto!';

  droppedFile = event.dataTransfer.files[0];
  console.log('Arquivo solto:', droppedFile);
}

function handleDragLeave(event) {
  event.preventDefault();
  const dragInfo = document.getElementById('dragInfo');
  dragInfo.innerText = 'Solte o arquivo a ser carregado aqui...';
}

const registros = [];

function adicionarRegistro(grupo, opcao, horas, data) {
  const registro = {
    grupo,
    opcao,
    horas,
    data
  };
  registros.push(registro);
}

function verificarLimiteHoras() {
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

    const grupo = grupoPrincipal === GRUPOS.G1 ? 'Grupo 1' : 'Grupo 2';
    const opcao = subGrupo.options[subGrupo.selectedIndex].text;
    const data = new Date().toLocaleDateString();

    adicionarRegistro(grupo, opcao, horasDesejadas, data);
    exibirRegistros();

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
function exibirRegistros() {
  const registrosDiv = document.getElementById('registros');
  registrosDiv.innerHTML = '';  // Limpa o conteúdo atual

  registros.forEach((registro, index) => {
    const item = document.createElement('div');
    item.classList.add('registro-item');
    item.innerHTML = `<strong>Grupo:</strong> ${registro.grupo}, <strong>Opção:</strong> ${registro.opcao}, <strong>Horas:</strong> ${registro.horas}, <strong>Data:</strong> ${registro.data} <button onclick="removerRegistro(${index})">Remover</button>`;
    registrosDiv.appendChild(item);
  });
}



function removerRegistro(index) {
  registros.splice(index, 1);
  exibirRegistros();
}


  event.preventDefault();
  const dragInfo = document.getElementById('dragInfo');
  dragInfo.innerText = 'Arquivo solto!';

  // Aqui você pode implementar o que deseja fazer com o arquivo que foi solto
  const file = event.dataTransfer.files[0];
  console.log('Arquivo solto:', file);




