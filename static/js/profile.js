// This is the js for the default/profile.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    // Enumerates an array.
    var enumerate = function(v) { var k=0; return v.map(function(e) {e._idx = k++;});};


    self.upload_resume = function(event) {
        var input = event.target;
        var file = input.files[0];

        if (file) {
            var reader = new FileReader();
            reader.addEventListener("load", function () {
                self.vue.resume = reader.result;
                $.post(resume_post_url, {
            
                    file_str: self.vue.resume,
                });
            }, false);
            reader.readAsDataURL(file);
        }
    };

    self.download_resume = function(event) {
        $.getJSON(resume_get_url, 
            {

            }, function (data) {
                self.vue.resume = data.file_str;
                console.log("Resume got");
        });
    };
 
    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            resume: null,
        },
        methods: {
            upload_resume: self.upload_resume,
            download_resume: self.download_resume,
            
        }

    });

    //Put runtime code here
    self.download_resume();
    $("#vue-div").show();

    
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
