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

    self.get_participants = function (pid) {
        $.post(get_participants_url,
            {
                post_id: pid
            },
            function (data) {
                // I am assuming here that the server gives me a nice list
                // of posts, all ready for display.
                self.vue.participants_list = data.participant_list;
                // Post-processing.
                self.refresh_participants();
            }
        );
    }

    self.refresh_participants = function (){
        enumerate(self.vue.participants_list);
        self.vue.participants_list.map(function (e) {});
    }

    self.refresh_applicants = function (){
        enumerate(self.vue.applicant_list);
        self.vue.applicant_list.map(function (e) {});
    }

    self.add_applicant = function (pid) {
        can_apply = false;
        //$.web2py.disableElement($("#apply"));
        $.post(add_applicant_url,
            {
                post_id: pid
            },
            function(data) {
                self.get_applicants(data.post_id);
                //self.refresh_applicants();
            }
        );
    };

    self.add_participant = function (aid) {
        $.post(add_participant_url,
            {
                applicant_id: aid
            },
            function(data) {
                self.get_applicants(post_id);
                self.get_participants(post_id);
            }
        );
    };

    self.decline_participant = function (aid) {
        $.post(decline_participant_url,
            {
                applicant_id: aid
            },
            function(data) {
                self.get_applicants(post_id);
                self.get_participants(post_id);
            }
        );
    };

    self.remove_post = function (pid) {
        $.post(remove_post_url,
            {
                post_id: pid
            },
            function(data) {
            }
        );
    };

    self.toggle_post = function (pid, pst) {
        if(post_status == 'Open')
            post_status = 'Closed';
        else
            post_status = 'Open';
        $.post(toggle_post_url,
            {
                post_id: pid,
                post_status: pst
            },
            function(data) {
                self.get_applicants(data.post_id);
            }
        );
    };

    self.toggle_edit = function (pid) {
        is_editing = !is_editing;
        self.get_applicants(post_id);
    };

    self.submit_click = function (pid) {
        $.post(submit_click_url,
            {
                post_id: pid,
                post_title: post_title,
                post_content: post_content,
                post_department: post_department
            },
            function (data) {
                self.refresh_applicants();
            }
        );
    }


    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            applicant_list: [],
            participants_list: [],
        },
        methods: {
            refresh_applicants: self.refresh_applicants,
            refresh_participants: self.refresh_participants,
            add_applicant: self.add_applicant,
            decline_participant: self.decline_participant,
            add_participant: self.add_participant,
            remove_post: self.remove_post,
            toggle_post: self.toggle_post,
            toggle_edit: self.toggle_edit,
            submit_click: self.submit_click
        }
    });

    // If we are logged in, shows the form to add posts.
    if (is_logged_in) {
        $("#add_post").show();
    }
    
    self.get_participants(post_id);
    self.get_applicants(post_id);

    return self;
};

var APP = null;

jQuery(function () { APP = app(); });

