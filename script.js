// cadastro
function validarFormulario() {
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

