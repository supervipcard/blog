// 网页加载进度条
NProgress.start();
setTimeout(function () {
    NProgress.done();
}, 1000);

// 禁止拖动
(function () {
    $('img').attr('draggable', 'false');
    $('a').attr('draggable', 'false');
})();

// 页面回到顶部
$("#gotop").hide();
$(window).scroll(function () {
    if ($(window).scrollTop() > 100) {
        $("#gotop").fadeIn()
    } else {
        $("#gotop").fadeOut()
    }
});
$("#gotop").click(function () {
    $('html,body').animate({
        'scrollTop': 0
    }, 500)
});

// 页面文字是否能被选中
document.body.onselectstart = document.body.ondrag = function () {
    return true
};

// 分页
$('[data-toggle="tooltip"]').tooltip();
jQuery.ias({
    history: false,
    container: '.content',
    item: '.excerpt',
    pagination: '.pagination',
    next: '.next-page a',
    trigger: '查看更多',
    loader: '<div class="pagination-loading"><img src="/static/images/loading.gif" /></div>',
    triggerPageThreshold: 0,
    onRenderComplete: function () {
        $('.excerpt img').attr('draggable', 'false');
        $('.excerpt a').attr('draggable', 'false')
    }
});

// sidebar浮动
$(window).scroll(function () {
    var sidebar = $('.sidebar');
    var sidebarHeight = sidebar.height();
    var windowScrollTop = $(window).scrollTop();
    if (windowScrollTop > sidebarHeight + 60 && sidebar.length) {
        $('.fixed').css({
            'position': 'fixed',
            'top': '10px',
            'width': '360px'
        })
    } else {
        $('.fixed').removeAttr("style")
    }
});
