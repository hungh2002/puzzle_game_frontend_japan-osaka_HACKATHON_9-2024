import { axios } from "../axios";
import { user } from "../user";

const timeHandle = async () => {
  let data;
  const currentTime = new Date();

  try {
    const response = await axios.get("/q_and_a");
    data = response.data;
  } catch (error) {
    console.error("timeHandle ", error);
  }

  user.setQuestionAndAnswer({ question: data.question, answer: data.answer });

  let start =
    parseInt(data.start_time.hour) * 60 + parseInt(data.start_time.minute);
  let finish =
    parseInt(data.finish_time.hour) * 60 + parseInt(data.finish_time.minute);

  return {
    detail: data,
    startTime:
      (start - (currentTime.getHours() * 60 + currentTime.getMinutes())) *
        60 *
        1000 -
      40000,
    finishTime:
      (finish - (currentTime.getHours() * 60 + currentTime.getMinutes())) *
        60 *
        1000 -
      40000,
  };
};

export { timeHandle };
