window.onload=start;
var scale=20;//比例尺,显示区宽度占比设备宽度
var word_data=null;


//初始化
function start()
{
    let window_width=$(window).width();
    scale=window_width*scale/100; //初始化比例尺
    build_screen();
    decisioner_function({});//运行决策器,决定开始加载哪一张卡片
}


//决策器
function decisioner_function(data)
{
    url='/main/decisioner/';
    success_function=decisioner_success;
    error_function=decisioner_error;
    get(url,data,success_function,error_function);
}


//决策器-成功
function decisioner_success(data,status)
{
    clear_screen();
    console.log('决策器运行成功');
    word_data=data;
    let card_type=data['card_type'];
    if(card_type==='memory_card'){
        console.log('卡片类型:记忆卡');
        start_memory_card(data)
    }
    else if(card_type==='test_card'){
        console.log('卡片类型:测试卡');
        start_test_card(data)
    }
    else if(card_type==='info_card'){
        console.log('卡片类型:信息卡');
        start_info_card(data)
    }
    else
    {
        console.log('记载失败!未知的卡片类型:',card_type);
    }
}


//决策器-失败
function decisioner_error(data,status)
{
    console.log('单词卡加载失败');
    console.log(data);
    console.log(status);
    clear_screen();
    let error_obj=$('#error');
    if(error_obj.text())
    {
        // let div_obj=$('#error');
        error_obj.empty();
        error_obj.append('<br><br><br><br><br><br>页面加载失败了!即将自动尝试.');
    }
    else
    {
        let body_obj=$('#body_id');
        let info='<div id="error"><br><br><br><br><br><br>页面加载失败了!2秒后重试.</div>';
        body_obj.append(info)
    }
    setTimeout(function () {
        decisioner_function();
    },100000);
}


//get请求
function get(url,data,success_function,error_function)
{
    $.ajax({
        url:url,
        async:true,
        contentType: "application/x-www-form-urlencoded",
        data:data,
        dataType:"json",
        success:success_function,
        error:error_function,
        //timeout:300,
        type:'get',
        });
}


//建造显示区
function build_screen()
{
    console.log('开始建造显示区');
    let back_obj=$('#back');
    back_obj.css('width',`${scale}px`);
    back_obj.css('height',`${scale*1.5}px`);
}


//清空显示区
function clear_screen()
{
    console.log('开始清理显示区');
    let back_childrens=$('#back').children();
    for(let i=0;i<back_childrens.length;i++)
    {
        let div=back_childrens[i];
        let div_obj=$(`#${div.id}`);
        div_obj.css('left','-300%');
    }
}
