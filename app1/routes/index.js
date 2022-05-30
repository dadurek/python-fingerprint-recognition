const express = require('express');
const router = express.Router();
const comparator = require('../services/comparator');
const upload = require('../middleware/upload');
const fs = require("fs");

router.get('/', function (req, res, next) {
    res.render('index', {title: 'Express'});
});

router.post('/compare', upload.fields([{name: "image1", maxCount: 1}, {
    name: "image2",
    maxCount: 1
}]), function (req, res, next) {
    const image1base64 = fs.readFileSync(req.files.image1[0].path, {encoding: 'base64'});
    const image2base64 = fs.readFileSync(req.files.image2[0].path, {encoding: 'base64'});

    res.render("result", {
        score: 0.3, //comparator.compare(req.files["image1"][0].path, req.files["image2"][0].path),
        image1: image1base64,
        image2: image2base64
    });

    fs.unlinkSync(req.files.image1[0].path);
    fs.unlinkSync(req.files.image2[0].path);
});

module.exports = router;
