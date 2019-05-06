var memory_card_build_status=null;


//启动记忆卡程序
function start_memory_card(data) {
    console.log('记忆卡启动');
    //清空显示区
    clear_screen();
    //建造记忆卡
    build_memory_card(data)
}


//建造记忆卡
function build_memory_card(data)
{
    console.log('开始建造记忆卡片');
    let memory_card_obj=$('#memory_card');
    if(!memory_card_build_status)
    {
        //设置记忆卡长宽
        memory_card_obj.css('width',`${scale}px`);
        memory_card_obj.css('height',`${scale*1.5}px`);
        //建造卡片区
        memory_card_build_body();
        //建造头部
        memory_card_build_head();
        //建造确认按钮
        memory_card_build_ok();
        //修改建造状态,保证只建造一次
        memory_card_build_status=true;
    }
    //更新内容
    memory_card_update_content(data);
    //记忆卡移动到显示区
    memory_card_obj.css('left','0');
}


//建造卡片区
function memory_card_build_body()
{
    console.log('开始建造图片区');

    let memory_body_obj=$('#memory_body');
    let memory_card_obj=$('#memory_card');
    //设置长宽
    memory_body_obj.css('width',`${memory_card_obj.width()}px`);
    memory_body_obj.css('height',`${memory_card_obj.width()*0.57}px`);
    //建造单词区
    body_build_english();
    //建造音标区
    body_build_pronunciation();
    //建造汉语区
    body_build_chinese();
}


//建造单词显示区
function body_build_english()
{
    console.log('开始建造单词显示区');
    let memory_card_obj=$('#memory_card');
    let memory_body_english_obj=$('#memory_body_english');
    memory_body_english_obj.css('font-size',`${memory_card_obj.width()*0.12}px`);
}


//建造音标显示区
function body_build_pronunciation()
{
    console.log('开始建造音标显示区');
    let memory_card_obj=$('#memory_card');
    let memory_body_pronunciation_obj=$('#memory_body_pronunciation');
    memory_body_pronunciation_obj.css('font-size',`${memory_card_obj.width()*0.07}px`);
}


//建造汉语释意显示区
function body_build_chinese()
{
    console.log('开始建造汉语释意显示区');
    let memory_card_obj=$('#memory_card');
    let memory_body_chinese_obj=$('#memory_body_chinese');
    memory_body_chinese_obj.css('font-size',`${memory_card_obj.width()*0.07}px`);
}


//建造记忆卡头部
function memory_card_build_head()
{
    console.log('开始建造记忆卡头部');
    let memory_card_obj=$('#memory_card');
    let memory_body_obj=$('#memory_body');
    let head_obj=$('#head');
    //设置长宽
    let height=(memory_card_obj.height()-memory_body_obj.height())/2;
    head_obj.css('width',`${memory_card_obj.width()}px`);
    head_obj.css('height',`${height}px`);
    //设置图片区top
    memory_body_obj.css('top',`${height}px`);
}


//建造确认按钮
function memory_card_build_ok()
{
    console.log('开始建造确认按钮');
    let memory_card_obj=$('#memory_card');
    let head_obj=$('#head');
    let memory_body_obj=$('#memory_body');
    let ok_obj=$('#ok');
    let ok_text_obj=$('#ok_text');
    let memory_card_width=memory_card_obj.width();
    ok_obj.css('width',`${memory_card_width*0.3}px`);
    ok_obj.css('height',`${memory_card_width*0.15}px`);
    ok_obj.css('left',`${memory_card_width*0.3}px`);

    //字体的大小和位置
    let ok_width=ok_obj.width();
    ok_text_obj.css('font-size',`${ok_width*0.4}px`);

    //设置按钮的顶部位置
    let a=head_obj.height()+memory_body_obj.height();
    let b=(memory_card_obj.height()-a-ok_obj.height())/2;
    ok_obj.css('top',`${a+b}px`);

}


//更新内容
function memory_card_update_content(data)
{
    console.log('更新单词内容');
    let memory_body_english_obj=$('#memory_body_english');
    let memory_body_chinese_obj=$('#memory_body_chinese');
    let memory_body_pronunciation_obj=$('#memory_body_pronunciation');
    //清空相关显示区
    memory_body_english_obj.empty();
    memory_body_chinese_obj.empty();
    memory_body_pronunciation_obj.empty();
    //填充相关显示区
    memory_body_english_obj.append(data['english']);
    memory_body_chinese_obj.append(data['chinese']);
    memory_body_pronunciation_obj.append(data['pronunciation']);
}


//头部关灯触发
function head_function() {
    let back_obj=$('#memory_card');
    let colour=back_obj.css('background-color');
    if (colour==='rgb(0, 0, 0)')
    {
        back_obj.css('background','#FFFFFF');
    }
    else
    {
        back_obj.css('background','#000000');
    }
}


//记忆卡提交按钮
function memory_submit_function()
{
    console.log('记忆卡触发提交');
    decisioner_function(word_data);
}










