window.onload=start



function start() {
    let window_width=$(window).width()
    let main_obj=$('#choice')
    main_obj.width(window_width)
    // main_obj.width(500)
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
    let register_mobile_text_obj=$('#register_mobile_text')
    let register_password_text_obj=$('#register_password_text')
    let register_re_password_text_obj=$('#register_re_password_text')
    let register_submit_obj=$('#register_submit')

    let register_mobile_obj=$('#register_mobile')
    let register_password_obj=$('#register_password')
    let register_re_password_obj=$('#register_re_password')



    register_mobile_text_obj.css('font-size',`${main_width*0.05}px`)
    register_password_text_obj.css('font-size',`${main_width*0.05}px`)
    register_re_password_text_obj.css('font-size',`${main_width*0.05}px`)
    register_submit_obj.css('font-size',`${main_width*0.05}px`)

    register_mobile_obj.css('font-size',`${main_width*0.05}px`)
    register_password_obj.css('font-size',`${main_width*0.05}px`)
    register_re_password_obj.css('font-size',`${main_width*0.05}px`)
}


