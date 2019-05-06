window.onload=start;



function start() {
    let window_width=$(window).width()
    let main_obj=$('#back')
    main_obj.width(window_width)
    // main_obj.width(500)
    auto_div('back',1.69)
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
    let start_obj=$('#start')
    let setting_obj=$('#setting')
    let count_obj=$('#count')
    let part_obj=$('#part')
    let familiar_obj=$('#familiar')
    let help_obj=$('#help')

    start_obj.css('font-size',`${main_width*0.1}px`)
    setting_obj.css('font-size',`${main_width*0.1}px`)
    count_obj.css('font-size',`${main_width*0.1}px`)
    part_obj.css('font-size',`${main_width*0.1}px`)
    familiar_obj.css('font-size',`${main_width*0.1}px`)
    help_obj.css('font-size',`${main_width*0.1}px`)
}

