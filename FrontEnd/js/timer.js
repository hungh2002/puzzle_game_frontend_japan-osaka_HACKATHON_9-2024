let isPlaying = false;

const playing = () => {
  isPlaying = true;
};

const endGame = () => {
  isPlaying = false;
};

const getTime = () => {
  //axios
  const data = {
    start: { hour: new Date().getHours(), minute: new Date().getMinutes() + 1 },
    finish: {
      hour: new Date().getHours(),
      minute: new Date().getMinutes() + 2,
    },
  };

  data.start.summary = data.start.hour * 60 + data.start.minute;
  data.finish.summary = data.finish.hour * 60 + data.finish.minute;

  return data;
};

export { isPlaying, getTime, playing, endGame };
