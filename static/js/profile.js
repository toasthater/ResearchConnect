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

    self.get_user = function() {

        $.getJSON(get_user_url,            
            function(data) {
                if(data.user != null) {
                    self.vue._user_bio = self.vue.user_bio = data.user.user_bio;
                    self.vue._user_degree = self.vue.user_degree = data.user.user_degree;
                    self.vue._user_linkedin =  self.vue.user_linkedin= data.user.user_linkedin;
                    
                    self.vue.user = true;
                }                
        });
        self.vue.user_bio = self.vue._user_bio;
        self.vue.user_degree = self.vue._user_degree;
        self.vue.user_linkedin = self.vue._user_linkedin;
        console.log("user got");

        $("#vue-div").show();
    };

    self.submit_user = function() {
        self.vue.editing = false;
        self.vue.user = true;

        $.post(edit_user_url, {
            user_first_name: self.vue.user_first_name,
            user_last_name: self.vue.user_last_name,

            user_bio: self.vue.user_bio,
            user_degree: self.vue.user_degree,
            user_linkedin: self.vue.user_linkedin,
            user_pic: self.vue.user_pic,
        });

        self.vue._user_pic = null;
    };

    self.choose_image = function(event) {
        var input = event.target;
        var file = input.files[0];

        if (file) {
            var reader = new FileReader();
            reader.addEventListener("load", function () {
                self.vue._user_pic = self.vue.user_pic;
                self.vue.user_pic = reader.result;

            }, false);
            reader.readAsDataURL(file);
        }
    };

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

    self.download_picture = function() {
        $.getJSON(picture_get_url, { },
                function (data) {
                self.vue.user_pic = data.file_str;
                console.log("Resume got");
        });
    };

    self.download_resume = function(event) {
        $.getJSON(resume_get_url, 
            {

            }, function (data) {
                self.vue.resume = data.file_str;
                console.log("Resume got");
        });
    };


    self.cancel_editing = function() {
        self.vue.editing = false;

        if(self.vue._user_pic != null) {
            self.vue.user_pic = self.vue._user_pic;
        }

        self.vue.user_bio = self.vue._user_bio;
        self.vue.user_degree = self.vue._user_degree;
        self.vue.user_linkedin = self.vue._user_linkedin;
        


    };
 
    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            resume: null,
            is_logged_in: is_logged_in,
            user_email: user_email,
            user_id: user_id,

            editing: false,

            user: false,
            user_first_name: user_first_name,
            user_last_name: user_last_name,
            user_degree: null,
            user_bio: null,
            user_linkedin: null,

            user_pic: null,
            _user_pic: null,
        },

        methods: {
            upload_resume: self.upload_resume,
            download_resume: self.download_resume,
            submit_user: self.submit_user,
            choose_image: self.choose_image,
            cancel_editing: self.cancel_editing,
            
        }

    });

    //Put runtime code here
    self.download_picture();
    self.download_resume();
    self.get_user();

    
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
