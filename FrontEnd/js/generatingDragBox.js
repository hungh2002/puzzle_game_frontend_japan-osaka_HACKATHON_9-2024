import { shuffleImage } from "./shuffleImage";
import { user } from "./user";

const generatingDragBox = async (rows, columns) => {
  const drag = document.getElementById("drag-aria");

  await user.setImagesList();
  const imagesList = user.imagesList;

  let imageIndex;
  // <div class="drag-box"><img class="image" id="block1" draggable="true" src="images/1.jpg"></div>
  for (let i = 1; i <= rows * columns; i++) {
    imageIndex = i - 1;

    const dragBox = document.createElement("div");
    dragBox.classList.add("drag-box");
    dragBox.id = `box${i}`;

    let image = document.createElement("img");
    image.classList.add("image");
    image.id = `block${i}`;
    image.draggable = true;
    image.src = imagesList[imageIndex];
    image.ondragstart = (event) => {
      event.dataTransfer.setData("text", event.target.id);
    };
    dragBox.appendChild(image);
    drag.appendChild(dragBox);
  }

  // Shuffling images
  shuffleImage();
};

export { generatingDragBox };
