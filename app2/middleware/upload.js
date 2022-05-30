const multer = require("multer");
const path = require("path");
const crypto = require("crypto");

const storage = multer.diskStorage({
    destination: "public/data/",
    filename: function (req, file, cb) {
        crypto.randomBytes(20, (err, buf) => {
            cb(null, buf.toString("hex") + path.extname(file.originalname))
        })
    }
});

const upload = multer({
    storage: storage,
    limits: {
        fileSize: 1024 * 1024 * 5
    }
});

module.exports = upload;
