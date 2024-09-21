import { getImagesList } from "./getImage";

const generatingDragBox = (rows, columns) => {
  const drag = document.getElementById("drag-aria");

  // const imagesList = getImagesList();

  // <div class="drag-box"><img class="image" id="block1" draggable="true" src="images/1.jpg"></div>
  for (let i = 1; i <= rows * columns; i++) {
    const dragBox = document.createElement("div");
    dragBox.classList.add("drag-box");
    dragBox.id = `box${i}`;

    let image = document.createElement("img");
    image.classList.add("image");
    image.id = `block${i}`;
    image.draggable = true;
    image.src = `images/${i}.jpg`;
    image.ondragstart = (event) => {
      event.dataTransfer.setData("text", event.target.id);
    };
    dragBox.appendChild(image);
    drag.appendChild(dragBox);
  }
};

export { generatingDragBox };
