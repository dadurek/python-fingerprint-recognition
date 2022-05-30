// send request to BACKEND_URL/compare with the 2 images to compare
// receive response containing a 0-1 float indicating the similarity

const axios = require('axios');
const FormData = require('form-data');
const fs = require("fs");

// image1 and image2 are image files
async function compare(image1, image2) {
    const formData = new FormData();
    formData.append('image1', fs.createReadStream(image1));
    formData.append('image2', fs.createReadStream(image2));

    const response = await axios.post(`${process.env.BACKEND_URL}/compare`, formData);

    return response.data.score;
}

exports.compare = compare;