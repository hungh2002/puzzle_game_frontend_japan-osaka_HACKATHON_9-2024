import { axios } from "../axios";

const imagesListHandle = async () => {
  //   {
  //     "pos": {
  //         "0": {
  //             "0": "img_11.png",
  //             "1": "img_23.png",
  //             "2": "img_32.png",
  //             "3": "img_22.png"
  //         },
  //         "1": {
  //             "0": "img_30.png",
  //             "1": "img_03.png",
  //             "2": "img_21.png",
  //             "3": "img_13.png"
  //         },
  //         "2": {
  //             "0": "img_31.png",
  //             "1": "img_10.png",
  //             "2": "img_01.png",
  //             "3": "img_20.png"
  //         },
  //         "3": {
  //             "0": "img_00.png",
  //             "1": "img_12.png",
  //             "2": "img_33.png",
  //             "3": "img_02.png"
  //         }
  //     }
  // }

  const imagesList = [];

  let data;
  try {
    const response = await axios.get("/img_list");
    data = response.data;
  } catch (error) {
    console.error("Failed to get image list:", error);
  }

  for (const [xKey, xValue] of Object.entries(data.pos)) {
    for (const [yKey, YValue] of Object.entries(data.pos[xKey])) {
      imagesList.push(
        `${import.meta.env.VITE_BACKEND_URL}/${data.pos[xKey][yKey]}`
      );
    }
  }

  return imagesList;
};

export { imagesListHandle };
