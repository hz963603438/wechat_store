/**
 * Created by Administrator on 2017/7/9.
 */
$(function() {
    var $num_show = $('.num_show');
    var $total_price = $('.total em')
    var goods_price = parseFloat($('.show_pirze em').text());
    var goods_store = parseInt($('.show_kucun em').text());
    $('.add').click(function() {
        //点击加按钮
        var goods_num = parseInt($num_show.val());
        if (goods_num > goods_store) {
            alert("亲只有这么多了,改天再来买");
        } else {
            var total_num = parseInt($num_show.val(goods_num + 1).val());
            get_total_price(total_num)
        }
    });
    $('.minus').click(function() {
        //点击减按钮
        var goods_num = parseInt($num_show.val());
        if (goods_num <= 1) {
            alert("亲就买一个吧 生活不易啊");
        } else {
            var total_num = $num_show.val(goods_num - 1).val();
            get_total_price(total_num)
        }
    });

    $num_show.blur(function() {
        // 用户自己输入数值的判断
        var inpunt_total_num = parseInt($num_show.val());
        if (isNaN(inpunt_total_num)) {
            alert("亲请输入一个整数可以啊");
            $num_show.val(1);
            inpunt_total_num = 1;
        } else if (inpunt_total_num < 1) {
            alert("亲就买一个吧 生活不易啊");
            $num_show.val(1);
            inpunt_total_num = 1;
        } else {
            if (inpunt_total_num > goods_store) {
                alert("亲只有这么多了,改天再来买");
                $num_show.val(goods_store);
                inpunt_total_num = goods_store;
            }
        }
        get_total_price(inpunt_total_num)
    });

    function get_total_price(total_num) {
        //计算总的价格
        var total_price = new Number(total_num * goods_price).toFixed(2);
        $total_price.html(total_price + "元");
    }


    // 加入购物车 动画
    var $add_cart = $('#add_cart');
    var $show_count = $('#show_count');
    var $add_jump = $('.add_jump');
    var $add_top = $add_cart.offset().top;
    var $add_left = $add_cart.offset().left;

    var $to_top = $show_count.offset().top;
    var $to_left = $show_count.offset().left;
    
    $add_cart.click(function() {
        // 点击添加到购物车按钮
        var buy_num = parseInt($('.num_show').val()); // 获取商品输入框中总的数量
        var add_cart_url = $('#add_cart_url').val();
        var $show_count = $('#show_count');
        $add_jump.css({
            'left': $add_left + 80,
            'top': $add_top + 10,
            'display': 'block'
        });
        $(".add_jump").stop().animate({
                'left': $to_left + 7,
                'top': $to_top + 7
            },
            "fast",
            function() {
                $(".add_jump").fadeOut('fast', function() {
                    cart_count = parseInt($show_count.html());
                    var total_num = cart_count + buy_num;

                    param = {'buy_num': buy_num};

                    $.get(add_cart_url, param, function(res) {
                        // 发送ajax请求 添加购物车
                       if(res.code === 0){
                           $show_count.html(res.buy_num);
                       }else{
                           alert('添加失败, 错误代码： ' + res.code);
                       }
                    });

                });

            });
    });



});