window.onload=start



function start() {
    let window_width=$(window).width()
    let main_obj=$('#choice')
    main_obj.width(window_width)
    // main_obj.width(1000)
    auto_div('choice',1.69)
    init_text(main_obj)
}

function auto_div(div_id,rate) {
    console.log(div_id)
    let div=$(`#${div_id}`)
    let width=div.width()
    let height=width * rate
    div.height(height)

}

function init_text(main_obj) {
    let main_width=main_obj.width()
    let login_mobile_text_obj=$('#login_mobile_text')
    let login_password_text_obj=$('#login_password_text')
    let login_submit_obj=$('#login_submit')
    let login_mobile_obj=$('#login_mobile')
    let login_password_obj=$('#login_password')

    login_mobile_text_obj.css('font-size',`${main_width*0.05}px`)
    login_password_text_obj.css('font-size',`${main_width*0.05}px`)
    login_submit_obj.css('font-size',`${main_width*0.05}px`)
    login_mobile_obj.css('font-size',`${main_width*0.05}px`)
    login_password_obj.css('font-size',`${main_width*0.05}px`)
}


