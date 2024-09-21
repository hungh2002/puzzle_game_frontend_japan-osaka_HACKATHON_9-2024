const shuffleImage = () => {
  let parent = document.getElementById("drag-aria");
  let frag = document.createDocumentFragment();
  for (let i = 0; i < parent.children.length; i++) {
    frag.appendChild(
      parent.children[Math.floor(Math.random() * parent.children.length)]
    );
  }
  parent.appendChild(frag);
};

export { shuffleImage };
