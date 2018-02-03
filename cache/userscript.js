// ==UserScript==
// @name         tingke
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        http://i.yanxiu.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    //setTimeout(function(){$(".clock-tip").click();},50000);
    window.setInterval(function(){$(".clock-tip").click();}, 60000);
})();