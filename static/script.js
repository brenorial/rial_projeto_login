const API_URL = "http://localhost:5000";
let modo = "cadastrar"; // ou "editar"
let processos = [];
let indiceAtual = 0;

function mostrarSecao(id) {
  const secoes = document.querySelectorAll(".secao");
  secoes.forEach((secao) => (secao.style.display = "none"));
  const secaoAtiva = document.getElementById(id);
  if (secaoAtiva) secaoAtiva.style.display = "block";
}

window.onload = () => mostrarSecao("cadastro");

document
  .getElementById("form-processo")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    salvarProcesso();
  });

async function salvarProcesso() {
  const payload = {
    numero: document.getElementById("numero").value,
    descricao: document.getElementById("descricao").value,
    data_inicio: document.getElementById("data_inicio").value,
    data_fim: document.getElementById("data_fim").value,
  };

  console.log("Enviando para backend:", payload); // debug

  const formData = new URLSearchParams();
  formData.append("numero", payload.numero);
  formData.append("descricao", payload.descricao);
  formData.append("data_inicio", payload.data_inicio);
  formData.append("data_fim", payload.data_fim);

  const res = await fetch(`${API_URL}/processo`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData.toString(),
  });

  let data;
  try {
    data = await res.json();
  } catch (e) {
    data = { message: "Erro desconhecido no servidor." };
  }

  if (res.ok) {
    alert("Cadastrado com sucesso!");
    listarProcessos();
    document.getElementById("form-processo").reset();
  } else {
    console.error("Erro ao cadastrar:", data);
    if (Array.isArray(data)) {
      alert(
        "Erro ao cadastrar processo:\n" +
          data.map((e) => `${e.loc.join(".")} - ${e.msg}`).join("\n")
      );
    } else {
      alert(
        "Erro ao cadastrar processo: " + (data.message || "Erro desconhecido.")
      );
    }
  }
}

function listarProcessos() {
  fetch(`${API_URL}/processos`)
    .then((res) => res.json())
    .then((data) => {
      processos = data.processos;
      indiceAtual = 0;
      exibirProcesso();
    })
    .catch((err) => {
      console.error("Erro ao listar processos:", err);
      document.getElementById("processo-visualizacao").textContent =
        "Erro ao buscar processos.";
    });
}

document.addEventListener("DOMContentLoaded", listarProcessos);

function mostrarProximo() {
  if (indiceAtual < processos.length - 1) {
    indiceAtual++;
    exibirProcesso();
  }
}

function mostrarAnterior() {
  if (indiceAtual > 0) {
    indiceAtual--;
    exibirProcesso();
  }
}

function deletarProcesso(numero) {
  if (!confirm(`Tem certeza que deseja deletar o processo "${numero}"?`))
    return;

  fetch(`${API_URL}/del_processo?numero=${encodeURIComponent(numero)}`, {
    method: "DELETE",
  })
    .then((res) => res.json())
    .then((data) => {
      alert("Processo deletado com sucesso.");
      listarProcessos();
    })
    .catch(() => {
      alert("Erro ao deletar o processo.");
    });
}
function exibirProcesso() {
  const container = document.getElementById("processo-visualizacao");

  if (processos.length === 0) {
    container.innerHTML = "Nenhum processo encontrado.";
    return;
  }

  const proc = processos[indiceAtual];
  container.innerHTML = `
    <h3>Processo ${proc.numero}</h3>
    <p><strong>Descrição:</strong> ${proc.descricao}</p>
    <p><strong>Data Início:</strong> ${new Date(
      proc.data_inicio
    ).toLocaleDateString()}</p>
    <p><strong>Data Fim:</strong> ${new Date(
      proc.data_fim
    ).toLocaleDateString()}</p>
    ${
      proc.data_insercao
        ? `<p><strong>Inserido em:</strong> ${new Date(
            proc.data_insercao
          ).toLocaleString()}</p>`
        : ""
    }
    <p><em>${indiceAtual + 1} de ${processos.length}</em></p>
    <button onclick="carregarParaEdicao()">Editar</button>
    <button onclick="deletarProcesso('${proc.numero}')">Deletar</button>
  `;
}
