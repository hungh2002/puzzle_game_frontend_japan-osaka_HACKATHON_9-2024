const generatingCSSGrid = (rows, columns) => {
  const board = document.getElementById("board");
  board.style.display = "flex";

  const drag = document.getElementById("drag-aria");
  // Generating css grid drag element
  //// Generating rows
  drag.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
  //// Generating columns
  drag.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;

  const drop = document.getElementById("drop-aria");
  // Generating css grid drag element
  //// Generating rows
  drop.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
  //// Generating columns
  drop.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;
};

export { generatingCSSGrid };
