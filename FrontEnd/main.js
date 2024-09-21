import { checkGameOver } from "./js/checkGameOver";
import { gameOver } from "./js/gameOver";
import { generatingCSSGrid } from "./js/generatingCSSGrid";
import { generatingDragBox } from "./js/generatingDragBox";
import { generatingDropBox } from "./js/generatingDropBox";
import { ranking } from "./js/ranking";
import { shuffleImage } from "./js/shuffleImage";
import { endGame, getTime, isPlaying, playing } from "./js/timer";
import "./style.css";

const rows = 3;
const columns = 3;

const playingButton = document.getElementById("playing-button");
playingButton.onclick = () => {
  playing();
};

setInterval(() => {
  if (isPlaying) {
    let time = getTime();
    let currentTime = new Date();

    setTimeout(() => {
      const title = document.getElementById("title");
      title.style.display = "none";

      generatingCSSGrid(rows, columns);
      generatingDragBox(rows, columns);

      // Shuffling images
      shuffleImage();

      generatingDropBox(rows, columns);
    }, (time.start.summary - (currentTime.getHours() * 60 + currentTime.getMinutes())) * 60 * 1000 - 30000);

    setTimeout(() => {
      gameOver();
    }, (time.finish.summary - (currentTime.getHours() * 60 + currentTime.getMinutes())) * 60 * 1000 - 30000);

    endGame();
  }
}, 1000);
