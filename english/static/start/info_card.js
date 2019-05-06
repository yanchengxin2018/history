info_card_build_status=null;


//启动信息卡程序
function start_info_card(data) {
    console.log('信息卡启动');
    //清空显示区
    clear_screen();
    //建造信息卡
    build_info_card(data);
}


//建造信息卡
function build_info_card(data)
{
    console.log('开始建造信息卡片');
    let info_card_obj=$('#info_card');
    if(!info_card_build_status)
    {
        //设置信息卡长宽
        info_card_obj.css('width',`${scale}px`);
        info_card_obj.css('height',`${scale*1.5}px`);
        //建造成功状态
        info_card_build_success_status();
        //建造信息区
        info_card_build_body();
        //建造提交区
        info_card_build_submit();
        //修改建造状态,保证只建造一次
        info_card_build_status=true;
    }
    //更新内容
    info_card_update_content(data);
    //更换背景
    info_card_update_back(data);
    //信息卡移动到显示区
    info_card_obj.css('left','0');
}


//建造成功状态
function info_card_build_success_status()
{
    console.log('开始建造成功状态');
    let success_status_obj=$('#info_card_success_status');
    let info_card_obj=$('#info_card');
    success_status_obj.css('font-size',`${info_card_obj.width()*0.1}px`);

}


//建造信息区
function info_card_build_body()
{
    console.log('开始建造信息区');
    //建造单词显示区
    info_card_body_build_word();
    //建造输入显示区
    info_card_body_build_input();
    //建造等级变化区
    info_card_body_build_level();
    //建造下次测试时间区
    info_card_body_build_time();
    //建造音标区
    info_card_body_build_pronunciation();
    //建造汉语区
    info_card_body_build_chinese();
}


//建造提交区
function info_card_build_submit()
{
    console.log('开始建造提交区');
    let submit_text_obj=$('#info_card_submit_text');
    let info_card_obj=$('#info_card');
    submit_text_obj.css('font-size',`${info_card_obj.width()*0.1}px`);
}


//建造单词显示区
function info_card_body_build_word()
{
    console.log('开始建造单词显示区');
    let info_card_obj=$('#info_card');
    let word_obj = $('#info_card_body_word_text');
    word_obj.css('font-size',`${info_card_obj.width()*0.1}px`);
}


//建造输入显示区
function info_card_body_build_input()
{
    console.log('开始建造区');
    let info_card_obj=$('#info_card');
    let input_obj = $('#info_card_body_input_text');
    input_obj.css('font-size',`${info_card_obj.width()*0.1}px`);
}


//建造等级变化区
function info_card_body_build_level()
{
    console.log('开始建造区');
    let info_card_obj=$('#info_card');
    let level_obj = $('#info_card_body_level_text');
    level_obj.css('font-size',`${info_card_obj.width()*0.06}px`);
}


//建造下次测试时间区
function info_card_body_build_time()
{
    console.log('开始建造区');
    let info_card_obj=$('#info_card');
    let time_obj = $('#info_card_body_time_text');
    time_obj.css('font-size',`${info_card_obj.width()*0.06}px`);
}


//建造音标区
function info_card_body_build_pronunciation()
{
    console.log('开始建造区');
    let info_card_obj=$('#info_card');
    let pronunciation_obj = $('#info_card_body_pronunciation_text');
    pronunciation_obj.css('font-size',`${info_card_obj.width()*0.06}px`);
}


//建造汉语区
function info_card_body_build_chinese()
{
    console.log('开始建造区');
    let info_card_obj=$('#info_card');
    let chinese_obj = $('#info_card_body_chinese_text');
    chinese_obj.css('font-size',`${info_card_obj.width()*0.05}px`);
}


//更新内容
function info_card_update_content(data)
{
    console.log('开始更新信息卡');
    let status_obj = $('#info_card_success_status_text');
    let word_obj = $('#info_card_body_word_text');
    let input_obj = $('#info_card_body_input_text');
    let level_obj = $('#info_card_body_level_text');
    let time_obj = $('#info_card_body_time_text');
    let pronunciation_obj = $('#info_card_body_pronunciation_text');
    let chinese_obj = $('#info_card_body_chinese_text');
    var success_status=null;
    status_obj.empty();
    word_obj.empty();
    input_obj.empty();
    level_obj.empty();
    time_obj.empty();
    pronunciation_obj.empty();
    chinese_obj.empty();
    if(data['success_status'])
    {
        success_status='正确';
    }
    else
    {
        success_status='错误';
    }
    status_obj.append(success_status);
    word_obj.append(data['english']);
    input_obj.append(data['answer']);
    level_obj.append(data['level']);
    time_obj.append(data['time']);
    pronunciation_obj.append(data['pronunciation']);
    chinese_obj.append(data['chinese']);
}


//更新背景
function info_card_update_back(data) {
    console.log('开始更新背景图片');

    let success_status=data['success_status'];

    let info_card_obj=$('#info_card');
    var num=null;
    if(success_status)
    {
        num=1;
        $('#info_card_success_status').css('background-color','#dfffdb');
        $('#info_card_body_input').css('background-color','#dfffdb');
    }
    else
    {
        num=0;
        $('#info_card_success_status').css('background-color','#fff5d1');
        $('#info_card_body_input').css('background-color','#fff5d1');
    }
    info_card_obj.css('background-image',`url(/static/start/info_card_back_${num}.jpg)`);
}


//信息卡提交
function info_card_submit()
{
    console.log('信息卡提交触发');
    decisioner_function();
}
