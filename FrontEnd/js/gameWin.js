import { axios } from "./axios";

const gameWin = async () => {
  const board = document.getElementById("board");
  const questionForm = document.createElement("question-form");
  questionForm.id = "question-form";

  const fieldset = document.createElement("fieldset");
  const question = document.createElement("legend");
  question.id = "question";

  const submitButton = document.createElement("button");
  submitButton.type = "submit";
  submitButton.textContent = "Send";

  //   const response = await axios.get("/q_and_a");
  //   const data = response.data;
  const data = {
    question: "問題文",
    answer: [
      "回答の選択肢_1",
      "回答の選択肢_2",
      "回答の選択肢_3",
      "回答の選択肢_4",
    ],
  };
  question.textContent = data.question;
  fieldset.appendChild(question);

  for (let i = 0; i < data.answer.length; i++) {
    const br = document.createElement("br");
    const answer = document.createElement("input");
    answer.classList.add("answer");
    answer.type = "radio";
    answer.name = "answer";
    answer.value = data.answer[i];
    answer.id = data.answer[i];

    const label = document.createElement("label");
    label.htmlFor = data.answer[i];
    label.textContent = data.answer[i];

    fieldset.appendChild(answer);
    fieldset.appendChild(label);
    fieldset.appendChild(br);
  }

  questionForm.appendChild(fieldset);
  questionForm.appendChild(submitButton);
  board.appendChild(questionForm);

  questionForm.onsubmit = (event) => {
    event.preventDefault();
    // const data = new FormData(e.target);
    // axios.get(`/send_answer/${"ユーザー名"}/${data.get("answer")}`);

    document.getElementById("question-form").remove();
  };
};

export { gameWin };
