import { checkGameOver } from "./checkGameOver";

const generatingDropBox = (rows, columns) => {
  const drop = document.getElementById("drop-aria");

  // <div class="drop-box"></div>
  for (let i = 1; i <= rows * columns; i++) {
    const dropBox = document.createElement("div");
    dropBox.classList.add("drop-box");

    // Adding event listener
    dropBox.ondragover = (event) => {
      event.preventDefault();
    };
    dropBox.ondrop = (event) => {
      event.preventDefault();
      let id = event.dataTransfer.getData("text");
      if (
        event.target.parentElement.id != "" &&
        event.target.parentElement.id != undefined &&
        event.target.children[0] == undefined
      ) {
        //<img class="image" id="block1" draggable="true" src="images/1.jpg">
        event.target.appendChild(document.getElementById(id));

        checkGameOver();
      }
    };

    drop.appendChild(dropBox);
  }
};

export { generatingDropBox };
