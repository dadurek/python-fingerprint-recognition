var express = require('express');
const upload = require("../middleware/upload");
var router = express.Router();
var auth = require("../services/auth");

/* GET home page. */
router.get('/', function (req, res, next) {
    if (req.session.user) {
        res.render('user', {username: req.session.user});
    } else {
        res.render('index');
    }
});

/* GET users listing. */
router.get('/login', function (req, res, next) {
    res.render('login', {error: req.query.error});
});

router.post('/login', upload.fields([{name: "fingerprint", maxCount: 1}]), async function (req, res, next) {
    var username = req.body.username;
    var fingerprint = req.files.fingerprint[0].path;

    var authResult = await auth.auth(username, fingerprint);
    if (authResult) {
        req.session.user = username;
        res.redirect('/');
    } else {
        res.redirect('/login?error=true');
    }
});

router.get('/logout', function (req, res, next) {
    req.session.destroy();
    res.redirect('/');

});

//register
router.get('/register', function (req, res, next) {
    res.render('register');

});

router.post('/register', upload.single("fingerprint"), async function (req, res, next) {
    var username = req.body.username;
    var fingerprint = req.file.path;

    await auth.register(username, fingerprint);
    req.session.user = username;
    res.redirect('/');
});

module.exports = router;
