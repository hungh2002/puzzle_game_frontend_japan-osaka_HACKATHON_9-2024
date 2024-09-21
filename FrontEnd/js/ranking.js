import { axios } from "./axios";

const ranking = async () => {
  const response = await axios.get("/ranking");
  const data = response.data;

  const app = document.getElementById("app");
  const ranking = document.createElement("ranking");
  ranking.id = "ranking";
  const ul = document.createElement("ul");

  let index;
  for (let i = 0; i < data.ranking.length; i++) {
    const rank = document.createElement("li");
    index = i + 1;
    rank.textContent = `位: ${data.ranking[i]}`;

    ul.appendChild(rank);
  }

  ranking.appendChild(ul);
  app.appendChild(ranking);
};

export { ranking };
