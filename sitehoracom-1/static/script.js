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

function showOptions() {
const grupoPrincipal = document.getElementById('grupoPrincipal').value;
const gruposOptions = document.querySelectorAll('.grupo-options');

gruposOptions.forEach(option => option.style.display = 'none');

const grupoOption = document.getElementById(`${grupoPrincipal}Options`);
if (grupoOption) {
  grupoOption.style.display = 'block';
  updateDescription(`${grupoPrincipal === GRUPOS.G1 ? 'Grupo 1' : 'Grupo 2'}: ...`);
  document.getElementById('horasDesejadas').disabled = grupoPrincipal === GRUPOS.G1;
} else {
  updateDescription('');
  document.getElementById('horasDesejadas').disabled = true;
}
}

function onSubGrupoChange(grupo) {
const subGrupo = grupo === GRUPOS.G1 ? document.getElementById('subGrupoG1') : document.getElementById('subGrupoG2');
const maximoHorasSpan = document.getElementById('maximoHoras');
const horas = obterLimiteHoras(grupo, subGrupo.value);
maximoHorasSpan.innerText = `Máximo de horas aceitas para a opção selecionada: ${horas} horas`;
}

function obterLimiteHoras(grupo, opcao) {//*Para aparecer as definições de limetes de horas  */
const limites = {
  g1: {
    opcao1: 60,
    opcao2: 60,
    opcao3: 120,
    opcao4: 120,
    opcao5: 120,
    opcao6: 120,
    opcao7: 120,
    opcao8: 120,
    opcao9: 120,
    opcao10: 120,
    opcao11: 120,
    opcao12: 120,
    opcao13: 120,
    opcao14: 120,
    opcao15: 120,
    opcao16: 120,
    opcao17: 120,
    opcao18: 120,
    opcao19: 120,
    // Colocar o valor do maximo de horas 
  },
  g2: {
    opcao1: 120,
    opcao2: 120,
    opcao3: 120,
    opcao4: 120,
    
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
  return false;  // Impede o envio do formulário
} else {
  alert('Horas dentro do limite. Enviando...');  // Substitua por sua lógica de envio
  return true;  // Permite o envio do formulário
}
}




function calculateReducedHours() {//CALCULA O REDUTOR De HORAS//
const grupoPrincipal = document.getElementById('grupoPrincipal').value;
const subGrupo = grupoPrincipal === GRUPOS.G1 ? document.getElementById('subGrupoG1') : document.getElementById('subGrupoG2');
const horasDesejadas = parseInt(document.getElementById('horasDesejadas').value, 10);
const limiteHoras = obterLimiteHoras(grupoPrincipal, subGrupo.value);
const REDUCER_FACTOR_G1_OP1 = 0.25;
let horasReduzidas = 0;

if (grupoPrincipal === GRUPOS.G1 && subGrupo.value === 'opcao1') {
  horasReduzidas = horasDesejadas * REDUCER_FACTOR_G1_OP1;
}

document.getElementById('horasReduzidas').innerText = `Horas reduzidas: ${horasReduzidas}`;
}

function goBack() {
// Implemente a lógica para voltar
}

