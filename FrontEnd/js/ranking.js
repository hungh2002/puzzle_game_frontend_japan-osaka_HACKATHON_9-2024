import { axios } from "./axios";

const ranking = async () => {
  const response = await axios.get("/ranking");
  const data = response.data;

  const ranking = document.getElementById("ranking");
  ranking.style.display = "flex";
  ranking.style.justifyContent = "center";
  ranking.style.alignItems = "center";
  ranking.style.flexDirection = "column";

  const ul = ranking.getElementsByTagName("ul")[0];

  let index;
  let li = "";
  for (let i = 0; i < data.ranking.length; i++) {
    index = i + 1;
    li = li + `<li>位: ${data.ranking[i]}</li>`;
  }
  ul.innerHTML = li;
};

export { ranking };
