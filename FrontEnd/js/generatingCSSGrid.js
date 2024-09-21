const generatingCSSGrid = (rows, columns) => {
  const app = document.getElementById("app");

  const board = document.createElement("div");
  board.id = "board";

  const drag = document.createElement("div");
  drag.id = "drag-aria";
  // Generating css grid drag element
  drag.style.display = "grid";
  //// Generating rows
  drag.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
  //// Generating columns
  drag.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;

  const drop = document.createElement("div");
  drop.id = "drop-aria";
  // Generating css grid drag element
  //// Generating rows
  drop.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
  //// Generating columns
  drop.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;

  board.appendChild(drag);
  board.appendChild(drop);
  app.appendChild(board);
};

export { generatingCSSGrid };
