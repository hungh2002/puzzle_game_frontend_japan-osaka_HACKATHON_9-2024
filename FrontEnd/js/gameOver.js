import { ranking } from "./ranking";

const gameOver = () => {
  const board = document.getElementById("board");
  board.remove();
  ranking();
};
export { gameOver };
