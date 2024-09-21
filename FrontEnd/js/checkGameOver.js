import { axios } from "./axios";
import { gameWin } from "./gameWin";

const checkGameOver = () => {
  let win = true;
  const dropBox = document.getElementsByClassName("drop-box");

  // Check win condition by comparing id of each image in drop-box with their index in array
  let index = 0;
  for (let i = 0; i < dropBox.length; i++) {
    const image = dropBox[i].getElementsByClassName("image")[0];
    if (image != undefined) {
      index = i + 1;
      if (image.id != `block${index}`) {
        win = false;
        break;
      }
    } else win = false;
  }

  if (win) {
    gameWin();
  }
};

export { checkGameOver };
