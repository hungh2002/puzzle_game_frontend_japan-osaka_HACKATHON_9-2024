import { axios } from "./axios";
import { ranking } from "./ranking";
import { user } from "./user";

let interval;
let countDown = 0;

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
    if (user.userName !== undefined) {
      axios.get(`/send_answer/${data.get("answer")}/${user.userName}`);
    } else {
      axios.get(
        `/send_answer/${data.get("answer")}/anonymous_${new Date.now()}`
      );
    }

    document.getElementById("question-form").remove();

    interval = setInterval(() => {
      if (countDown <= user.time.finishTime * 1000) {
        ranking();
        countDown = countDown + 1;
      } else {
        countDown = 0;
        clearInterval(interval);
      }
    }, 1000);
  };

  questionForm.appendChild(submitButton);
};

export { gameWin };
