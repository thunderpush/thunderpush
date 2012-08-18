var Thunder = new function() {
    this.apikey = '';
    this.channels = [];
    this.reconnect_delays = [1000, 2500, 5000, 10000, 30000, 60000];
    this.reconnect_tries = 0;
    this.no_reconnect = false
    this.handlers = [];
    this.user = 'randomname'; // TODO: save in cookie
    this.options = {
        // verbose?
        log: false,

        // default address of thunderpush server
        gateway: "http://localhost:8080/connect/",
    };

    this.connect = function(apikey, channels, options) {
        this.apikey = apikey;
        this.channels = channels;

        // merge options
        for (var attr in options) {
            this.options[attr] = options[attr];
        }

        this.no_reconnect = false;
        this.user = this.options.user;
        this.makeConnection();

        var that = this;

        // add internal handler
        this.handlers.push(function(e) {
            if (e.data == 'WRONGKEY') {
                that.no_reconnect = true;
            }
        });
    };

    this.listen = function(handler) {
        this.log("New handler has been registered.");
        this.handlers.push(handler);
    };

    this.makeConnection = function() {
        var that = this;
        this.socket = new SockJS(this.options.gateway);

        this.socket.onopen = function() {
            that.log("Connection has been estabilished.");

            // reset retries counter
            that.reconnect_tries = 0;

            // connect and subscribe to channels
            that.socket.send("CONNECT " + that.user + ":" + that.apikey);
            that.socket.send("SUBSCRIBE " + that.channels.join(":"));
        }

        this.socket.onmessage = function(e) {
            that.log("Message has been received", e.data);

            try {
                // try to parse the message as json
                var json_data = JSON.parse(e.data);
                e.data = json_data;
            }
            catch(e) {
                // not json, leave it as is
            }

            for (var i = 0; i < that.handlers.length; i++) {
                that.handlers[i](e);
            }
        }

        this.socket.onclose = function() {
            that.log("Connection has been lost.");

            if (that.no_reconnect) {
                that.log("Reconnect supressed.");
                return;
            }

            var delay = that.reconnect_delays[that.reconnect_tries]
                || that.reconnect_delays[that.reconnect_delays.length - 1];

            that.log("Reconnecting in", delay, "ms...");
            that.reconnect_tries++;

            setTimeout(function() {
                that.makeConnection();
            }, delay);
        }
    };

    this.log = function(msg) {
        if (this.options.log
                && "console" in window && "log" in window.console) {

            if (arguments.length == 1) {
                console.log(arguments[0]);
            }
            else {
                console.log.apply(console, 
                    Array.prototype.slice.call(arguments));
            }
        }
    };
}