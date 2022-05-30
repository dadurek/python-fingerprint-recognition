const axios = require('axios');
const FormData = require('form-data');
const fs = require("fs");

async function compare(image1, image2) {
    const formData = new FormData();
    formData.append('upload_file_1', fs.createReadStream(image1));
    formData.append('upload_file_2', fs.createReadStream(image2));

    const response = await axios.post(`${process.env.BACKEND_URL}/compare`, formData, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'multipart/form-data'
        }
    });

    return response.data.score;
}

exports.compare = compare;
