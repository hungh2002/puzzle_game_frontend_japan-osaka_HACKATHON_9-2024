import { axios } from "./axios";

let imagesList = [];

const getImagesList = async () => {
  //   {
  //     "pos": {
  //         "0": {
  //             "0": "img_20.png",
  //             "1": "img_02.png",
  //             "2": "img_03.png",
  //             "3": "img_12.png"
  //         },
  //         "1": {
  //             "0": "img_01.png",
  //             "1": "img_13.png",
  //             "2": "img_21.png",
  //             "3": "img_30.png"
  //         },
  //         "2": {
  //             "0": "img_33.png",
  //             "1": "img_32.png",
  //             "2": "img_00.png",
  //             "3": "img_11.png"
  //         },
  //         "3": {
  //             "0": "img_31.png",
  //             "1": "img_22.png",
  //             "2": "img_23.png",
  //             "3": "img_10.png"
  //         }
  //     }
  // }

  //   const response = await axios.get("/img_list");
  //   return response.data;

  imagesList = {
    img_list: ["画像名1", "画像名2", "画像名3", "画像名4"],
  };
};

export { getImagesList };
