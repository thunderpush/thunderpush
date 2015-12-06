var isMSIE = /*@cc_on!@*/0;
var Thunder = new function() {
    this.channels = [];
    this.handlers = [];
    
    this.reconnect_delays = [1000, 2500, 5000, 10000, 30000, 60000];
    
    this.options = {
        // verbose?
        log: false,
        retry: true,
        protocol: 'http'
    };


    /** Underscore Functions **/
    var ArrayProto = Array.prototype, ObjProto = Object.prototype, FuncProto = Function.prototype;

    var
        push             = ArrayProto.push,
        slice            = ArrayProto.slice,
        concat           = ArrayProto.concat,
        toString         = ObjProto.toString,
        hasOwnProperty   = ObjProto.hasOwnProperty;
     
      var
        nativeForEach      = ArrayProto.forEach,
        nativeMap          = ArrayProto.map,
        nativeReduce       = ArrayProto.reduce,
        nativeReduceRight  = ArrayProto.reduceRight,
        nativeFilter       = ArrayProto.filter,
        nativeEvery        = ArrayProto.every,
        nativeSome         = ArrayProto.some,
        nativeIndexOf      = ArrayProto.indexOf,
        nativeLastIndexOf  = ArrayProto.lastIndexOf,
        nativeIsArray      = Array.isArray,
        nativeKeys         = Object.keys,
        nativeBind         = FuncProto.bind;

    var _ = function(obj) {
        if (obj instanceof _) return obj;
        if (!(this instanceof _)) return new _(obj);
        this._wrapped = obj;
    };

    if (typeof (/./) !== 'function') {
        _.isFunction = function(obj) {
          return typeof obj === 'function';
        };
    }
    _.identity = function(value) {
        return value;
    };
    _.lookupIterator = function(value) {
        return _.isFunction(value) ? value : function(obj){ return obj[value]; };
    };
    _.sortedIndex = function(array, obj, iterator, context) {
        iterator = iterator == null ? _.identity : _.lookupIterator(iterator);
        var value = iterator.call(context, obj);
        var low = 0, high = array.length;
        while (low < high) {
            var mid = (low + high) >>> 1;
            iterator.call(context, array[mid]) < value ? low = mid + 1 : high = mid;
        }
        return low;
    };
    _.indexOf = function(array, item, isSorted) {
        if (array == null) return -1;
        var i = 0, l = array.length;
        if (isSorted) {
            if (typeof isSorted == 'number') {
                i = (isSorted < 0 ? Math.max(0, l + isSorted) : isSorted);
            } else {
                i = _.sortedIndex(array, item);
                return array[i] === item ? i : -1;
            }
        }
        if (nativeIndexOf && array.indexOf === nativeIndexOf) return array.indexOf(item, isSorted);
        for (; i < l; i++) if (array[i] === item) return i;
        return -1;
    };
    /** UnderscoreJS Functions **/

    this.onSockOpen = function(cb) {
        if(typeof cb === 'function')
            this.onopen = cb;
    }

    this.onSockError = function(cb) {
        if(typeof cb === 'function')
            this.onerror = cb;
    }

    this.onSockClose = function(cb) {
        if(typeof cb === 'function')
            this.onclose = cb;
    }

    this.onSockMessage = function(cb) {
        if(typeof cb === 'function')
            this.onmessage = cb;
    }


    this.connect = function(server, apikey, channels, options) {
        this.apikey = apikey;
        this.channels = channels;
        this.reconnect_tries = 0;

        // merge options
        for (var attr in options) {
            this.options[attr] = options[attr];
        }

        this.server = this.options.protocol + "://" + server + "/connect";
        this.user = this.options.user;
        this.makeConnection();

        var that = this;
    };

    this.disconnect = function() {
        var thunder = this;

        this.socket.onclose = function(e) {
            if(this.onclose) this.onclose.call(thunder, e);
        }

        if(this.socket.readyState === SockJS.OPEN) return this.socket.close();
        return false;
    }

    /**
     * Subscribe to channel
     */
    this.subscribe = function(channel, success, error) {
        if(typeof channel !== 'string' || channel.length <= 0)
            throw {
                name: 'channel.invalid',
                message: 'Channel is not a string'
            };

        if(this.socket.readyState === SockJS.OPEN) {
            if(_.indexOf(this.channels, channel) !== -1) {
                typeof success === 'function' && success(this, 'Channel already subscribed');
                return true;
            }

            this.socket.send("SUBSCRIBE " + channel);
            this.channels.push(channel);
            typeof success === 'function' && success(this, 'Channel subscribed');
            return true;
        }

        typeof error === 'function' && error(this, 'Socket not open');
        throw {
            name: 'socket.status',
            message: 'Socket not OPEN: ' . this.socket.readyState
        };
    }

    /**
     * Subscribe to channel
     */
    this.unsubscribe = function(channel, success, error) {
        if(this.socket.readyState === SockJS.OPEN) {
            this.socket.send("UNSUBSCRIBE " + channel);

            var pos = _.indexOf(this.channels, channel);
            
            if(pos !== -1) {
                channels = this.channels.splice(pos, 1);
            }

            typeof success === 'function' && success(this, 'Channel unsubscribed');
            return true;
        }
        else {
            var error = ''
            typeof error === 'function' && error(this, 'Socket not open');
            throw {
                name: 'socket.status',
                message: 'Socket not OPEN: ' . this.socket.readyState
            };
        }
    }

    this.listen = function(handler) {
        this.log("New handler has been registered.");
        this.handlers.push(handler);
    };

    this.makeConnection = function() {
        var that = this;

        // make a connection
        this.socket = new SockJS(this.server, undefined, 
            {'debug': this.options.log});

        this.socket.onopen = function(e) {
            that.log("Connection has been established.");

            if (that.onopen) that.onopen.call(that, e);

            // reset retries counter
            that.reconnect_tries = 0;

            // connect and subscribe to channels
            that.socket.send("CONNECT " + that.user + ":" + that.apikey);

            if (that.channels.length)
                that.socket.send("SUBSCRIBE " + that.channels.join(":"));
        }

        this.socket.onmessage = function(e) {
            that.log("Message has been received", e.data);

            if (that.onmessage) that.onmessage.call(that, e);

            try {
                // try to parse the message as json
                var json_data = JSON.parse(e.data.payload);
                e.data = json_data;
            }
            catch(e) {
                // not json, leave it as is
            }

            for (var i = 0; i < that.handlers.length; i++) {
                that.handlers[i](e.data);
            }
        }

        this.socket.onerror = function(e) {
            if (that.onerror) that.onerror.call(that, e);
        }

        this.socket.onclose = function(e) {
            that.log("Connection has been lost.");

            if (that.onclose) that.onclose.call(that, e);

            if (that.options.retry === false) {
                that.log("Reconnect supressed because of retry option false");
                return;
            }

            if (e.code == 9000 || e.code == 9001 || e.code == 9002) {
                // received "key not good" close message
                that.log("Reconnect supressed because of:", e);
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
                if (isMSIE) {
                    var log = Function.prototype.bind.call(console.log, console);
                    log.apply(console, Array.prototype.slice.call(arguments));
                } else {
                    console.log.apply(console, Array.prototype.slice.call(arguments));
                }
            }
        }
    };
}