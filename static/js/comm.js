// 判断横竖屏
var utils = {
    debounce: function(func,delay){
        var timer = null;
        return function(){
            var context = this,
                args = arguments;
            clearTimeout(timer);
            timer = setTimeout(function(){
                func.apply(context,args);
            },delay);
        }
    }
}

