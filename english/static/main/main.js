window.onload=start



function start() {
    let window_width=$(window).width()
    let main_obj=$('#choice')
    main_obj.width(window_width)
    // main_obj.width(300)
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
    let register_obj=$('#register')
    let login_obj=$('#login')
    register_obj.css('font-size',`${main_width*0.1}px`)
    login_obj.css('font-size',`${main_width*0.1}px`)
}


