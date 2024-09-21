import { axios } from "./axios";
import { user } from "./user";

const gameWin = () => {
  const questionForm = document.getElementById("question-form");
  questionForm.style.display = "block";

  const fieldset = questionForm.getElementsByTagName("fieldset")[0];
  const question = fieldset.getElementsByTagName("legend")[0];

  const submitButton = questionForm.getElementsByTagName("button")[0];

  const data = user.questionAndAnswer;

  question.textContent = data.question;

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

  questionForm.onsubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.target);
    axios.post(`/send_answer`, {
      user_name: user.userName ? user.userName : "anonymous",
      choice_answer: data.answer,
    });

    document.getElementById("question-form").remove();
  };

  questionForm.appendChild(submitButton);
};

export { gameWin };
