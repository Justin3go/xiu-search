function remSize(){
    // 获取屏幕的宽度
    var deviceWidth = document.documentElement.clientWidth || window.innerWidth;
    // 限制屏幕的宽度
    if(deviceWidth >= 750){
        deviceWidth = 750
    }
    if(deviceWidth <= 320){
        deviceWidth = 320
    }
    document.documentElement.style.fontSize = (deviceWidth/7.5) + 'px'
    // 设计稿是750px
    // 设置一半的宽度，那么就是375px
    // 1rem == 100px的设计稿宽度
    // 表达一半的宽度就是3.75rem

    // 设置字体大小
    document.querySelector('body').style.fontSize = 0.16 + 'rem'
}

remSize();
// 当窗口发生变化时我们也调用一下这个函数
window.onresize = function(){
    remSize();
}