import { imagesListHandle } from "./handle/imagesListHandle";
import { timeHandle } from "./handle/timeHandle";

class User {
  constructor(userName, time, imagesList, questionAndAnswer) {
    this.userName = userName;
    this.time = time;
    this.isPlaying = false;
    this.imagesList = imagesList;
    this.questionAndAnswer = questionAndAnswer;
  }

  setUsername() {
    const userNameForm = document.getElementById("username-form");

    userNameForm.onsubmit = (e) => {
      e.preventDefault();

      const data = new FormData(e.target);
      this.userName = data.get("userName");
    };
  }

  async setTime() {
    this.time = await timeHandle();
  }

  setIsPlaying(isPlaying) {
    this.isPlaying = isPlaying;
  }

  async setImagesList() {
    this.imagesList = await imagesListHandle();
  }

  setQuestionAndAnswer(questionAndAnswer) {
    this.questionAndAnswer = questionAndAnswer;
  }
}

const user = new User();

export { user };
