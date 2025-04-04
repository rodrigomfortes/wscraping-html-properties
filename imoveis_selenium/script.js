document.addEventListener("DOMContentLoaded", function() {
  fetch("http://127.0.0.1:8000/imoveis/")
      .then(response => response.json())
      .then(data => {
          let tabela = document.getElementById("tabela-imoveis");
          tabela.innerHTML = "";  // Limpa a tabela antes de adicionar os dados

          data.forEach(imovel => {
              let row = `<tr>
                  <td>${imovel.endereco}</td>
                  <td>${imovel.quartos}</td>
                  <td>${imovel.banheiros}</td>
                  <td>${imovel.vagas}</td>
                  <td>${imovel.area}</td>
                  <td>${imovel.descricao.substring(0, 50)}...</td>
                  <td><a href="${imovel.link}" target="_blank">Ver Imóvel</a></td>
              </tr>`;
              tabela.innerHTML += row;
          });
      })
      .catch(error => {
          console.error("Erro ao carregar imóveis:", error);
          document.getElementById("tabela-imoveis").innerHTML = 
              `<tr><td colspan="7" style="text-align:center;color:red;">Erro ao carregar imóveis!</td></tr>`;
      });
});
