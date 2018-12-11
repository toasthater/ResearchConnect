// This is the js for the default/index.html view.

var app = function () {
    Vue.config.devtools = true;
    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function (a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    // Enumerates an array.
    var enumerate = function (v) { var k = 0; return v.map(function (e) { e._idx = k++; }); };

    self.get_applicants = function (pid) {
        $.post(get_applicants_url,
            {
                post_id: pid
            },
            function (data) {
                // I am assuming here that the server gives me a nice list
                // of posts, all ready for display.
                self.vue.applicant_list = data.applicant_list;
                // Post-processing.
                self.refresh_applicants();
            }
        );
    };

    self.refresh_applicants = function (){
        enumerate(self.vue.applicant_list);
        self.vue.applicant_list.map(function (e) {});
    }

    self.add_applicant = function (pid) {
        //$.web2py.disableElement($("#apply"));
        console.log("I'm in here");
        $.post(add_applicant_url,
            {
                post_id: pid,
            },
            function(data) {
                self.get_applicants(data.post_id);
                //self.refresh_applicants();
            }
        );
    };

    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            applicant_list: []
        },
        methods: {
            refresh_applicants: self.refresh_applicants,
            add_applicant: self.add_applicant
        }
    });

    // If we are logged in, shows the form to add posts.
    if (is_logged_in) {
        $("#add_post").show();
    }
    
    self.get_applicants(post_id);

    return self;
};

var APP = null;

jQuery(function () { APP = app(); });

