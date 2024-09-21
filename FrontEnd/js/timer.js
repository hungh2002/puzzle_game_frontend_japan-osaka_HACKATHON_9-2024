import { user } from "./user";

let timerStatus = true;

const timer = () => {
  if (timerStatus) {
    let hourStart = user.time.detail.start_time.hour;
    let minuteStart = user.time.detail.start_time.minute;
    let hourFinish = user.time.detail.finish_time.hour;
    let minuteFinish = user.time.detail.finish_time.minute;
    let playingTime = user.time.finishTime - user.time.startTime;

    const timer = document.getElementById("timer");
    const br = document.createElement("br");
    timer.style.display = "inline-block";

    //   const elapsedTime = document.createElement("div");
    const timeStatus = document.createElement("div");
    timeStatus.textContent = `Start: ${hourStart}:${minuteStart} ~ ${hourFinish}:${minuteFinish}`;
    //   elapsedTime.textContent = `Time elapsed: ${playingTime * 1000}`;

    //   timer.appendChild(elapsedTime);
    timer.appendChild(br);
    timer.appendChild(timeStatus);

    const interval = setInterval(() => {
      if (playingTime == 0) {
        clearInterval(interval);
      }

      // elapsedTime.textContent = `Time elapsed: ${playingTime * 1000}`;

      playingTime = playingTime - 1000;
    }, 1000);

    timerStatus = false;
  }
};

export { timer };
