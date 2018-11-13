// This is the js for the default/index.html view.
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

    self.toggle_form = function () {
        $("#add_post").show();
        $("#toggle_form_button").hide();
    }

    self.add_post = function () {
        // We disable the button, to prevent double submission.
        $.web2py.disableElement($("#add-post"));
        var sent_title = self.vue.form_title; // Makes a copy 
        var sent_content = self.vue.form_content; // 
        $.post(add_post_url,
            // Data we are sending.
            {
                post_title: self.vue.form_title,
                post_content: self.vue.form_content
            },
            // What do we do when the post succeeds?
            function (data) {
                // Re-enable the button.
                $.web2py.enableElement($("#add-post"));
                // Clears the form.
                self.vue.form_title = "";
                self.vue.form_content = "";
                // Adds the post to the list of posts. 
                var new_post = {
                    id: data.post_id,
                    post_title: sent_title,
                    post_content: sent_content,
                    score: 0
                };
                self.vue.post_list.unshift(new_post);
                // We re-enumerate the array.
                self.process_posts();
                $("#add_post").hide();
                $("#toggle_form_button").show();
            });
        // If you put code here, it is run BEFORE the call comes back.
    };

    self.get_posts = function() {
        $.getJSON(get_post_list_url,
            function(data) {
                // I am assuming here that the server gives me a nice list
                // of posts, all ready for display.
                self.vue.post_list = data.post_list;
                // Post-processing.
                self.process_posts();
            }
        );
    };

    self.process_posts = function() {
        // This function is used to post-process posts, after the list has been modified
        // or after we have gotten new posts. 
        // We add the _idx attribute to the posts. 
        enumerate(self.vue.post_list);
        // We initialize the smile status to match the like. 
        self.vue.post_list.map(function (e) {
            // I need to use Vue.set here, because I am adding a new watched attribute
            // to an object.  See https://vuejs.org/v2/guide/list.html#Object-Change-Detection-Caveats
            // The code below is commented out, as we don't have smiles any more. 
            // Replace it with the appropriate code for thumbs. 
            // // Did I like it? 
            // // If I do e._smile = e.like, then Vue won't see the changes to e._smile .
             Vue.set(e, '_thumb', e.thumb);
             Vue.set(e, '_over_up', false);
             Vue.set(e, '_over_down', false);
             Vue.set(e, '_thumbs_up', e.thumb == 'u' ? true : false);
             Vue.set(e, '_thumbs_down', e.thumb == 'd' ? true : false);
             Vue.set(e, '_score', e.score);

        });
    };

    self.thumb_up_mouseover = function (post_idx) {
        var p = self.vue.post_list[post_idx];
        p._thumbs_up = !p._thumbs_up;
        p._over_up = true;
    };

    self.thumb_down_mouseover = function (post_idx) {
        var p = self.vue.post_list[post_idx];
        p._thumbs_down = !p._thumbs_down;
        p._over_down = true;
    };

    self.thumb_up_mouseout = function (post_idx) {
        var p = self.vue.post_list[post_idx];
        p._over_up = false;
        p._thumbs_up = p.thumb == 'u' ? true : false;
    };

    self.thumb_down_mouseout = function (post_idx) {
        var p = self.vue.post_list[post_idx];
        p._thumbs_down = p.thumb == 'd' ? true : false;
        p._over_down = false;
    };

    self.thumbs_up_click = function (post_idx) {
        var p = self.vue.post_list[post_idx];
        switch (p._thumb){
            case 'u':
                p._score--;
                break;
            case 'd':
                p._score += 2;
                break;
            default:
                p._score++;
        }
        var thumb_status = (p._thumb == 'u') ? null : 'u';
        p.thumb = thumb_status;
        p._thumb = p.thumb;
        p._thumbs_up = (p.thumb == 'u') ? true : false;
        //x means None for all we care
        //Need to update the score
        //Need to change the state of thumbs_up
        //Need to record the thumb_up

        $.post(set_thumb_url, {
            post_id: p.id,
            thumb: thumb_status
        });
    };

    self.thumbs_down_click = function (post_idx) {
        var p = self.vue.post_list[post_idx];
                switch (p._thumb){
            case 'u':
                p._score -= 2;
                break;
            case 'd':
                p._score++;
                break;
            default:
                p._score--;
        }
        var thumb_status = (p._thumb == 'd') ? null : 'd';
        p.thumb = thumb_status;
        p._thumb = p.thumb;
        p._thumbs_down = (p.thumb == 'd') ? true : false;
        //Need to update the score
        //Need to change the state of thumbs_down
        //Need to record the thumb_down
        $.post(set_thumb_url, {
            post_id: p.id,
            thumb: thumb_status
        });

    };

    self.thumbs_count = function (post_idx) {
       var p = self.vue.post_list[post_idx];
       $.getJSON(get_score_url, {post_id: p.id}, function (data) {
                p.score = data.score;
       })
    };


    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            form_title: "",
            form_content: "",
            post_list: []
        },
        methods: {
            add_post: self.add_post,
            thumb_up_mouseover: self.thumb_up_mouseover,
            thumb_down_mouseover: self.thumb_down_mouseover,
            thumb_up_mouseout: self.thumb_up_mouseout,
            thumb_down_mouseout: self.thumb_down_mouseout,
            thumbs_up_click: self.thumbs_up_click,
            thumbs_down_click: self.thumbs_down_click,
            thumbs_count: self.thumbs_count,
            toggle_form: self.toggle_form
        }

    });

    // If we are logged in, shows the form to add posts.
    if (is_logged_in) {
        $("#add_post").show();
    }

    // Gets the posts.
    self.get_posts();
    $("#add_post").hide();
    $("#toggle_form_button").show();
    return self;
};

var APP = null;

// No, this would evaluate it too soon.
// var APP = app();

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
