const axios = require('axios');
const FormData = require('form-data');
const fs = require("fs");

async function auth(username, fingerprint) {
    const formData = new FormData();
    formData.append('upload_file', fs.createReadStream(fingerprint));

    const response = await axios.post(`${process.env.BACKEND_URL}/compare-with-user?username=${username}`, formData, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'multipart/form-data'
        }
    });

    return response.data.match;
}

async function register(username, fingerprint) {
    const formData = new FormData();
    formData.append('upload_file', fs.createReadStream(fingerprint));

    await axios.post(`${process.env.BACKEND_URL}/add-file?username=${username}`, formData, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'multipart/form-data'
        }
    });
}

exports.auth = auth;
exports.register = register;
