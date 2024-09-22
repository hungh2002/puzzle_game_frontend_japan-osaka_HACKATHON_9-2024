import { gameOver } from "./js/gameOver";
import { generatingCSSGrid } from "./js/generatingCSSGrid";
import { generatingDragBox } from "./js/generatingDragBox";
import { generatingDropBox } from "./js/generatingDropBox";
import { timer } from "./js/timer";
import { user } from "./js/user";
import "./style.css";

const rows = 4;
const columns = 4;

const playingButton = document.getElementById("playing-button");
playingButton.onclick = () => {
  user.setIsPlaying(true);
};

setInterval(async () => {
  user.setUsername();
  if (user.isPlaying) {
    await user.setTime();
    timer();

    setTimeout(async () => {
      const title = document.getElementById("title");
      title.style.display = "none";
      const userNameForm = document.getElementById("username-form");
      userNameForm.style.display = "none";

      generatingCSSGrid(rows, columns);
      generatingDragBox(rows, columns);

      generatingDropBox(rows, columns);
    }, user.time.startTime);

    setTimeout(() => {
      gameOver();
    }, user.time.finishTime);

    user.setIsPlaying(false);
  }
}, 1000);
