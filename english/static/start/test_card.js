var test_card_build_status=null;
var caps_status=null;


//启动测试卡程序
function start_test_card(data)
{
    console.log('测试卡启动');
    //清空显示区
    clear_screen();
    //建造测试卡
    build_test_card(data);
}


//建造测试卡
function build_test_card(data)
{
    console.log('开始建造测试卡');
    let test_card_obj=$('#test_card');
    if(!test_card_build_status)
    {
        //设置测试卡长宽
        test_card_obj.css('width',`${scale}px`);
        test_card_obj.css('height',`${scale*1.5}px`);
        //建造汉语区
        test_card_build_chinese();
        //建造显示区
        test_card_build_screen();
        //建造输入区
        test_card_build_keys();
        //建造提交区
        test_card_build_ok();
        //修改建造状态,保证只建造一次
        test_card_build_status=true;
    }
    //更新内容
    test_card_update_content(data);
    //更换背景
    test_card_update_back();
    //记忆卡移动到显示区
    test_card_obj.css('left','0');
}


//建造汉语区
function test_card_build_chinese()
{
    console.log('开始建造汉语区');
    let test_chinese_obj=$('#test_chinese');
    let test_card_obj=$('#test_card');
    let test_chinese_text_obj=$('#test_chinese_text');
    test_chinese_text_obj.css('font-size',`${test_card_obj.width()*0.07}px`);
    test_chinese_text_obj.css('top',`20%`);
}


//建造显示区
function test_card_build_screen()
{
    console.log('开始建造显示区');
    let test_screen_obj=$('#test_screen');
    let test_card_obj=$('#test_card');
    let test_screen_text_obj=$('#test_screen_text');
    test_screen_text_obj.css('font-size',`${test_card_obj.width()*0.1}px`);
    test_screen_text_obj.css('top',`5%`);
}


//建造输入区
function test_card_build_keys()
{
    console.log('开始建造输入区');
    let test_keys_obj=$('#test_keys');
    let test_card_obj=$('#test_card');
    let test_keys_width=test_keys_obj.width();

    //第1行
    for(let i=0;i<"QWERTYUIOP".length;i++)
    {
        let c='QWERTYUIOP'[i];
        test_keys_obj.append(`<div id=${c} class='key' onclick="key_function(this)">`);
        let key_obj=$(`#${c}`);
        key_obj.append(c.toLowerCase());
        key_obj.css('top','5.5%');
        key_obj.css('left',`${0.4}%`);
        let left=parseFloat(key_obj.css('left').replace('px',''));
        key_obj.css('left',`${left+test_keys_width*i*0.10}`+'px');
        key_obj.css('font-size',`${test_keys_width*0.08}px`);
    }
    //第2行
    for(let i=0;i<'ASDFGHJKL'.length;i++)
    {
        let c='ASDFGHJKL'[i];
        test_keys_obj.append(`<div id=${c} class='key' onclick="key_function(this)">`);
        let key_obj=$(`#${c}`);
        key_obj.append(c.toLowerCase());
        key_obj.css('top','36%');
        key_obj.css('left',`${4}%`);
        let left=parseFloat(key_obj.css('left').replace('px',''));
        key_obj.css('left',`${left+test_keys_width*i*0.10}`+'px');
        key_obj.css('font-size',`${test_keys_width*0.08}px`);
    }
    //第3行
    for(let i=0;i<'ZXCVBNM'.length;i++)
    {
        let c='ZXCVBNM'[i];
        test_keys_obj.append(`<div id=${c} class='key' onclick="key_function(this)"  >`);
        let key_obj=$(`#${c}`);
        key_obj.append(c.toLowerCase());
        key_obj.css('top','67%');
        key_obj.css('left',`${16}%`);
        let left=parseFloat(key_obj.css('left').replace('px',''));
        key_obj.css('left',`${left+test_keys_width*i*0.10}`+'px');
        key_obj.css('font-size',`${test_keys_width*0.08}px`);
    }
    $('#del').css('font-size',`${test_keys_width*0.08}px`);
    $('#caps').css('font-size',`${test_keys_width*0.07}px`);

}


//建造提交区
function test_card_build_ok()
{
    console.log('开始建造汉语区');
    let test_card_obj=$('#test_card');
    let test_ok_text_obj=$('#test_ok_text');
    test_ok_text_obj.css('font-size',`${test_card_obj.width()*0.08}px`);
    test_ok_text_obj.css('top',`10%`)
}


//更新内容
function test_card_update_content(data)
{
    console.log('开始更新内容');
    let test_chinese_text_obj=$('#test_chinese_text');
    let test_screen_text_obj=$('#test_screen_text');
    //清空相关显示区
    test_chinese_text_obj.empty();
    test_screen_text_obj.empty();
    //填充相关显示区
    test_chinese_text_obj.append(data['chinese']);
}


//更新背景
function test_card_update_back()
{
    console.log('开始更新背景');
    while(true)
    {
        var num=Math.random().toString();
        num=num[num.length-1].toString();
        if('123456'.replace(num,'') !== '0123456789')
        {
            $('#test_card').css('background-image',`url(/static/start/test_word_back_${num}.jpg)`);
            break;
        }
    }
}


//字母按键
function key_function(event)
{
    let test_screen=$('#test_screen_text');
    let value=event.id;
    if(!caps_status)
    {
        value=value.toLowerCase();
    }
    test_screen.append(value);
}


//删除
function del_function()
{
    let test_screen_text=$('#test_screen_text');
    let text=test_screen_text.text();
    if(text.length>0)
    {
        text=test_screen_text.text();
        text=text.substr(0,text.length-1);
        test_screen_text.empty();
        test_screen_text.append(text);
    }
}


//大写锁定
function caps_function()
{
    let caps_obj=$('#caps');
    let keys='QWERTYUIOPASDFGHJKLZXCVBNM';
    if(caps_status)
    {
        for(let i=0;i<keys.length;i++)
        {
            let key_obj=$(`#${keys[i]}`);
            key_obj.empty();
            key_obj.append(keys[i].toLowerCase());
        }
        caps_obj.css('background','#fff9fb');
        caps_obj.css('color','#000000');
        caps_status=null;
    }
    else
    {
        caps_obj.css('background','#000000');
        caps_obj.css('color','#fff9fb');
        for(let i=0;i<keys.length;i++)
        {
            let key_obj=$(`#${keys[i]}`);
            key_obj.empty();
            key_obj.append(keys[i].toUpperCase());
        }
        caps_status=true;
    }
}


//测试卡提交按钮
function test_card_ok()
{
    console.log('测试卡提交按钮');
    let test_screen_text_obj=$('#test_screen_text');
    url='/main/decisioner/';
    word_data['answer']=test_screen_text_obj.text();
    success_function=decisioner_success;
    error_function=decisioner_error;
    get(url,word_data,success_function,error_function);
}














